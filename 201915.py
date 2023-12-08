from intcode import Intcode, intcode_from_file, OutputInterrupt, InputInterrupt
from collections import defaultdict, deque
from copy import copy
from enum import IntEnum
import math


class Tile(IntEnum):
    WALL = 0
    EMPTY = 1
    OXYGEN = 2


class Directon(IntEnum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4


def explore_grid():
    oxygen = None
    droid = intcode_from_file("201915.txt")
    grid = {(0, 0): Tile.EMPTY}
    x, y = 0, 0
    s = deque([(x, y, droid)])
    while s:
        (x, y, d) = s.popleft()
        for direction in Directon:
            dx, dy = 0, 0
            match direction:
                case Directon.NORTH:
                    dx, dy = 0, 1
                case Directon.SOUTH:
                    dx, dy = 0, -1
                case Directon.WEST:
                    dx, dy = -1, 0
                case Directon.EAST:
                    dx, dy = 1, 0
            if (x + dx, y + dy) not in grid:
                droid = copy(d)
                droid.append_input(direction)
                try:
                    droid.run()
                except OutputInterrupt:
                    tile = droid.pop_output()
                    grid[(x + dx, y + dy)] = Tile(tile)
                    if tile != Tile.WALL:
                        s.append((x + dx, y + dy, droid))
                        if tile == Tile.OXYGEN:
                            oxygen = (x + dx, y + dy)
                            break
    return (grid, oxygen)


grid, oxygen = explore_grid()
part_one = 0
q = deque([(0, 0, 0)])
visited = {(0, 0)}
while q:
    (x, y, steps) = q.popleft()
    if (x, y) == oxygen:
        print(f"Part one: {steps}")
        break
    for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
        if (x + dx, y + dy) not in visited:
            visited.add((x + dx, y + dy))
            if grid[(x + dx, y + dy)] != Tile.WALL:
                q.append((x + dx, y + dy, steps + 1))

part_two = 0
q = deque([(*oxygen, 0)])
visited = {oxygen}
while q:
    (x, y, steps) = q.popleft()
    part_two = max(part_two, steps)
    for dx, dy in ((0, 1), (0, -1), (-1, 0), (1, 0)):
        if (x + dx, y + dy) not in visited:
            visited.add((x + dx, y + dy))
            if grid[(x + dx, y + dy)] != Tile.WALL:
                q.append((x + dx, y + dy, steps + 1))
print(f"Part two: {part_two}")
