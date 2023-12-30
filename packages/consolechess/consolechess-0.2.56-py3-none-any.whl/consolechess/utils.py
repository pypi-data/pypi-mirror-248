"""Helper functions for board.py."""

import re
from contextlib import suppress
from functools import cache
from pathlib import Path

from .constants import FILES, SQUARES
from .datatypes import Color, PieceType, SquareGenerator, StepFunction


@cache
def other_color(color: Color) -> Color:
    """Get white if black, or black if white."""
    return "black" if color == "white" else "white"


@cache
def get_adjacent_files(square: str) -> list[str]:
    """Get FILES adjacent to square."""
    adjacent_files: list[str] = []
    match square[0]:
        case "a":
            adjacent_files = ["b"]
        case "h":
            adjacent_files = ["g"]
        case _:
            for index in (
                FILES.index(square[0]) + 1,
                FILES.index(square[0]) - 1,
            ):
                with suppress(IndexError):
                    adjacent_files.append(FILES[index])
    return adjacent_files


@cache
def iter_to_top(square: str) -> list[str]:
    """Get board squares up to the top (rank 8)."""
    return [f"{square[0]}{rank}" for rank in range(int(square[1]) + 1, 9)]


@cache
def iter_to_bottom(square: str) -> list[str]:
    """Get board squares down to the bottom (rank 1)."""
    return [f"{square[0]}{rank}" for rank in range(int(square[1]) - 1, 0, -1)]


@cache
def iter_to_right(square: str) -> list[str]:
    """Get board squares to the right (file h)."""
    return [f"{file}{square[1]}" for file in FILES[FILES.index(square[0]) + 1 :]]


@cache
def iter_to_left(square: str) -> list[str]:
    """Get board squares to the left (file a)."""
    return [f"{file}{square[1]}" for file in reversed(FILES[: FILES.index(square[0])])]


@cache
def iter_top_right_diagonal(square: str) -> list[str]:
    """Get board squares diagonally upward and to the right from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            FILES[FILES.index(square[0]) + 1 :],
            range(int(square[1]) + 1, 9),
            strict=False,
        )
    ]


@cache
def iter_bottom_left_diagonal(square: str) -> list[str]:
    """Get board squares diagonally downward and to the left from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            reversed(FILES[: FILES.index(square[0])]),
            range(int(square[1]) - 1, 0, -1),
            strict=False,
        )
    ]


