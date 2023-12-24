"""A Chess Board."""

from collections import Counter
from collections.abc import Iterator, Sequence
from contextlib import contextmanager, suppress
from csv import DictReader
from pathlib import Path
from random import shuffle
from re import findall, search, sub
from textwrap import TextWrapper
from typing import ClassVar, overload

with suppress(ImportError):
    from rich.console import Console

from .constants import (
    ALGEBRAIC_PIECE_ABBRS,
    BLACK_SQUARES,
    CASTLING_FINAL_SQUARES,
    COLORS,
    FEN_REPRESENTATIONS,
    FILES,
    KING_NAVIGABLE_SQUARES,
    KNIGHT_NAVIGABLE_SQUARES,
    PIECE_SYMBOLS,
    PIECES_TO_TRACK,
    PLAINTEXT_ABBRS,
    SIDES,
    SQUARES,
    STAUNTON_PATTERN_GRID,
    WHITE_SQUARES,
)
from .datatypes import (
    Color,
    GameStatus,
    Opening,
    Piece,
    PieceType,
    Side,
    SquareGenerator,
)
from .exceptions import (
    InvalidMoveError,
    InvalidNotationError,
    OffGridError,
    OtherPlayersTurnError,
)
from .utils import (
    BISHOP_GENERATORS,
    DIRECTION_GENERATORS,
    GENERATORS_BY_PIECE_TYPE,
    QUEEN_GENERATORS,
    ROOK_GENERATORS,
    STEP_FUNCTIONS_BY_DIRECTION,
    get_adjacent_files,
    get_squares_between,
    other_color,
    step_diagonal_down_left,
    step_diagonal_down_right,
    step_diagonal_up_left,
    step_diagonal_up_right,
    step_down,
    step_left,
    step_right,
    step_up,
)


