from enum import Enum
from typing import Iterator, List, Tuple


def input_as_string(filename):
    with open(filename, "r") as f:
        return f.read().strip()


def input_as_strings_iter(filename):
    with open(filename, "r") as f:
        for line in f:
            yield line.strip()


def input_as_strings(filename):
    return list(input_as_strings_iter(filename))


def input_as_numbers_iter(filename):
    with open(filename, "r") as f:
        for line in f:
            yield int(line.strip())


def input_as_numbers(filename):
    return list(input_as_numbers_iter(filename))


def input_as_list_of_numbers_iter(filename, split_on=None):
    with open(filename, "r") as f:
        for line in f:
            yield list(map(lambda v: int(v.strip()), line.strip().split(split_on)))


def input_as_list_of_numbers(filename, split_on=None):
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


def get_neighbors_sides(pos: complex) -> Iterator[Tuple[Dir, complex]]:
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
    for d in get_neighbors_sides(pos):
        yield d
    for d in get_neighbors_diagonal(pos):
        yield d
