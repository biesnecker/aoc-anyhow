from enum import Enum
from typing import Iterator, List, Optional, Tuple


def input_as_string(filename: str) -> str:
    with open(filename, "r") as f:
        return f.read().strip()


def input_as_strings_iter(filename: str) -> Iterator[str]:
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


def input_as_strings(filename: str) -> List[str]:
    return list(input_as_strings_iter(filename))


def input_as_numbers_iter(filename: str) -> Iterator[int]:
    with open(filename, "r") as f:
        for line in f:
            yield int(line.strip())


def input_as_numbers(filename: str) -> List[int]:
    return list(input_as_numbers_iter(filename))


def input_as_list_of_numbers_iter(
    filename: str, split_on: Optional[str] = None
) -> Iterator[List[int]]:
    with open(filename, "r") as f:
        for line in f:
            yield list(map(lambda v: int(v.strip()), line.strip().split(split_on)))


def input_as_list_of_numbers(
    filename: str, split_on: Optional[str] = None
) -> List[List[int]]:
    return list(input_as_list_of_numbers_iter(filename, split_on))


class Dir(Enum):
    NORTH = -1j
    SOUTH = 1j
    WEST = -1
    EAST = 1
    NORTHEAST = 1 - 1j
    NORTHWEST = -1 - 1j
    SOUTHEAST = 1 + 1j
    SOUTHWEST = -1 + 1j


def get_neighbors_cardinal(pos: complex) -> Iterator[Tuple[Dir, complex]]:
    yield (Dir.NORTH, pos + Dir.NORTH.value)
    yield (Dir.SOUTH, pos + Dir.SOUTH.value)
    yield (Dir.WEST, pos + Dir.WEST.value)
    yield (Dir.EAST, pos + Dir.EAST.value)


def get_neighbors_diagonal(pos: complex) -> Iterator[Tuple[Dir, complex]]:
    yield (Dir.NORTHEAST, pos + Dir.NORTHEAST.value)
    yield (Dir.NORTHWEST, pos + Dir.NORTHWEST.value)
    yield (Dir.SOUTHEAST, pos + Dir.SOUTHEAST.value)
    yield (Dir.SOUTHWEST, pos + Dir.SOUTHWEST.value)


def get_neighbors_all(pos: complex) -> Iterator[Tuple[Dir, complex]]:
    for d in get_neighbors_cardinal(pos):
        yield d
    for d in get_neighbors_diagonal(pos):
        yield d


def turn_left(dir: Dir) -> Dir:
    return Dir(dir.value * -1j)


def turn_right(dir: Dir) -> Dir:
    return Dir(dir.value * 1j)


def move(pos: complex, dir: Dir) -> complex:
    return pos + dir.value


def move_north(pos: complex) -> complex:
    return pos + Dir.NORTH.value


def move_south(pos: complex) -> complex:
    return pos + Dir.SOUTH.value


def move_east(pos: complex) -> complex:
    return pos + Dir.EAST.value


def move_west(pos: complex) -> complex:
    return pos + Dir.WEST.value


def move_northeast(pos: complex) -> complex:
    return pos + Dir.NORTHEAST.value


def move_northwest(pos: complex) -> complex:
    return pos + Dir.NORTHWEST.value


def move_southeast(pos: complex) -> complex:
    return pos + Dir.SOUTHEAST.value


def move_southwest(pos: complex) -> complex:
    return pos + Dir.SOUTHWEST.value


def coord_to_xy(coord: complex) -> Tuple[int, int]:
    return (int(coord.real), int(coord.imag))


def xy_to_coord(x: int, y: int) -> complex:
    return x + y * 1j


def coord_in_bounds(c: complex, x_range: range, y_range: range) -> bool:
    return int(c.real) in x_range and int(c.imag) in y_range


def manhattan_distance(a: complex, b: complex) -> int:
    return abs(int(a.real) - int(b.real)) + abs(int(a.imag) - int(b.imag))
