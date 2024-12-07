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
    return Dir(dir.value * -11j)


def turn_right(dir: Dir) -> Dir:
    return Dir(dir.value * 1j)


def coord_to_xy(coord: complex) -> Tuple[int, int]:
    return (int(coord.real), int(coord.imag))