class ChessBoard:
    """A chess board."""

    AUTOPRINT: ClassVar[bool] = False
    """Print board upon `__repr__` call."""

    ARBITER_DRAW_AFTER_THREEFOLD_REPETITION: ClassVar[bool] = False
    """Do not require claim to draw after threefold repetition."""

    ARBITER_DRAW_AFTER_100_HALFMOVE_CLOCK: ClassVar[bool] = False
    """Do not require claim to draw after halfmove clock hits 100 moves."""

    LICHESS_RULES_FOR_INSUFFICIENT_MATERIAL: ClassVar[bool] = False
    """Use Lichess rules for insufficient material. Otherwise, use Chess.com rules."""

    def __init__(
        self: "ChessBoard",
        fen: str | None = None,
        pgn: str | None = None,
        *,
        empty: bool = False,
        import_fields: bool = True,
    ) -> None:
        """Create a chess board object."""
        self.halfmove_clock = 0
        self.turn: Color = "white"
        self.initial_fen: str | None = None
        self._grid: dict[str, Piece | None] = {sq: None for sq in SQUARES}
        self._initial_squares: dict[
            tuple[PieceType, Color, Side | None], str | None
        ] = {piece_tuple: None for piece_tuple in PIECES_TO_TRACK}
        self._has_moved: dict[tuple[PieceType, Color, Side | None], bool] = {
            piece_tuple: False for piece_tuple in PIECES_TO_TRACK
        }
        self._cached_checks: dict[tuple[int, Color], bool] = {}
        self._white_king_sq: str | None = None
        self._black_king_sq: str | None = None
        self._double_forward_last_move: str | None = None
        self._status = GameStatus(game_over=False)
        self._moves: list[str] = []
        self._moves_before_fen_import: int = 0
        self._hashes: list[int] = []
        self._must_promote_pawn: str | None = None
        self._fields: dict[str, str] = {}
        self._move_annotations: dict[str, str] = {}
        self._opening: Opening | None = None
        if not empty and fen is None and pgn is None:
            self.set_staunton_pattern()
        if fen is not None:
            self.import_fen(fen)
        if pgn is not None:
            self.import_pgn(pgn, import_fields=import_fields)
            return None
        with suppress(StopIteration):
            self.set_initial_positions()

    @overload
    def __getitem__(self: "ChessBoard", index: slice) -> list[Piece | None]: ...

    @overload
    def __getitem__(self: "ChessBoard", index: str) -> Piece | None: ...

    def __getitem__(
        self: "ChessBoard", index: slice | str
    ) -> Piece | None | list[Piece | None]:
        """Get a square's current piece, or None if empty."""
        if isinstance(index, str):
            return self._grid[index]
        return [
            self._grid[sq]
            for sq in (
                index.start,
                *get_squares_between(index.start, index.stop),
                index.stop,
            )[:: index.step if index.step is not None else 1]
        ]

    @overload
    def __setitem__(self: "ChessBoard", index: str, value: Piece | None) -> None: ...

    @overload
    def __setitem__(
        self: "ChessBoard", index: slice, value: Sequence[Piece | None]
    ) -> None: ...

    def __setitem__(
        self: "ChessBoard",
        index: str | slice,
        value: Piece | None | Sequence[Piece | None],
    ) -> None:
        """Set a square to a piece or None if setting to empty."""
        if isinstance(index, str):
            if not (isinstance(value, Piece) or value is None):
                msg = "Must set board square to Piece or None."
                raise TypeError(msg)
            if isinstance(value, Piece) and value.piece_type == "king":
                setattr(self, f"_{value.color}_king_sq", index)
            self._grid[index] = value
        elif isinstance(index, slice) and isinstance(value, Sequence):
            for i, sq in enumerate(
                (
                    index.start,
                    *get_squares_between(index.start, index.stop),
                    index.stop,
                )[:: index.step if index.step is not None else 1]
            ):
                self[sq] = value[i]
        else:
            msg = "Must set board square to Piece or None."
            raise TypeError(msg)

    def __iter__(self: "ChessBoard") -> Iterator[str]:
        """Iterate through board."""
        return iter(self._grid)

    def __hash__(self: "ChessBoard") -> int:
        """Hash position."""
        return hash(
            (
                (black_king_has_moved := self._has_moved["king", "black", None])
                or self._has_moved["rook", "black", "kingside"],
                black_king_has_moved or self._has_moved["rook", "black", "queenside"],
                (white_king_has_moved := self._has_moved["king", "white", None])
                or self._has_moved["rook", "white", "kingside"],
                white_king_has_moved or self._has_moved["rook", "white", "queenside"],
                self._double_forward_last_move if self.can_en_passant() else None,
                self.turn,
                *self._grid.items(),
            )
        )

    def __repr__(self: "ChessBoard") -> str:
        """Represent ChessBoard as string."""
        if self.AUTOPRINT:
            self.print()
        return f"ChessBoard('{self.fen}')"

    def _hash_grid(self: "ChessBoard") -> int:
        """Hash pieces on board."""
        return hash(tuple(self._grid.items()))

    @property
    def opening(self: "ChessBoard") -> Opening | None:
        """Get the ECO opening."""
        if self._opening is not None:
            return self._opening
        path = (
            Path(f"{Path(__file__).parent}/openings.csv")
            if "__file__" in globals()
            else Path("openings.csv")
        )
        moves = self.export_moves()
        with path.open() as file:
            candidates = [
                opening for opening in DictReader(file) if opening["moves"] in moves
            ]
        longest_len = 0
        if len(candidates) == 0:
            return None
        for candidate in candidates:
            length = len(candidate["moves"])
            if length > longest_len:
                longest = candidate
                longest_len = length
        self._opening = Opening(
            eco=longest["ECO"], name=longest["name"], moves=longest["moves"]
        )
        return self._opening

    def alternate_turn(
        self: "ChessBoard",
        *,
        reset_halfmove_clock: bool = False,
    ) -> None:
        """
        Alternate turn from white to black or black to white.
        If reset_capture is True, moves_since_capture will be set to 0.
        """
        self.turn = self._other_player
        self._hashes.append(hash(self))
        self.halfmove_clock = 0 if reset_halfmove_clock else self.halfmove_clock + 1

    def set_staunton_pattern(self: "ChessBoard") -> None:
        """Add Staunton pattern (initial piece squares)."""
        self._grid = STAUNTON_PATTERN_GRID.copy()
        self.set_initial_positions()

    @contextmanager
    def test_position(self: "ChessBoard", changes: dict[str, Piece | None]) -> Iterator:
        """
        Make temporary changes to the board to test properties of a position.
        Do not raise exceptions within a `test_position` context manager.
        """
        original_contents = {sq: self._grid[sq] for sq in changes}
        for sq in changes:
            self[sq] = changes[sq]
        yield
        for sq in original_contents:
            self[sq] = original_contents[sq]

    def set_random(self: "ChessBoard") -> None:
        """Set board for Fischer random chess / Chess960."""
        # Set pawns.
        ranks_and_colors: list[tuple[int, Color]] = [(2, "white"), (7, "black")]
        for rank, color in ranks_and_colors:
            for file in FILES:
                self[f"{file}{rank}"] = Piece("pawn", color)
        # Set major pieces.
        major_pieces = [
            "knight",
            "knight",
            "bishop_1",
            "bishop_2",
            "rook_1",
            "rook_2",
            "queen",
            "king",
        ]
        while True:
            shuffle(major_pieces)
            # Check if bishops are on opposite-color squares.
            bishop_1 = f"a{major_pieces.index('bishop_1')}"
            bishop_2 = f"a{major_pieces.index('bishop_2')}"
            if (bishop_1 in BLACK_SQUARES and bishop_2 in BLACK_SQUARES) or (
                bishop_1 in WHITE_SQUARES and bishop_2 in WHITE_SQUARES
            ):
                continue
            # Check if king is in between rooks.
            rook_1_rank = major_pieces.index("rook_1")
            rook_2_rank = major_pieces.index("rook_2")
            a_side_rook = rook_1_rank if rook_1_rank < rook_2_rank else rook_2_rank
            h_side_rook = rook_1_rank if a_side_rook == rook_2_rank else rook_1_rank
            king_rank = major_pieces.index("king")
            if king_rank > h_side_rook or king_rank < a_side_rook:
                continue
            break
        # Populate board.
        major_rank_and_colors: list[tuple[int, Color]] = [(1, "white"), (8, "black")]
        for rank, color in major_rank_and_colors:
            for i, piece in enumerate(major_pieces):
                pt: PieceType = piece.removesuffix("_1").removesuffix("_2")  # type: ignore
                self[f"{FILES[i]}{rank}"] = Piece(pt, color)
        self.set_initial_positions()
        self.initial_fen = self.fen
        self._fields["Variant"] = "Chess960"

    def set_initial_positions(self: "ChessBoard") -> None:
        """Set initial positions of pieces used for castling."""
        white_rooks = [sq for sq in SQUARES if self._grid[sq] == Piece("rook", "white")]
        black_rooks = [sq for sq in SQUARES if self._grid[sq] == Piece("rook", "black")]
        if len(white_rooks) == 2:
            self._initial_squares["rook", "white", "queenside"] = (
                white_rooks[0]
                if FILES.index(white_rooks[0][0]) < FILES.index(white_rooks[1][0])
                else white_rooks[1]
            )
            self._initial_squares["rook", "white", "kingside"] = (
                white_rooks[0]
                if self._initial_squares["rook", "white", "queenside"] != white_rooks[0]
                else white_rooks[1]
            )
        elif len(white_rooks) == 1:
            self._initial_squares["rook", "white", "queenside"] = white_rooks[0]
            self._initial_squares["rook", "white", "kingside"] = white_rooks[0]
        if len(black_rooks) == 2:
            self._initial_squares["rook", "black", "queenside"] = (
                black_rooks[0]
                if FILES.index(black_rooks[0][0]) < FILES.index(black_rooks[1][0])
                else black_rooks[1]
            )
            self._initial_squares["rook", "black", "kingside"] = (
                black_rooks[0]
                if self._initial_squares["rook", "black", "queenside"] != black_rooks[0]
                else black_rooks[1]
            )
        elif len(black_rooks) == 1:
            self._initial_squares["rook", "black", "queenside"] = black_rooks[0]
            self._initial_squares["rook", "black", "kingside"] = black_rooks[0]
        if self._white_king_sq is None:
            self._white_king_sq = next(
                sq for sq in self if self._grid[sq] == Piece("king", "white")
            )
        if self._black_king_sq is None:
            self._black_king_sq = next(
                sq for sq in self if self._grid[sq] == Piece("king", "black")
            )
        self._initial_squares["king", "white", None] = self._white_king_sq
        self._initial_squares["king", "black", None] = self._black_king_sq

    def import_pgn(self: "ChessBoard", pgn: str, *, import_fields: bool = True) -> None:
        """Import a game by PGN string."""
        pgn = pgn.replace("\n", " ")
        if "[FEN " in pgn and (match := search(r"\[FEN \"(.+?)\"\]", pgn)):
            fen = match.group(1)
            self.import_fen(fen)
        else:
            self.set_staunton_pattern()
        self.set_initial_positions()
        self.submit_moves(pgn)
        if import_fields:
            self._fields.update(dict(findall(r"\[([^\s]+) \"(.+?)\"\]", pgn)))
            self._move_annotations = dict(findall(r"(\d+\.+)[^\.\{]+?\{(.+?)\}", pgn))
        if (
            import_fields
            and not self.status.game_over
            and (result := search(r"\[Result \"(.+?)\"\]", pgn))
        ):
            match result.group(1):
                case "1/2-1/2":
                    self.draw()
                case "1-0":
                    self._status = GameStatus(
                        game_over=True, winner="white", description="imported"
                    )
                case "0-1":
                    self._status = GameStatus(
                        game_over=True, winner="black", description="imported"
                    )

    def import_fen(self: "ChessBoard", fen: str) -> None:
        """Import Forsyth-Edwards Notation to board."""
        if match := search(
            r"(?P<R8>[^/]+)/(?P<R7>[^/]+)/(?P<R6>[^/]+)/(?P<R5>[^/]+)/"
            r"(?P<R4>[^/]+)/(?P<R3>[^/]+)/(?P<R2>[^/]+)/(?P<R1>[^/\s]+) "
            r"(?P<turn>[wb]) (?P<castling>[KQkqA-Ha-h-]+) (?P<enpassant>[a-h1-8-]+)"
            r"(?: (?P<halfmove>\d+) (?P<fullmove>\d+))?",
            fen,
        ):
            groups = match.groups()
        else:
            msg = "Could not read FEN."
            raise ValueError(msg)

        # Populate board.
        for rank, group in zip(range(8, 0, -1), groups[:8], strict=True):
            cursor = f"a{rank}"
            for char in group:
                if char.isalpha():
                    self[cursor] = FEN_REPRESENTATIONS[char]
                    with suppress(IndexError):
                        cursor = f"{FILES[FILES.index(cursor[0]) + 1]}{cursor[1]}"
                elif char.isnumeric():
                    for _ in range(int(char)):
                        self[cursor] = None
                        with suppress(IndexError):
                            cursor = f"{FILES[FILES.index(cursor[0]) + 1]}{cursor[1]}"

        # Set turn.
        self.turn = "white" if groups[8] == "w" else "black"

        # Set en passant target square.
        if groups[10] != "-":
            self._double_forward_last_move = (
                f"{groups[10][0]}{5 if groups[10][1] == 6 else 4}"
            )

        # Set halfmove clock.
        if groups[11] is not None:
            self.halfmove_clock = int(groups[11])

        # Set fullmove number.
        if groups[12] is not None:
            self._moves_before_fen_import = int(groups[12]) - 1
            if groups[8] == "b":
                self._moves.append("_")

        # Set initial position variables for rooks and kings.
        self.set_initial_positions()

        # Set castling availability.
        if groups[9] == "-":
            self._has_moved["king", "white", None] = True
            self._has_moved["king", "black", None] = True
        else:
            queenside_rook_file = (
                sq[0]
                if (sq := self._initial_squares["rook", "white", "queenside"])
                is not None
                else "q"
            )
            kingside_rook_file = (
                sq[0]
                if (sq := self._initial_squares["rook", "white", "kingside"])
                is not None
                else "k"
            )
            if "K" not in groups[9] and kingside_rook_file.upper() not in groups[9]:
                self._has_moved["rook", "white", "kingside"] = True
            if "Q" not in groups[9] and queenside_rook_file.upper() not in groups[9]:
                self._has_moved["rook", "white", "queenside"] = True
            if "k" not in groups[9] and kingside_rook_file not in groups[9]:
                self._has_moved["rook", "black", "kingside"] = True
            if "q" not in groups[9] and queenside_rook_file not in groups[9]:
                self._has_moved["rook", "black", "queenside"] = True

        self.initial_fen = fen

    @property
    def fen(self: "ChessBoard") -> str:
        """Export the board in Forsyth-Edwards Notation."""
        return self.export_fen()

    def export_fen(
        self: "ChessBoard", *, no_clocks: bool = False, shredder: bool = False
    ) -> str:
        """Export the board in Forsyth-Edwards Notation."""
        fen = ""

        # Concatenate piece placement data.
        for rank in range(8, 0, -1):
            squares = [f"{file}{rank}" for file in FILES]
            blank_sq_counter = 0
            for sq in squares:
                if self._grid[sq] is None:
                    blank_sq_counter += 1
                    continue
                if blank_sq_counter > 0:
                    fen += str(blank_sq_counter)
                    blank_sq_counter = 0
                piece = self._grid[sq]
                assert piece is not None
                char = PLAINTEXT_ABBRS[piece.piece_type]
                fen += char.upper() if piece.color == "white" else char.lower()
            if blank_sq_counter > 0:
                fen += str(blank_sq_counter)
            if rank > 1:
                fen += "/"

        # Concatenate active color.
        fen += f" {self.turn[0]} "

        # Concatenate castling availability.
        if not shredder or (
            self._initial_squares["king", "white", None] is None
            or self._initial_squares["king", "black", None] is None
            or self._initial_squares["rook", "white", "kingside"] is None
            or self._initial_squares["rook", "white", "queenside"] is None
            or self._initial_squares["rook", "black", "kingside"] is None
            or self._initial_squares["rook", "black", "queenside"] is None
            or "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR" in fen
        ):
            white_kingside_castle_symbol = "K"
            white_queenside_castle_symbol = "Q"
            black_kingside_castle_symbol = "k"
            black_queenside_castle_symbol = "q"
        else:
            white_kingside_castle_symbol = (
                self._initial_squares["rook", "white", "kingside"][0].upper()
                if self._initial_squares["rook", "white", "kingside"] is not None
                else "K"
            )
            white_queenside_castle_symbol = (
                self._initial_squares["rook", "white", "queenside"][0].upper()
                if self._initial_squares["rook", "white", "queenside"] is not None
                else "Q"
            )
            black_kingside_castle_symbol = (
                self._initial_squares["rook", "black", "kingside"][0]
                if self._initial_squares["rook", "black", "kingside"] is not None
                else "k"
            )
            black_queenside_castle_symbol = (
                self._initial_squares["rook", "black", "queenside"][0]
                if self._initial_squares["rook", "black", "queenside"] is not None
                else "q"
            )
        any_castles_possible = False
        if (
            not self._has_moved["king", "white", None]
            and not self._has_moved["rook", "white", "kingside"]
        ):
            fen += white_kingside_castle_symbol
            any_castles_possible = True
        if (
            not self._has_moved["king", "white", None]
            and not self._has_moved["rook", "white", "queenside"]
        ):
            fen += white_queenside_castle_symbol
            any_castles_possible = True
        if (
            not self._has_moved["king", "black", None]
            and not self._has_moved["rook", "black", "kingside"]
        ):
            fen += black_kingside_castle_symbol
            any_castles_possible = True
        if (
            not self._has_moved["king", "black", None]
            and not self._has_moved["rook", "black", "queenside"]
        ):
            fen += black_queenside_castle_symbol
            any_castles_possible = True
        if not any_castles_possible:
            fen += "-"
        fen += " "

        # Concatenate en passant target square.
        if self._double_forward_last_move is not None:
            fen += self._double_forward_last_move[0]
            if self._double_forward_last_move[1] == "4":
                fen += "3"
            if self._double_forward_last_move[1] == "5":
                fen += "6"
        else:
            fen += "-"

        # Concatenate halfmove and fullmove clocks.
        if not no_clocks:
            fen += f" {self.halfmove_clock} {self.fullmove_clock}"

        return fen

    @property
    def fullmove_clock(self: "ChessBoard") -> int:
        """Return the current move number, as it appears in FEN notation."""
        return self._moves_before_fen_import + (len(self._moves) // 2) + 1

    @property
    def pgn(self: "ChessBoard") -> str:
        """Export game in Portable Game Notation."""
        return self.export_pgn()

    def export_pgn(
        self: "ChessBoard",
        fields: dict[str, str] | None = None,
        *,
        wrap: int | None = 80,
        include_current_position: bool = False,
        include_eco: bool = True,
    ) -> str:
        """Export game in Portable Game Notation. Default wrap is 80 chars."""
        _fields = self._fields if fields is None else fields
        output = ""
        header_fields = ["Event", "Site", "Date", "Round", "White", "Black"]
        for field in header_fields:
            if field in _fields:
                output += f'[{field} "{self._fields[field]}"]\n'
        if not self._status.game_over:
            output += '[Result "*"]\n'
        elif self._status.winner is None:
            output += '[Result "1/2-1/2"]\n'
        elif self._status.winner == "white":
            output += '[Result "1-0"]\n'
        elif self._status.winner == "black":
            output += '[Result "0-1"]\n'
        if self.initial_fen is not None:
            if "SetUp" not in _fields:
                output += '[SetUp "1"]\n'
            if "FEN" not in _fields:
                output += f'[FEN "{self.initial_fen}"]\n'
        if (
            include_eco
            and "ECO" not in self._fields
            and (opening := self.opening) is not None
        ):
            output += f'[ECO "{opening.eco}"]\n'
        for name, value in self._fields.items():
            if name not in header_fields and name != "Result":
                output += f'[{name} "{value}"]\n'
        if include_current_position:
            output += f'[CurrentPosition "{self.fen}"]\n'
        output += f"\n{self.export_moves(include_annotations=True, wrap=wrap)}\n"
        return output

    @property
    def epd(self: "ChessBoard") -> str:
        """Return Extended Position Description (EPD) as string."""
        return self.export_epd()

    @property
    def _other_player(self: "ChessBoard") -> Color:
        """Not ChessBoard.turn, but the other player."""
        return "black" if self.turn == "white" else "white"

    def export_epd(
        self: "ChessBoard",
        fields: dict[str, str] | None = None,
        *,
        include_hmvc: bool = True,
        include_fmvn: bool = True,
    ) -> str:
        """Return Extended Position Description (EPD) as string."""
        output = self.export_fen(no_clocks=True)
        if include_hmvc:
            output += f" hvmc {self.halfmove_clock};"
        if include_fmvn:
            output += f" fmvn {self.fullmove_clock};"
        if fields is not None:
            for field in fields:
                output += f" {field} {fields[field]};"
        return output

    def _pseudolegal_squares(
        self: "ChessBoard",
        initial_square: str,
        *,
        capture_only: bool = False,
        check_castle: bool = True,
    ) -> Iterator[str]:
        """
        Get all pseudolegal squares for a given piece.
        This includes squares occupied by the king or which, if moved to,
        would put the king in check. Use ChessBoard.legal_moves()
        to only include legal moves.

        If capture_only is True, only include squares which are eligible for capture.
        In other words, pawn forward moves will not be included in return list.

        If check_castle is True, yield post-castling positions for kings.
        """
        if (piece := self._grid[initial_square]) is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        match piece.piece_type:
            case "pawn":
                return self._pawn_pseudolegal_squares(
                    initial_square, piece, capture_only=capture_only
                )
            case "rook":
                return self._rook_pseudolegal_squares(initial_square, piece)
            case "queen":
                return self._queen_pseudolegal_squares(initial_square, piece)
            case "bishop":
                return self._bishop_pseudolegal_squares(initial_square)
            case "knight":
                return self._knight_pseudolegal_squares(initial_square)
            case "king":
                return self._king_pseudolegal_squares(
                    initial_square, piece, check_castle=check_castle
                )

    def legal_moves(self: "ChessBoard", square: str) -> Iterator[str]:
        """Get legal moves for a piece."""
        if (piece := self._grid[square]) is None:
            msg = f"No piece at square '{square}'."
            raise InvalidMoveError(msg)
        for sq in self._pseudolegal_squares(square):
            # If the piece is a pawn diagonal to the pseudolegal square,
            # and the square at pseudolegal square is None, it must be an en passant.
            if (
                piece.piece_type == "pawn"
                and sq[0] in get_adjacent_files(square)
                and self._grid[sq] is None
            ):
                if self.can_en_passant(square, sq[0]):
                    yield sq
            # If the piece is a king, it could be a castle.
            elif piece.piece_type == "king" and (
                (sq in ("c1", "g1", "c8", "g8") and self.can_castle(piece.color))
                or self.can_move_piece(square, sq, navigability_already_checked=True)
            ):
                yield sq
            # Otherwise, it goes through move_piece.
            else:
                if self.can_move_piece(square, sq, navigability_already_checked=True):
                    yield sq

    def can_move_piece(
        self: "ChessBoard",
        initial_square: str,
        final_square: str,
        *,
        navigability_already_checked: bool = False,
    ) -> bool:
        """
        Check if a piece can be moved to final_square without castling or en passant.
        Does not check turn.
        """
        piece = self._grid[initial_square]
        piece_at_final_square = self._grid[final_square]
        if piece is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        if (
            not navigability_already_checked
            and final_square not in self._pseudolegal_squares(initial_square)
        ):
            return False
        if piece_at_final_square is not None and (
            piece_at_final_square.color == piece.color
            or piece_at_final_square.piece_type == "king"
        ):
            return False
        with self.test_position({final_square: piece, initial_square: None}):
            if self.king_is_in_check(piece.color):
                return False
        return True

    def _pawn_pseudolegal_squares(
        self: "ChessBoard",
        initial_square: str,
        piece: Piece,
        *,
        capture_only: bool = False,
    ) -> Iterator[str]:
        """Get pawn's pseudolegal squares (ignores king capture rules)."""
        step_func = step_up if piece.color == "white" else step_down
        # forward and double forward advance
        with suppress(OffGridError):
            if (
                not capture_only
                and self._grid[(sq := step_func(initial_square, 1))] is None
            ):
                yield sq
                starting_rank = "2" if piece.color == "white" else "7"
                if (
                    initial_square[1] == starting_rank
                    and self._grid[(sq := step_func(initial_square, 2))] is None
                ):
                    yield sq
        # diagonal capture
        adjacent_files = get_adjacent_files(initial_square)
        rank = int(initial_square[1])
        for file in adjacent_files:
            sq = f"{file}{rank + 1 if piece.color == 'white' else rank - 1}"
            if sq not in SQUARES:
                break
            if (pc := self._grid[sq]) is not None and pc.color != piece.color:
                yield sq
        # en passant capture
        adjacent_squares = [f"{file}{initial_square[1]}" for file in adjacent_files]
        if self._double_forward_last_move in adjacent_squares:
            yield (
                f"{self._double_forward_last_move[0]}"
                f"{rank + 1 if piece.color == 'white' else rank - 1}"
            )

    def _rook_pseudolegal_squares(
        self: "ChessBoard", initial_square: str, piece: Piece
    ) -> Iterator[str]:
        """Get rook's pseudolegal squares (ignores king capture rules)."""
        for generator in ROOK_GENERATORS:
            iterator = generator(initial_square)
            for sq in iterator:
                other_piece = self._grid[sq]
                if other_piece is None:
                    yield sq
                else:
                    if other_piece.color != piece.color:
                        yield sq
                    break

    def _queen_pseudolegal_squares(
        self: "ChessBoard", initial_square: str, piece: Piece
    ) -> Iterator[str]:
        """Get queen's pseudolegal squares (ignores king capture rules)."""
        for generator in QUEEN_GENERATORS:
            for sq in generator(initial_square):
                other_piece = self._grid[sq]
                if other_piece is None:
                    yield sq
                else:
                    if other_piece.color != piece.color:
                        yield sq
                    break

    def _bishop_pseudolegal_squares(
        self: "ChessBoard", initial_square: str
    ) -> Iterator[str]:
        """Get bishop pseudolegal squares (ignores king capture rules)."""
        for generator in BISHOP_GENERATORS:
            for sq in generator(initial_square):
                piece = self._grid[sq]
                moving_piece = self._grid[initial_square]
                assert moving_piece is not None
                if piece is None:
                    yield sq
                else:
                    if piece.color != moving_piece.color:
                        yield sq
                    break

    def _knight_pseudolegal_squares(
        self: "ChessBoard", initial_square: str
    ) -> Iterator[str]:
        """Get knight pseudolegal squares (ignores king capture rules)."""
        candidates = KNIGHT_NAVIGABLE_SQUARES[initial_square]
        for sq in candidates:
            piece = self._grid[sq]
            if piece is None:
                yield sq
            else:
                moving_piece = self._grid[initial_square]
                assert moving_piece is not None
                if piece.color != moving_piece.color:
                    yield sq

    def _king_pseudolegal_squares(
        self: "ChessBoard",
        initial_square: str,
        piece: Piece,
        *,
        check_castle: bool = False,
    ) -> Iterator[str]:
        """Get king pseudolegal squares (ignores capture rules)."""
        for sq in KING_NAVIGABLE_SQUARES[initial_square]:
            if (pc := self._grid[sq]) is None or pc.color != piece.color:
                yield sq
        if check_castle:
            if self.can_castle(piece.color, "queenside"):
                yield f"c{initial_square[1]}"
            if self.can_castle(piece.color, "kingside"):
                yield f"g{initial_square[1]}"

    def move_piece(
        self: "ChessBoard",
        initial_square: str,
        final_square: str,
        *,
        autocastle: bool = True,
        ignore_turn: bool = False,
        skip_checks: bool = False,
        no_disambiguator: bool = False,
        return_metadata: bool = False,
    ) -> dict[str, str | bool] | None:
        """Move a game piece."""
        notation = ""
        piece = self._grid[initial_square]
        if piece is None:
            msg = f"No piece at initial_square '{initial_square}'."
            raise InvalidMoveError(msg)
        if not skip_checks and self._must_promote_pawn is not None:
            msg = (
                f"Must promote pawn at square '{self._must_promote_pawn}' "
                "before next move."
            )
            raise InvalidMoveError(msg)
        piece_at_final_square = self._grid[final_square]
        # Try to castle if king is moving to a final castling square,
        # or if rook is jumping over a king.
        if autocastle:
            castle_side: Side = (
                "queenside" if final_square[0] in ("c", "d") else "kingside"
            )
            if (
                piece.piece_type == "king"
                and final_square in ("c1", "c8", "g1", "g8")
                and self.can_castle(piece.color, castle_side)
            ):
                self.castle(piece.color, castle_side, skip_checks=True)
                return (
                    {"move_type": "castle", "side": castle_side}
                    if return_metadata
                    else None
                )
        # Reroute to self.en_passant if pawn captures on empty final square.
        if (
            piece.piece_type == "pawn"
            and initial_square[0] != final_square[0]
            and self._grid[final_square] is None
        ):
            self.en_passant(initial_square, final_square)
            return (
                {"move_type": "en_passant", "capture": True}
                if return_metadata
                else None
            )
        # Add piece type notation, disambiguating if necessary.
        notation += (
            PLAINTEXT_ABBRS[piece.piece_type] if piece.piece_type != "pawn" else ""
        )
        disambiguator = ""
        if not no_disambiguator:
            match piece.piece_type:
                case "rook" | "bishop" | "queen":
                    ambiguous_pieces: list[str] = []
                    generators: list[SquareGenerator] = GENERATORS_BY_PIECE_TYPE[
                        piece.piece_type
                    ]
                    for generator in generators:
                        for sq in generator(final_square):
                            if (pc := self._grid[sq]) == piece:
                                if sq != initial_square and self.can_move_piece(
                                    sq, final_square
                                ):
                                    ambiguous_pieces.append(sq)
                                break
                            elif pc is not None:
                                break
                case "pawn":
                    # Forward moves are unambiguous by nature.
                    if piece_at_final_square is None:
                        ambiguous_pieces = []
                    # If the piece is not None, it must be a diagonal capture.
                    else:
                        ambiguous_pieces = []
                        step_funcs = (
                            (step_diagonal_up_left, step_diagonal_up_right)
                            if piece_at_final_square.color == "white"
                            else (
                                step_diagonal_down_left,
                                step_diagonal_down_right,
                            )
                        )
                        for func in step_funcs:
                            with suppress(OffGridError):
                                if (
                                    (sq := func(final_square, 1)) != initial_square
                                    and self._grid[sq] is not None
                                    and self.can_move_piece(sq, final_square)
                                ):
                                    ambiguous_pieces = [sq]
                case "knight":
                    with self.test_position(
                        {final_square: Piece("knight", other_color(piece.color))}
                    ):
                        ambiguous_pieces = [
                            sq
                            for sq in KNIGHT_NAVIGABLE_SQUARES[final_square]
                            if self._grid[sq] == piece
                            and sq != initial_square
                            and self.can_move_piece(sq, final_square)
                        ]
                case "king":
                    ambiguous_pieces = []
            if len(ambiguous_pieces) > 0:
                possible_disambiguators = (
                    initial_square[0],
                    initial_square[1],
                    initial_square,
                )
                for possible_disambiguator in possible_disambiguators:
                    still_ambiguous_pieces = [
                        sq
                        for sq in ambiguous_pieces
                        if possible_disambiguator in sq and sq != initial_square
                    ]
                    if len(still_ambiguous_pieces) == 0:
                        disambiguator = possible_disambiguator
                        break
        notation += disambiguator
        if not skip_checks:
            # Check correct player's piece is being moved.
            if not ignore_turn and piece.color != self.turn:
                msg = f"It is {self.turn}'s turn."
                raise OtherPlayersTurnError(msg)
            # Check piece can navigate to square.
            if final_square not in self._pseudolegal_squares(initial_square):
                msg = "Not a valid move."
                raise InvalidMoveError(msg)
        # Update clocks and notation to denote capture, and raise exceptions
        # for illegal captures.
        if piece_at_final_square is not None:
            if piece.piece_type == "pawn" and len(notation) == 0:
                notation += initial_square[0]
            notation += "x"
            is_capture = True
            if piece_at_final_square.color == piece.color:
                msg = "Cannot place piece at square occupied by same color piece."
                raise InvalidMoveError(msg)
            elif piece_at_final_square.piece_type == "king":
                msg = "Cannot capture king."
                raise InvalidMoveError(msg)
        else:
            is_capture = False
        notation += final_square
        # Update has_moved variables (used to determine castling availability).
        if piece.piece_type == "king":
            self._has_moved["king", piece.color, None] = True
        elif piece.piece_type == "rook":
            if initial_square == (
                self._initial_squares["rook", "black", "kingside"]
                if piece.color == "black"
                else self._initial_squares["rook", "white", "kingside"],
            ):
                side: Side | None = "kingside"
            elif initial_square == (
                self._initial_squares["rook", "black", "queenside"]
                if piece.color == "black"
                else self._initial_squares["rook", "white", "queenside"],
            ):
                side = "queenside"
            else:
                side = None
            if side is not None:
                self._has_moved["rook", piece.color, side] = True
        if (
            piece.piece_type == "pawn"
            and abs(int(initial_square[1]) - int(final_square[1])) == 2
        ):
            self._double_forward_last_move = final_square
        else:
            self._double_forward_last_move = None
        # Test if king would be in check if moved.
        if not skip_checks:
            king_would_be_in_check = False
            with self.test_position({final_square: piece, initial_square: None}):
                if self.king_is_in_check(self.turn):
                    king_would_be_in_check = True
            if king_would_be_in_check:
                msg = "Cannot move piece because king would be in check."
                raise InvalidMoveError(msg)
        # Move piece.
        self[final_square] = piece
        self[initial_square] = None
        # If pawn moving to final rank, require pawn promotion.
        if piece.piece_type == "pawn" and final_square[1] in ("1", "8"):
            self._must_promote_pawn = final_square
        else:
            self._must_promote_pawn = None
            self.alternate_turn(
                reset_halfmove_clock=(piece.piece_type == "pawn" or is_capture),
            )
            if self.is_checkmate():
                notation += "#"
            elif self.king_is_in_check(self.turn):
                notation += "+"
        self._moves.append(notation)
        if not return_metadata:
            return None
        if piece_at_final_square is not None:
            return {
                "move_type": "normal",
                "capture": is_capture,
                "capture_piece_type": piece_at_final_square.piece_type,
                "capture_piece_is_promoted": piece_at_final_square.promoted,
            }
        else:
            return {"move_type": "normal", "capture": is_capture}

    def submit_moves(self: "ChessBoard", *notations: str) -> None:
        """Submit multiple moves at once with algebraic notation."""
        if len(notations) == 1 and " " in notations[0]:
            notations = tuple(
                sub(
                    r"[\s\n]+",
                    " ",
                    sub(
                        r"\d+\.+|\[.+?\]|\{.+?\}|[10]-[10]|1/2-1/2|\*", "", notations[0]
                    ),
                ).split()
            )
        for notation in notations:
            self.move(notation)

    @property
    def moves(self: "ChessBoard") -> str:
        """Export moves to string."""
        return self.export_moves()

    def export_moves(
        self: "ChessBoard",
        *,
        include_annotations: bool = False,
        wrap: int | None = None,
    ) -> str:
        """Export moves to string."""
        i = self._moves_before_fen_import
        output = ""
        moves = self._moves
        while True:
            i += 1
            if len(moves) == 1:
                move_no = f"{i}."
                move_annotation = f"{move_no} {moves[0]}"
                output += move_annotation
                if include_annotations and move_no in self._move_annotations:
                    output += f" {{{self._move_annotations[move_no]}}} "
            if len(moves) < 2:
                break
            move_no = f"{i}."
            output += f"{move_no} {moves[0]} "
            if include_annotations and move_no in self._move_annotations:
                output += f"{{{self._move_annotations[move_no]}}} {i}... "
            output += f"{moves[1]} "
            if include_annotations and (no := f"{i}...") in self._move_annotations:
                output += f"{{{self._move_annotations[no]}}} "
            moves = moves[2:]
        output = output.strip()
        status = self.status
        if status.game_over:
            match status.winner:
                case "white":
                    output += " 1-0"
                case "black":
                    output += " 0-1"
                case None:
                    output += " 1/2-1/2"
        else:
            output += " *"
        output = sub(r"\. _", "...", output).strip()
        return "\n".join(TextWrapper(width=wrap).wrap(output)) if wrap else output

    def move(
        self: "ChessBoard", notation: str, *, return_metadata: bool = False
    ) -> dict[str, str | bool] | None:
        """Make a move using algebraic notation."""
        if "O-O-O" in notation:
            self.castle(self.turn, "queenside")
            return (
                {"move_type": "castle", "side": "queenside", "capture": False}
                if return_metadata
                else None
            )
        elif "O-O" in notation:
            self.castle(self.turn, "kingside")
            return (
                {"move_type": "castle", "side": "kingside", "capture": False}
                if return_metadata
                else None
            )
        elif match := search(
            r"([KQRBN]?)([a-h1-8]{,2})x?([a-h][1-8])[\(=/]?([KQRBN]?)\)?\s?.*$",
            notation,
        ):
            piece_type = ALGEBRAIC_PIECE_ABBRS[match.group(1)]
            disambiguator = match.group(2)
            final_square = match.group(3)
            pawn_promotion = (
                ALGEBRAIC_PIECE_ABBRS[grp] if (grp := match.group(4)) != "" else None
            )
            match piece_type:
                case "rook" | "bishop" | "queen":
                    candidates = []
                    generators: list[SquareGenerator] = GENERATORS_BY_PIECE_TYPE[
                        piece_type
                    ]
                    for generator in generators:
                        for sq in generator(final_square):
                            if (pc := self._grid[sq]) == Piece(
                                piece_type, self.turn
                            ) and disambiguator in sq:
                                candidates.append(sq)
                            elif pc is not None:
                                break
                case "pawn":
                    candidates = []
                    # If capturing but moving to an empty square, it must be an
                    # en passant. For en passant moves, the file must also be
                    # specified (e.g. "exf6"). We know the initial rank by
                    # color, so there is only one candidate.
                    if "x" in notation and self._grid[final_square] is None:
                        candidates = [
                            f"{disambiguator}{5 if self.turn == 'white' else 4}"
                        ]
                    # If no piece at final square, it must be a forward advance.
                    elif self._grid[final_square] is None:
                        step_func = step_down if self.turn == "white" else step_up
                        with suppress(OffGridError):
                            if (
                                disambiguator in (sq := step_func(final_square, 1))
                                and (pc := self._grid[sq]) == Piece("pawn", self.turn)
                            ) or (
                                self._grid[(sq := step_func(final_square, 2))]
                                == Piece("pawn", self.turn)
                                and disambiguator in sq
                            ):
                                candidates.append(sq)
                    # Otherwise, it's a capture.
                    else:
                        step_funcs = (
                            (step_diagonal_down_left, step_diagonal_down_right)
                            if self.turn == "white"
                            else (step_diagonal_up_left, step_diagonal_up_right)
                        )
                        for func in step_funcs:
                            with suppress(OffGridError):
                                sq = func(final_square, 1)
                                if disambiguator in sq and self._grid[sq] == Piece(
                                    "pawn", self.turn
                                ):
                                    candidates.append(sq)
                case "knight":
                    with self.test_position(
                        {final_square: Piece("knight", self._other_player)}
                    ):
                        candidates = [
                            sq
                            for sq in KNIGHT_NAVIGABLE_SQUARES[final_square]
                            if disambiguator in sq
                            and self._grid[sq] == Piece(piece_type, self.turn)
                        ]
                case "king":
                    king_sq = (
                        self._white_king_sq
                        if self.turn == "white"
                        else self._black_king_sq
                    )
                    candidates = [king_sq] if king_sq is not None else []
            if len(candidates) == 1:
                initial_square = candidates[0]
            elif len(candidates) == 0:
                msg = f"'{notation}' is not allowed."
                raise InvalidNotationError(msg)
            else:
                successful_candidates = [
                    candidate
                    for candidate in candidates
                    if self.can_move_piece(candidate, final_square)
                ]
                if len(successful_candidates) == 1:
                    initial_square = successful_candidates[0]
                elif len(candidates) == 0:
                    msg = f"'{notation}' is not allowed."
                    raise InvalidNotationError(msg)
                else:
                    msg = f"Must disambiguate moving pieces: {successful_candidates}"
                    raise InvalidNotationError(msg)
            if (
                "x" in notation
                and self._grid[final_square] is None
                and "#" not in notation
            ):
                with suppress(InvalidMoveError):
                    self.en_passant(initial_square, final_square)
                    return (
                        {
                            "move_type": "en_passant",
                            "capture": True,
                            "capture_piece_type": "pawn",
                            "capture_piece_is_promoted": False,
                        }
                        if return_metadata
                        else None
                    )
            if (
                piece_type == "pawn"
                and final_square[1] in ("1", "8")
                and pawn_promotion is None
            ):
                msg = "Must promote pawn upon move to final rank."
                raise InvalidMoveError(msg)
            metadata = self.move_piece(
                initial_square,
                final_square,
                autocastle=False,
                no_disambiguator=(disambiguator == ""),
                return_metadata=return_metadata,
            )
            if pawn_promotion is not None:
                self.promote_pawn(final_square, pawn_promotion)
                if metadata is not None:
                    metadata["promote_pawn"] = True
            return metadata
        else:
            msg = f"Could not read notation '{notation}'."
            raise InvalidNotationError(msg)

    def can_castle(self: "ChessBoard", color: Color, side: Side | None = None) -> bool:
        """Check if a player can castle. Optionally specify side."""
        # Castling can only be done when:
        #  - The king has not moved.
        #  - The rook has not moved.
        #  - The king is not in check.
        #  - The king would not pass through a checked square.
        #  - The king would not land into a checked square.
        #  - There are no pieces between king and rook.
        king_has_moved = self._has_moved["king", color, None]
        if king_has_moved:
            return False
        king_sq = (
            self._initial_squares["king", "black", None]
            if color == "black"
            else self._initial_squares["king", "white", None]
        )
        if king_sq is None:
            return False
        sides = [side] if side is not None else SIDES
        rooks = [
            (
                self._initial_squares["rook", color, side_],
                self._has_moved["rook", color, side_],
                CASTLING_FINAL_SQUARES[color, side_],
            )
            for side_ in sides
        ]
        pcs_allowed_on_final_squares = (
            None,
            Piece("rook", color),
            Piece("king", color),
        )
        for rook_init_sq, rook_has_moved, final_squares in rooks:
            if rook_init_sq is None:
                continue
            squares_between = get_squares_between(king_sq, rook_init_sq)
            squares_king_crosses = get_squares_between(king_sq, final_squares[0])
            if (
                not rook_has_moved
                and self._grid[rook_init_sq] == Piece("rook", color)
                and all(self._grid[sq] is None for sq in squares_between)
                and all(
                    self._grid[sq] in pcs_allowed_on_final_squares
                    for sq in final_squares
                )
                and not self.king_is_in_check(color)
                and not any(
                    sq in squares_king_crosses for sq in self.checked_squares(color)
                )
            ):
                return True
        return False

    def castle(
        self: "ChessBoard",
        color: Color,
        side: Side,
        *,
        skip_checks: bool = False,
    ) -> None:
        """
        Move the king two spaces right or left and move the closest rook
        to its other side.
        """
        if not skip_checks:
            if color != self.turn:
                msg = f"It is {self.turn.upper()}'s turn."
                raise OtherPlayersTurnError(msg)
            if self._must_promote_pawn is not None:
                msg = (
                    f"Must promote pawn at square '{self._must_promote_pawn}' "
                    "before next move."
                )
                raise InvalidMoveError(msg)
        if skip_checks or self.can_castle(color, side):
            king_final_sq, rook_final_sq = CASTLING_FINAL_SQUARES[color, side]
            self[getattr(self, f"_{color}_king_sq")] = None
            rook_init_sq = self._initial_squares["rook", color, side]
            assert rook_init_sq is not None
            self[rook_init_sq] = None
            self[king_final_sq] = Piece("king", color)
            self[rook_final_sq] = Piece("rook", color)
            self._has_moved["king", color, None] = True
            self._has_moved["rook", color, side] = True
            self._double_forward_last_move = None
            self.alternate_turn()
            notation = "O-O" if side == "kingside" else "O-O-O"
            if self.is_checkmate():
                notation += "#"
            elif self.king_is_in_check(self.turn):
                notation += "+"
            self._moves.append(notation)
            self._must_promote_pawn = None
        else:
            msg = "Castling not allowed."
            raise InvalidMoveError(msg)

    def promote_pawn(self: "ChessBoard", square: str, piece_type: PieceType) -> None:
        """Promote a pawn on the farthest rank from where it started."""
        if (piece := self._grid[square]) is None:
            msg = f"No piece at square '{square}'."
            raise InvalidMoveError(msg)
        if piece.color != self.turn:
            msg = f"It is {self.turn}'s turn."
            raise OtherPlayersTurnError(msg)
        if (piece.color == "white" and square[1] != "8") or (
            piece.color == "black" and square[1] != "1"
        ):
            msg = (
                "Cannot promote pawn unless it is at "
                "farthest rank from where it started."
            )
            raise InvalidMoveError(msg)
        self[square] = Piece(piece_type, piece.color, promoted=True)
        self._double_forward_last_move = None
        self._hashes.append(hash(self))
        self._must_promote_pawn = None
        self.alternate_turn(reset_halfmove_clock=True)
        updated_notation = f"{self._moves[-1]}={PLAINTEXT_ABBRS[piece_type]}"
        if self.is_checkmate():
            updated_notation += "#"
        elif self.king_is_in_check(self.turn):
            updated_notation += "+"
        self._moves[-1] = updated_notation

    def can_en_passant(
        self: "ChessBoard",
        initial_square: str | None = None,
        capture_file: str | None = None,
    ) -> bool:
        """Check if an en passant capture is possible."""
        if self._double_forward_last_move is None:
            return False
        if initial_square is None:
            possible_capturing_pawn_sqs = [
                f"{file}{self._double_forward_last_move[1]}"
                for file in get_adjacent_files(self._double_forward_last_move)
            ]
            for sq in possible_capturing_pawn_sqs:
                if self._grid[sq] == Piece("pawn", self.turn):
                    return True
            return False
        candidate_squares = []
        for func in (step_left, step_right):
            with suppress(OffGridError):
                square = func(initial_square, 1)
                if capture_file is None or capture_file in square:
                    candidate_squares.append(square)
        if (
            self._double_forward_last_move not in candidate_squares
            or (piece := self._grid[initial_square]) is None
        ):
            return False
        color = piece.color
        with self.test_position(
            {
                initial_square: None,
                f"{capture_file}{6 if color == 'white' else 3}": Piece("pawn", color),
                self._double_forward_last_move: None,
            }
        ):
            if self.king_is_in_check(color):
                return False
        return True

    def en_passant(
        self: "ChessBoard",
        initial_square: str,
        final_square: str,
        *,
        skip_checks: bool = False,
    ) -> None:
        """Capture an adjacent file pawn that has just made a double forward advance."""
        piece = self[initial_square]
        if not skip_checks:
            if piece is None:
                msg = f"No piece at initial_square '{initial_square}'."
                raise InvalidMoveError(msg)
            if piece.color != self.turn:
                msg = f"It is {self.turn}'s turn."
                raise OtherPlayersTurnError(msg)
            if self._must_promote_pawn is not None:
                msg = (
                    f"Must promote pawn at square '{self._must_promote_pawn}' "
                    "before next move."
                )
                raise InvalidMoveError(msg)
        assert piece is not None
        if skip_checks or self.can_en_passant(initial_square, final_square[0]):
            assert self._double_forward_last_move is not None
            self[self._double_forward_last_move] = None
            self[initial_square] = None
            self[final_square] = piece
            self._double_forward_last_move = None
            notation = f"{initial_square[0]}x{final_square}"
            self.alternate_turn(reset_halfmove_clock=True)
            if self.is_checkmate():
                notation += "#"
            elif self.king_is_in_check(self.turn):
                notation += "+"
            self._moves.append(notation)
            self._must_promote_pawn = None

    @property
    def pieces(self: "ChessBoard") -> dict[str, Piece]:
        """Get all pieces on the board."""
        return {sq: piece for sq in self._grid if (piece := self._grid[sq]) is not None}

    def checked_squares(self: "ChessBoard", color: Color) -> Iterator[str]:
        """Get all checked squares for a color."""
        oc = other_color(color)
        other_color_pieces = [
            sq for sq in self if (pc := self._grid[sq]) is not None and pc.color == oc
        ]
        already_yielded: list[str] = []
        for init_sq in other_color_pieces:
            for sq in self._pseudolegal_squares(
                init_sq, capture_only=True, check_castle=False
            ):
                if sq not in already_yielded:
                    yield sq
                    already_yielded.append(sq)

    def is_checkmate(self: "ChessBoard") -> bool:
        """Check if either color's king is checkmated."""
        for color in COLORS:
            if (
                self.king_is_in_check(color)
                and not self.can_block_check(color)
                and not self.king_can_escape_check(color)
            ):
                self._status = GameStatus(
                    game_over=True,
                    winner=other_color(color),
                    description="checkmate",
                )
                return True
        return False

    def is_stalemate(
        self: "ChessBoard", pieces: dict[str, Piece] | None = None
    ) -> bool:
        """Check if the game is a stalemate."""
        pieces_ = self.pieces if pieces is None else pieces
        if all(
            list(self.legal_moves(sq)) == []
            for sq in pieces_
            if pieces_[sq].color == self.turn
        ) and not self.can_castle(self.turn):
            self._status = GameStatus(game_over=True, description="stalemate")
            return True
        return False

    def is_draw_by_fivefold_repetition(self: "ChessBoard") -> bool:
        """Check if any position has repeated 5 times or more."""
        with suppress(IndexError):
            if Counter(self._hashes).most_common(1)[0][1] >= 5:
                self._status = GameStatus(
                    game_over=True, description="fivefold_repetition"
                )
                return True
        return False

    def is_draw_by_insufficient_material(
        self: "ChessBoard", pieces: dict[str, Piece] | None = None
    ) -> bool:
        """Check if board has insufficient material."""
        _pieces = self.pieces if pieces is None else pieces
        white_pieces = []
        black_pieces = []
        for sq in _pieces:
            if (pc := _pieces[sq]).color == "white":
                white_pieces.append(pc.piece_type)
            else:
                black_pieces.append(pc.piece_type)
        pieces_by_color = white_pieces, black_pieces
        if not self.LICHESS_RULES_FOR_INSUFFICIENT_MATERIAL:
            for pcs, other_pcs in pieces_by_color, pieces_by_color[::-1]:
                counter = Counter(pcs)
                if (
                    counter["pawn"] > 0
                    or counter["rook"] > 0
                    or counter["queen"] > 0
                    or counter["bishop"] > 1
                    or (counter["bishop"] > 0 and counter["knight"] > 0)
                    or (counter["knight"] > 1 and other_pcs != ["king"])
                ):
                    return False
            self._status = GameStatus(
                game_over=True, description="insufficient_material"
            )
            return True
        else:
            is_sufficient = False
            for color_pieces, other_color_pieces in (
                pieces_by_color,
                pieces_by_color[::-1],
            ):
                # A king + any(pawn, rook, queen) is sufficient.
                if (
                    "rook" in color_pieces
                    or "pawn" in color_pieces
                    or "queen" in color_pieces
                ):
                    is_sufficient = True
                    break
                # A king and more than one other type of piece is sufficient
                # (i.e. knight + bishop). A king and two (or more) knights
                # is also sufficient.
                if color_pieces.count("knight") + color_pieces.count("bishop") > 1:
                    is_sufficient = True
                    break
                # King + knight against king + any(rook, bishop, knight, pawn)
                # is sufficient.
                if "knight" in color_pieces and any(
                    pt in other_color_pieces
                    for pt in ("rook", "knight", "bishop", "pawn")
                ):
                    is_sufficient = True
                    break
                # King + bishop against king + any(knight, pawn) is sufficient.
                if "bishop" in color_pieces and (
                    "knight" in other_color_pieces or "pawn" in other_color_pieces
                ):
                    is_sufficient = True
                    break
                # King + bishop(s) is also sufficient if there's bishops on
                # opposite colours (even king + bishop against king + bishop).
                if "bishop" in color_pieces and "bishop" in color_pieces:
                    bishops = [
                        sq for sq in _pieces if _pieces[sq].piece_type == "bishop"
                    ]
                    bishop_square_colors = {
                        ("white" if bishop in WHITE_SQUARES else "black")
                        for bishop in bishops
                    }
                    if len(bishop_square_colors) == 2:
                        is_sufficient = True
                        break
            if not is_sufficient:
                self._status = GameStatus(
                    game_over=True, description="insufficient_material"
                )
                return True
            return False

    def is_draw_by_75_move_rule(self: "ChessBoard") -> bool:
        """Check if draw by 75 moves without pawn move or capture."""
        if self.halfmove_clock >= 150:
            self._status = GameStatus(game_over=True, description="the_75_move_rule")
            return True
        return False

    @property
    def status(self: "ChessBoard") -> GameStatus:
        """Check the board for a checkmate or draw."""
        pieces = self.pieces
        if (
            self._status.game_over
            or self.is_checkmate()
            or self.is_stalemate(pieces)
            or (
                self.ARBITER_DRAW_AFTER_THREEFOLD_REPETITION
                and self.can_claim_draw_by_threefold_repetition()
            )
            or self.is_draw_by_fivefold_repetition()
            or self.is_draw_by_insufficient_material(pieces)
            or (
                self.ARBITER_DRAW_AFTER_100_HALFMOVE_CLOCK
                and self.can_claim_draw_by_halfmove_clock()
            )
            or self.is_draw_by_75_move_rule()
        ):
            return self._status
        return GameStatus(game_over=False)

    def can_block_check(
        self: "ChessBoard", color: Color, *, drop_pool: list[PieceType] | None = None
    ) -> bool:
        """Return True if a check can be blocked by another piece."""
        pieces = self.pieces
        same_color_pieces_except_king = []
        other_color_pieces = []
        for sq in pieces:
            if (pc := pieces[sq]).color == color:
                if pc.piece_type == "king":
                    king = sq
                else:
                    same_color_pieces_except_king.append(sq)
            else:
                other_color_pieces.append(sq)
        checks: list[str] = [
            piece
            for piece in other_color_pieces
            if king in self._pseudolegal_squares(piece, capture_only=True)
        ]
        squares_that_would_block_check = []
        for check in checks:
            if (rank_difference := int(king[1]) - int(check[1])) > 0:
                rank_direction = "up"  # i.e. king is upward of piece
            elif rank_difference == 0:
                rank_direction = "inline"
            else:
                rank_direction = "down"
            if (file_difference := FILES.index(king[0]) - FILES.index(check[0])) > 0:
                file_direction = "right"  # i.e. king is to the right of piece
            elif file_difference == 0:
                file_direction = "inline"
            else:
                file_direction = "left"
            possible_squares = [
                check,
                *list(DIRECTION_GENERATORS[rank_direction, file_direction](check)),
            ]
            if (pt := pieces[check].piece_type) in ("knight", "pawn"):
                squares_that_would_block_check.append(check)
            if pt in ("rook", "bishop", "queen"):
                for square in possible_squares:
                    if square == king:
                        break
                    squares_that_would_block_check.append(square)
        # In variants like Crazyhouse, a piece can be dropped on the board
        # to block checkmate. It only works when there is a piece in the
        # pool to drop, and there is only one check to block. Also,
        # it must be noted that pawns can only be dropped on ranks 2-7.
        if drop_pool is not None and drop_pool != [] and len(checks) == 1:
            no_drop_on_first_or_eighth = set(drop_pool) == {"pawn"}
            for sq in squares_that_would_block_check:
                if sq not in checks and not (
                    no_drop_on_first_or_eighth and sq[1] in ("1", "8")
                ):
                    return True
        possible_moves: list[tuple[str, str]] = []  # [(from, to), ...]
        for sq in same_color_pieces_except_king:
            possible_moves.extend(
                [(sq, move) for move in self._pseudolegal_squares(sq)]
            )
        # Check if en passant capture can block check.
        if self._double_forward_last_move is not None:
            adjacent_squares = [
                f"{file}{self._double_forward_last_move[1]}"
                for file in get_adjacent_files(self._double_forward_last_move)
            ]
            final_rank = (
                int(self._double_forward_last_move[1]) + 1
                if color == "white"
                else int(self._double_forward_last_move[1]) - 1
            )
            final_sq = f"{self._double_forward_last_move[0]}{final_rank}"
            for sq in adjacent_squares:
                if self._grid[sq] == Piece("pawn", color) and self.can_en_passant(
                    sq, self._double_forward_last_move[0]
                ):
                    with self.test_position(
                        {
                            self._double_forward_last_move: None,
                            sq: None,
                            final_sq: Piece("pawn", color),
                        }
                    ):
                        if not self.king_is_in_check(color):
                            return True
        squares_that_can_be_moved_to = [move[1] for move in possible_moves]
        for square in squares_that_can_be_moved_to:
            if square in squares_that_would_block_check:
                candidates = [move for move in possible_moves if move[1] == square]
                for initial_sq, final_sq in candidates:
                    with self.test_position(
                        {initial_sq: None, final_sq: self._grid[initial_sq]}
                    ):
                        if not self.king_is_in_check(color):
                            return True
        return False

    def king_is_in_check(
        self: "ChessBoard", color: Color, hash: int | None = None
    ) -> bool | None:
        """Return True if king is in check."""
        hash_ = self._hash_grid() if hash is None else hash
        if self._cached_checks.get((hash_, color)):
            return self._cached_checks[hash_, color]
        king_sq = self._white_king_sq if color == "white" else self._black_king_sq
        if king_sq is None:
            return None
        # Check if a piece above/left/right/below king can capture.
        for generator in ROOK_GENERATORS:
            for sq in generator(king_sq):
                if (
                    (pc := self._grid[sq]) is not None
                    and pc.color != color
                    and pc.piece_type in ("rook", "queen")
                ):
                    self._cached_checks[hash_, color] = True
                    return True
                elif pc is not None:
                    break
        # Check if a piece diagonal to king can capture.
        for generator in BISHOP_GENERATORS:
            for sq in generator(king_sq):
                if (
                    (pc := self._grid[sq]) is not None
                    and pc.color != color
                    and pc.piece_type in ("bishop", "queen")
                ):
                    self._cached_checks[hash_, color] = True
                    return True
                elif pc is not None:
                    break
        # Find the squares which, if occupied by an opposite color pawn, check the king.
        pawn_sq_funcs = (
            (step_diagonal_up_left, step_diagonal_up_right)
            if color == "white"
            else (step_diagonal_down_left, step_diagonal_down_right)
        )
        pawn_sqs = []
        for func in pawn_sq_funcs:
            with suppress(OffGridError):
                pawn_sqs.append(func(king_sq, 1))
        for sq in pawn_sqs:
            if self._grid[sq] == Piece("pawn", other_color(color)):
                self._cached_checks[hash_, color] = True
                return True
        # Check if opposite color king is touching the king.
        for func_ in STEP_FUNCTIONS_BY_DIRECTION.values():
            try:
                sq = func_(king_sq, 1)
            except OffGridError:
                continue
            if self._grid[sq] == Piece("king", other_color(color)):
                self._cached_checks[hash_, color] = True
                return True
        # Check if an opponent knight checks the king.
        with self.test_position({king_sq: Piece("knight", color)}):
            for sq in KNIGHT_NAVIGABLE_SQUARES[king_sq]:
                if self._grid[sq] == Piece("knight", other_color(color)):
                    self._cached_checks[hash_, color] = True
                    return True
        self._cached_checks[hash_, color] = False
        return False

    def king_can_escape_check(self: "ChessBoard", color: Color) -> bool:
        """Check if a king can escape check (assuming it is in check)."""
        king_sq = self._white_king_sq if color == "white" else self._black_king_sq
        assert king_sq is not None
        return len(list(self.legal_moves(king_sq))) > 0

    def resign(self: "ChessBoard", color: Color | None = None) -> GameStatus:
        """Resign instead of moving."""
        self._status = GameStatus(
            game_over=True,
            winner=self._other_player if color is None else other_color(color),
            description="opponent_resignation",
        )
        return self._status

    def draw(self: "ChessBoard") -> GameStatus:
        """Draw instead of moving."""
        if self.can_claim_draw():
            return self.claim_draw()
        self._status = GameStatus(game_over=True, description="agreement")
        return self._status

    def can_claim_draw(self: "ChessBoard") -> bool:
        """Check if a draw can be claimed without agreement."""
        return (
            self.can_claim_draw_by_halfmove_clock()
            or self.can_claim_draw_by_threefold_repetition()
        )

    def can_claim_draw_by_halfmove_clock(self: "ChessBoard") -> bool:
        """Check if draw can be claimed due to 50 moves without pawn move or capture."""
        can_claim = self.halfmove_clock >= 100
        if can_claim and self.ARBITER_DRAW_AFTER_100_HALFMOVE_CLOCK:
            self._status = GameStatus(game_over=True, description="the_50_move_rule")
        return can_claim

    def can_claim_draw_by_threefold_repetition(self: "ChessBoard") -> bool:
        """Check if draw can be claimed due to threefold repetition."""
        try:
            can_claim = Counter(self._hashes).most_common(1)[0][1] >= 3
            if can_claim and self.ARBITER_DRAW_AFTER_THREEFOLD_REPETITION:
                self._status = GameStatus(
                    game_over=True, description="threefold_repetition"
                )
        except IndexError:
            return False
        else:
            return can_claim

    def claim_draw(self: "ChessBoard") -> GameStatus:
        """Claim a draw due to 50 moves without a capture or pawn move."""
        if self._status.game_over:
            return self._status
        if (move_rule := self.halfmove_clock >= 100) or (
            Counter(self._hashes).most_common(1)[0][1] >= 3
        ):
            self._status = GameStatus(
                game_over=True,
                description="the_50_move_rule" if move_rule else "threefold_repetition",
            )
            return self._status
        return GameStatus(game_over=False)

    @property
    def _rich_renderable(self: "ChessBoard") -> str:
        """Return a Rich renderable representation of the board."""
        losing_king_sq: str | None = None
        winning_king_sq: str | None = None
        if self.status.description == "checkmate":
            losing_king_sq = (
                self._white_king_sq
                if self._status.winner == "black"
                else self._black_king_sq
            )
        if self._status.winner is not None:
            winning_king_sq = (
                self._white_king_sq
                if self._status.winner == "white"
                else self._black_king_sq
            )
        rank_renderable = "\n"
        for rank in range(8, 0, -1):
            rank_renderable += f"[white]{rank}[/white] "
            rank_grid = [sq for sq in self if sq[1] == str(rank)]
            for sq in rank_grid:
                piece = self._grid[sq]
                if piece is not None:
                    symbol = "#" if sq == losing_king_sq else " "
                    if sq == winning_king_sq:
                        color_tags = ("[reverse][#FFD700]", "[/reverse][/#FFD700]")
                    else:
                        color_tags = (
                            ("[reverse][#ffffff]", "[/#ffffff][/reverse]")
                            if piece.color == "white"
                            else ("[white]", "[/white]")
                        )
                    rank_renderable += (
                        f"{color_tags[0]}{PIECE_SYMBOLS[piece.piece_type]}"
                        f"{symbol}{color_tags[1]}"
                    )
                else:
                    rank_renderable += (
                        "[reverse][#789656]  [/reverse][/#789656]"
                        if sq in BLACK_SQUARES
                        else "[reverse][#f0edd1]  [/reverse][/#f0edd1]"
                    )
            rank_renderable += "\n"
        rank_renderable += "[bold][white]  a b c d e f g h [/bold][/white]\n"
        return rank_renderable

    @property
    def ascii(self: "ChessBoard") -> str:
        """Get an ASCII representation of the board."""
        if self.status.description == "checkmate":
            winning_king_sq = (
                self._black_king_sq
                if self._status.winner == "white"
                else self._white_king_sq
            )
        output = ""
        for rank in range(8, 0, -1):
            output += f"{rank} "
            rank_grid = [sq for sq in self if sq[1] == str(rank)]
            for sq in rank_grid:
                piece = self._grid[sq]
                if piece is None:
                    output += ". "
                else:
                    output += (
                        f"{PLAINTEXT_ABBRS[piece.piece_type].upper()}"
                        f"{'#' if sq == winning_king_sq else ' '}"
                        if piece.color == "white"
                        else f"{PLAINTEXT_ABBRS[piece.piece_type].lower()} "
                    )
            output += "\n"
        output += "  a b c d e f g h "
        return output

    def print(self: "ChessBoard", *, plaintext: bool = False) -> None:
        """Print the ChessBoard to console."""
        if not plaintext and "Console" in globals():
            Console().print(self._rich_renderable)
        else:
            print(self.ascii)
