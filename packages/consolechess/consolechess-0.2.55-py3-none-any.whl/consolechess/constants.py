"""Constants for ChessBoard."""

from platform import system

from .datatypes import Color, Piece, PieceType, Side

COLORS: tuple[Color, Color] = ("white", "black")
SIDES: tuple[Side, Side] = ("queenside", "kingside")
FILES = list("abcdefgh")
SQUARES = [f"{file}{rank}" for rank in range(1, 9) for file in FILES]
PIECE_SYMBOLS: dict[PieceType, str] = {
    "king": "♚",
    "queen": "♛",
    "rook": "♜",
    "bishop": "♝",
    "knight": "♞",
    "pawn": "♟︎" if "Windows" not in system() else ":chess_pawn:",
}
BLACK_SQUARES = [f"{file}{rank}" for file in "aceg" for rank in (1, 3, 5, 7)] + [
    f"{file}{rank}" for file in "bdfh" for rank in (2, 4, 6, 8)
]
WHITE_SQUARES = [sq for sq in SQUARES if sq not in BLACK_SQUARES]
PLAINTEXT_ABBRS: dict[str, str] = {
    "knight": "N",
    "rook": "R",
    "bishop": "B",
    "pawn": "P",
    "queen": "Q",
    "king": "K",
}
ALGEBRAIC_PIECE_ABBRS: dict[str, PieceType] = {
    "K": "king",
    "Q": "queen",
    "R": "rook",
    "B": "bishop",
    "N": "knight",
    "": "pawn",
    "P": "pawn",
}
FEN_REPRESENTATIONS: dict[str, Piece] = {
    "N": Piece("knight", "white"),
    "K": Piece("king", "white"),
    "R": Piece("rook", "white"),
    "B": Piece("bishop", "white"),
    "Q": Piece("queen", "white"),
    "P": Piece("pawn", "white"),
    "n": Piece("knight", "black"),
    "k": Piece("king", "black"),
    "r": Piece("rook", "black"),
    "b": Piece("bishop", "black"),
    "q": Piece("queen", "black"),
    "p": Piece("pawn", "black"),
}
PIECES: list[Piece] = [
    *([Piece("rook", "white")] * 2),
    *([Piece("knight", "white")] * 2),
    *([Piece("bishop", "white")] * 2),
    Piece("queen", "white"),
    Piece("king", "white"),
    *([Piece("pawn", "white")] * 8),
    *([Piece("rook", "black")] * 2),
    *([Piece("knight", "black")] * 2),
    *([Piece("bishop", "black")] * 2),
    Piece("queen", "black"),
    Piece("king", "black"),
    *([Piece("pawn", "black")] * 8),
]
CASTLING_FINAL_SQUARES: dict[tuple[Color, Side], tuple[str, str]] = {
    ("white", "kingside"): ("g1", "f1"),  # color, side: rook, king
    ("white", "queenside"): ("c1", "d1"),
    ("black", "kingside"): ("g8", "f8"),
    ("black", "queenside"): ("c8", "d8"),
}
PIECES_TO_TRACK: list[tuple[PieceType, Color, Side | None]] = [
    ("king", "white", None),
    ("rook", "white", "kingside"),
    ("rook", "white", "queenside"),
    ("king", "black", None),
    ("rook", "black", "kingside"),
    ("rook", "black", "queenside"),
]
STAUNTON_PATTERN_GRID = {
    "a1": Piece(piece_type="rook", color="white"),
    "b1": Piece(piece_type="knight", color="white"),
    "c1": Piece(piece_type="bishop", color="white"),
    "d1": Piece(piece_type="queen", color="white"),
    "e1": Piece(piece_type="king", color="white"),
    "f1": Piece(piece_type="bishop", color="white"),
    "g1": Piece(piece_type="knight", color="white"),
    "h1": Piece(piece_type="rook", color="white"),
    "a2": Piece(piece_type="pawn", color="white"),
    "b2": Piece(piece_type="pawn", color="white"),
    "c2": Piece(piece_type="pawn", color="white"),
    "d2": Piece(piece_type="pawn", color="white"),
    "e2": Piece(piece_type="pawn", color="white"),
    "f2": Piece(piece_type="pawn", color="white"),
    "g2": Piece(piece_type="pawn", color="white"),
    "h2": Piece(piece_type="pawn", color="white"),
    "a3": None,
    "b3": None,
    "c3": None,
    "d3": None,
    "e3": None,
    "f3": None,
    "g3": None,
    "h3": None,
    "a4": None,
    "b4": None,
    "c4": None,
    "d4": None,
    "e4": None,
    "f4": None,
    "g4": None,
    "h4": None,
    "a5": None,
    "b5": None,
    "c5": None,
    "d5": None,
    "e5": None,
    "f5": None,
    "g5": None,
    "h5": None,
    "a6": None,
    "b6": None,
    "c6": None,
    "d6": None,
    "e6": None,
    "f6": None,
    "g6": None,
    "h6": None,
    "a7": Piece(piece_type="pawn", color="black"),
    "b7": Piece(piece_type="pawn", color="black"),
    "c7": Piece(piece_type="pawn", color="black"),
    "d7": Piece(piece_type="pawn", color="black"),
    "e7": Piece(piece_type="pawn", color="black"),
    "f7": Piece(piece_type="pawn", color="black"),
    "g7": Piece(piece_type="pawn", color="black"),
    "h7": Piece(piece_type="pawn", color="black"),
    "a8": Piece(piece_type="rook", color="black"),
    "b8": Piece(piece_type="knight", color="black"),
    "c8": Piece(piece_type="bishop", color="black"),
    "d8": Piece(piece_type="queen", color="black"),
    "e8": Piece(piece_type="king", color="black"),
    "f8": Piece(piece_type="bishop", color="black"),
    "g8": Piece(piece_type="knight", color="black"),
    "h8": Piece(piece_type="rook", color="black"),
}
WINNER_BY_PGN_RESULT: dict[str, Color | None] = {
    "1-0": "white",
    "0-1": "black",
    "1/2-1/2": None,
}
PGN_RESULT_BY_WINNER: dict[Color | None, str] = {
    "white": "1-0",
    "black": "0-1",
    None: "1/2-1/2",
}