@cache
def iter_top_left_diagonal(square: str) -> list[str]:
    """Get board squares diagonally upward and to the left from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            reversed(FILES[: FILES.index(square[0])]),
            range(int(square[1]) + 1, 9),
            strict=False,
        )
    ]


@cache
def iter_bottom_right_diagonal(square: str) -> list[str]:
    """Get board squares diagonally downward and to the right from square."""
    return [
        f"{file}{rank}"
        for file, rank in zip(
            FILES[FILES.index(square[0]) + 1 :],
            range(int(square[1]) - 1, 0, -1),
            strict=False,
        )
    ]


@cache
def step_up(square: str, steps: int) -> str | None:
    """Get square `steps` up from `square`."""
    return (
        f"{square[0]}{rank}"
        if (rank := int(square[1]) + steps) > 0 and rank < 9
        else None
    )


@cache
def step_down(square: str, steps: int) -> str | None:
    """Get square `steps` down from `square`."""
    return (
        f"{square[0]}{rank}"
        if (rank := int(square[1]) - steps) > 0 and rank < 9
        else None
    )


@cache
def step_right(square: str, steps: int) -> str | None:
    """Get square `steps` right from `square`."""
    return (
        f"{FILES[col_index]}{square[1]}"
        if (col_index := FILES.index(square[0]) + steps) >= 0 and col_index <= 7
        else None
    )


@cache
def step_left(square: str, steps: int) -> str | None:
    """Get square `steps` left from `square`."""
    return (
        f"{FILES[col_index]}{square[1]}"
        if (col_index := FILES.index(square[0]) - steps) >= 0 and col_index <= 7
        else None
    )


@cache
def step_diagonal_up_right(square: str, steps: int) -> str | None:
    """Step diagonally to the top and right from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_up(cursor, 1)
        if cursor is None:
            return None
        cursor = step_right(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step_diagonal_up_left(square: str, steps: int) -> str | None:
    """Step diagonally to the top and left from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_up(cursor, 1)
        if cursor is None:
            return None
        cursor = step_left(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step_diagonal_down_right(square: str, steps: int) -> str | None:
    """Step diagonally to the bottom and right from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_down(cursor, 1)
        if cursor is None:
            return None
        cursor = step_right(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step_diagonal_down_left(square: str, steps: int) -> str | None:
    """Step diagonally to the bottom and left from square."""
    cursor: str | None = square
    for _ in range(steps):
        cursor = step_down(cursor, 1)
        if cursor is None:
            return None
        cursor = step_left(cursor, 1)
        if cursor is None:
            return None
    return cursor


@cache
def step(square: str, file_offset: int = 0, rank_offset: int = 0) -> str | None:
    """Step multiple directions at once."""
    with suppress(IndexError):
        if (file_idx := FILES.index(square[0]) + file_offset) >= 0 and (
            square := f"{FILES[file_idx]}{int(square[1]) + rank_offset}"
        ) in SQUARES:
            return square
    return None


@cache
def get_squares_between(
    square_1: str, square_2: str, *, strict: bool = False
) -> list[str]:
    """
    Get the squares between two other squares on the board.

    Squares must be directly horizontal, vertical, or diagonal
    to each other.

    Raises
    ------
    ValueError - if squares are not inline.
    """
    if square_1 == square_2:
        return []
    if square_1[0] == square_2[0] and square_1[1] != square_2[1]:
        if int(square_1[1]) < int(square_2[1]):
            iterator = iter_to_top
        else:
            iterator = iter_to_bottom
    elif square_1[0] != square_2[0] and square_1[1] == square_2[1]:
        if FILES.index(square_1[0]) < FILES.index(square_2[0]):
            iterator = iter_to_right
        else:
            iterator = iter_to_left
    elif square_1[0] != square_2[0] and square_1[1] != square_2[1]:
        if int(square_1[1]) < int(square_2[1]) and FILES.index(
            square_1[0]
        ) < FILES.index(square_2[0]):
            iterator = iter_top_right_diagonal
        elif int(square_1[1]) < int(square_2[1]):
            iterator = iter_top_left_diagonal
        elif int(square_1[1]) > int(square_2[1]) and FILES.index(
            square_1[0]
        ) < FILES.index(square_2[0]):
            iterator = iter_bottom_right_diagonal
        else:
            iterator = iter_bottom_left_diagonal
    squares_between = []
    met_square_2 = False
    for sq in iterator(square_1):
        if sq == square_2:
            met_square_2 = True
            break
        squares_between.append(sq)
    if met_square_2:
        return squares_between
    else:
        if strict:
            msg = (
                "Squares must be directly diagonal, horizontal,"
                "or vertical to each other."
            )
            raise ValueError(msg)
        else:
            return []


def read_pgn_database(path: str | Path) -> list[str]:
    """Read a .pgn file to a list of PGN strings."""
    if not isinstance(path, Path):
        path = Path(path)
    with path.open() as file:
        text = file.read()
    pgns = text.split("\n\n[")
    pgns = [f"[{pgn}" for pgn in pgns if len(pgn) > 0 and pgn[0] != "["]
    return pgns


def strip_bare_moves_from_pgn(pgn: str, *, strip_numbers: bool = True) -> str:
    """Strip the SAN tokens from a PGN string."""
    pattern = (
        r"\[.+?\]|\{.+?\}|\d+\.+|[10]-[10]|\*|1/2-1/2|[?!]"
        if strip_numbers
        else r"\[.+?\]|\{.+?\}|[10]-[10]|\*|1/2-1/2|[?!]"
    )
    return re.sub(r"[\n\s]+", " ", re.sub(pattern, "", pgn)).replace("P@", "@").strip()


def get_pgn_field_by_name(pgn: str, name: str) -> str | None:
    """Get PGN field by field name and PGN text."""
    return mat.group(1) if (mat := re.search(rf"\[{name} \"(.+?)\"\]", pgn)) else None


def pgn_database_to_dicts(path: Path | str) -> list[dict[str, int | str | None]]:
    """Read a .pgn file to a list of dicts."""
    pgns = read_pgn_database(path)
    return [
        {
            "game_no": i,
            "variant": get_pgn_field_by_name(pgn, "Variant"),
            "imported_pgn": pgn,
            "imported_bare_moves": strip_bare_moves_from_pgn(pgn),
            "imported_result": get_pgn_field_by_name(pgn, "Result"),
            "imported_termination": get_pgn_field_by_name(pgn, "Termination"),
            "imported_initial_fen": get_pgn_field_by_name(pgn, "FEN"),
        }
        for i, pgn in enumerate(pgns)
    ]


@cache
def knight_navigable_squares(square: str) -> list[str]:
    """Get knight navigable squares on board."""
    knight_moves = [
        ((dir_1, step_1), (dir_2, step_2))
        for dir_1 in ("up", "down")
        for dir_2 in ("left", "right")
        for step_1, step_2 in ((1, 2), (2, 1))
    ]
    squares = []
    for (dir_1, step_1), (dir_2, step_2) in knight_moves:
        cursor: str | None = square
        assert cursor is not None
        cursor = STEP_FUNCTIONS_BY_DIRECTION[dir_1](cursor, step_1)
        if cursor is None:
            continue
        cursor = STEP_FUNCTIONS_BY_DIRECTION[dir_2](cursor, step_2)
        if cursor is None:
            continue
        squares.append(cursor)
    return squares


@cache
def king_navigable_squares(square: str) -> list[str]:
    """Get king navigable squares on board."""
    return [
        sq
        for func in STEP_FUNCTIONS_BY_DIRECTION.values()
        if (sq := func(square, 1)) is not None
    ]


DIRECTION_GENERATORS: dict[tuple[str, str], SquareGenerator] = {
    ("up", "right"): iter_top_right_diagonal,
    ("up", "inline"): iter_to_top,
    ("up", "left"): iter_top_left_diagonal,
    ("inline", "right"): iter_to_right,
    ("inline", "left"): iter_to_left,
    ("down", "right"): iter_bottom_right_diagonal,
    ("down", "inline"): iter_to_bottom,
    ("down", "left"): iter_bottom_left_diagonal,
}
STEP_FUNCTIONS_BY_DIRECTION: dict[str, StepFunction] = {
    "up": step_up,
    "right": step_right,
    "left": step_left,
    "down": step_down,
    "up_right": step_diagonal_up_right,
    "up_left": step_diagonal_up_left,
    "down_right": step_diagonal_down_right,
    "down_left": step_diagonal_down_left,
}
ROOK_GENERATORS: list[SquareGenerator] = [
    iter_to_top,
    iter_to_bottom,
    iter_to_right,
    iter_to_left,
]
BISHOP_GENERATORS: list[SquareGenerator] = [
    iter_bottom_left_diagonal,
    iter_bottom_right_diagonal,
    iter_top_left_diagonal,
    iter_top_right_diagonal,
]
QUEEN_GENERATORS: list[SquareGenerator] = ROOK_GENERATORS + BISHOP_GENERATORS
GENERATORS_BY_PIECE_TYPE: dict[PieceType, list[SquareGenerator]] = {
    "rook": ROOK_GENERATORS,
    "bishop": BISHOP_GENERATORS,
    "queen": QUEEN_GENERATORS,
}
STEP_FUNCTIONS_BY_PAWN_COLOR: dict[Color, StepFunction] = {
    "white": step_up,
    "black": step_down,
}
