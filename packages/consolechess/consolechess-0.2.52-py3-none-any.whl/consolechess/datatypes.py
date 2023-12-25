"""Types for ChessBoard."""

from collections.abc import Callable, Iterator
from dataclasses import dataclass
from typing import Literal

PieceType = Literal["king", "queen", "rook", "bishop", "knight", "pawn"]
Color = Literal["white", "black"]
Side = Literal["kingside", "queenside"]
StatusDescription = Literal[
    "checkmate",
    "stalemate",
    "opponent_resignation",
    "agreement",
    "threefold_repetition",
    "fivefold_repetition",
    "the_50_move_rule",
    "the_75_move_rule",
    "insufficient_material",
    "imported",
    "explosion",
]
SquareGenerator = Callable[[str], Iterator[str]]
StepFunction = Callable[[str, int], str]


@dataclass(frozen=True, slots=True)
class Piece:
    """A piece on a chess board."""

    piece_type: PieceType
    color: Color
    promoted: bool = False

    def __eq__(self: "Piece", other: object) -> bool:
        """Check if two pieces are of the same type and color."""
        if isinstance(other, Piece):
            return self.piece_type == other.piece_type and self.color == other.color
        return False


@dataclass(slots=True)
class GameStatus:
    """Status of the game."""

    game_over: bool
    winner: Color | None = None
    description: StatusDescription | None = None


@dataclass(frozen=True, slots=True)
class Opening:
    """An ECO game opening."""

    eco: str
    name: str
    moves: str
