from utils import (
    input_as_strings_iter,
    coord_to_xy,
    xy_to_coord,
    get_neighbors_cardinal,
    manhattan_distance,
)
from typing import Set, List, Deque, Dict
from collections import deque

grid: Set[complex] = set()
start_pos: complex = 0
end_pos: complex = 0
max_x = max_y = 0
for y, line in enumerate(input_as_strings_iter("202420.txt")):
    max_y = max(y, max_y)
    for x, c in enumerate(line):
        max_x = max(x, max_x)
        if c == "#":
            grid.add(xy_to_coord(x, y))
        elif c == "S":
            start_pos = xy_to_coord(x, y)
        elif c == "E":
            end_pos = xy_to_coord(x, y)
assert start_pos != 0 and end_pos != 0


def calculate_shortest(
    grid: Set[complex], start: complex
) -> Dict[complex, List[complex]]:
    shortest = {start: [start]}
    q: Deque[complex] = deque([start])
    visited: Set[complex] = set([start])

    while q:
        pos = q.popleft()
        for _, npos in get_neighbors_cardinal(pos):
            if npos in visited or npos in grid:
                continue
            visited.add(npos)
            npath = shortest[pos].copy()
            npath.append(npos)
            shortest[npos] = npath
            q.append(npos)
    return shortest


shortest_paths = calculate_shortest(grid, end_pos)
fair_path = shortest_paths[start_pos]
fair_path = list(reversed(fair_path))

# Now we just need the lengths
shortest_paths = {k: len(v) for k, v in shortest_paths.items()}


def solve(path: List[complex], radius: int) -> int:
    res = 0
    path_distance = len(path)
    for step, pos in enumerate(path):
        remaining = path_distance - step
        x, y = coord_to_xy(pos)
        for ny in range(y - radius, y + radius + 1):
            max_offset = radius - abs(y - ny)
            for nx in range(x - max_offset, x + max_offset + 1):
                npos = xy_to_coord(nx, ny)
                dist = manhattan_distance(npos, pos)
                if npos in shortest_paths and shortest_paths[npos] < remaining - dist:
                    diff = remaining - shortest_paths[npos] - dist
                    if diff >= 100:
                        res += 1
    return res


print(f"Part one: {solve(fair_path, 2)}")
print(f"Part two: {solve(fair_path, 20)}")
