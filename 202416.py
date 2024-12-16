from utils import (
    input_as_strings_iter,
    Dir,
    xy_to_coord,
    coord_to_xy,
    move,
    turn_left,
    turn_right,
)
from typing import Dict, List, Tuple, Set

grid: Set[complex] = set()
start_pos = 0
target_pos = 0
for y, line in enumerate(input_as_strings_iter("202416.txt")):
    for x, c in enumerate(line):
        match c:
            case ".":
                grid.add(xy_to_coord(x, y))
            case "S":
                coord = xy_to_coord(x, y)
                start_pos = coord
                grid.add(coord)
            case "E":
                coord = xy_to_coord(x, y)
                target_pos = coord
                grid.add(coord)
            case _:
                pass


def solve():
    best = float("inf")
    best_square: Dict[Tuple[complex, Dir], int] = {}
    best_paths: Set[complex] = set()

    def better(pos: complex, d: Dir, cost: int) -> bool:
        return best_square.get((pos, d), float("inf")) >= cost

    s = [(start_pos, Dir.EAST, 0, [start_pos])]
    while s:
        pos, d, cost, p = s.pop()
        if pos == target_pos:
            if cost < best:
                best = cost
                best_paths = set(p)
            elif cost == best:
                best_paths.update(p)
            continue
        elif cost >= best:
            # Don't bother exploring this path if we've found a cheaper one already
            continue

        # Is the square to our left open?
        if move(pos, turn_left(d)) in grid and better(pos, turn_left(d), cost + 1000):
            s.append((pos, turn_left(d), cost + 1000, p))
            best_square[(pos, turn_left(d))] = cost + 1000

        # Is the square to our right open?
        if move(pos, turn_right(d)) in grid and better(pos, turn_right(d), cost + 1000):
            s.append((pos, turn_right(d), cost + 1000, p))
            best_square[(pos, turn_right(d))] = cost + 1000

        # Can we continue straight?
        forward = move(pos, d)
        if forward in grid and better(forward, d, cost + 1):
            np = p.copy()
            np.append(forward)
            s.append((forward, d, cost + 1, np))
            best_square[(forward, d)] = cost + 1

    print("Part one:", best)
    print("Part two:", len(best_paths))


solve()
