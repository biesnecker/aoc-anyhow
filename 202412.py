from collections import deque
from typing import Set

from utils import (
    get_neighbors_cardinal,
    input_as_strings_iter,
    move_east,
    move_north,
    move_northeast,
    move_northwest,
    move_south,
    move_southwest,
    move_west,
    xy_to_coord,
)

grid = {}
max_x = max_y = 0
for y, line in enumerate(input_as_strings_iter("202412.txt")):
    for x, c in enumerate(line):
        grid[xy_to_coord(x, y)] = c
        max_x = max(max_x, x)
        max_y = max(max_y, y)
regions = []
global_seen = set()


def perimeter(region: Set[complex]) -> int:
    perimeter = 0
    for pos in region:
        p = 4
        for _, npos in get_neighbors_cardinal(pos):
            if npos in region:
                p -= 1
        perimeter += p
    return perimeter


def shared_sides(region: Set[complex]) -> int:
    sides = 0
    for c in region:
        if move_west(c) in region:
            if move_north(c) not in region and move_northwest(c) not in region:
                sides += 1
            if move_south(c) not in region and move_southwest(c) not in region:
                sides += 1
        if move_north(c) in region:
            if move_west(c) not in region and move_northwest(c) not in region:
                sides += 1
            if move_east(c) not in region and move_northeast(c) not in region:
                sides += 1
    return sides


# first, let's find all of the regions
for x in range(max_x + 1):
    for y in range(max_y + 1):
        c = xy_to_coord(x, y)
        if c in global_seen:
            continue

        region_seen = set([c])
        q = deque([c])
        while q:
            pos = q.popleft()
            for _, d in get_neighbors_cardinal(pos):
                if d not in region_seen and grid.get(d) == grid[pos]:
                    assert d not in global_seen
                    region_seen.add(d)
                    q.append(d)
        # We have the whole region, append it.
        regions.append(region_seen)
        # Add the whole region to the global seen set.
        global_seen |= region_seen

part_one = 0
part_two = 0
for r in regions:
    p = perimeter(r)
    s = shared_sides(r)
    a = len(r)
    part_one += a * p
    part_two += a * (p - s)

print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
