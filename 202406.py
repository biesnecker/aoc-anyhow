from typing import Optional, Set, Tuple

from utils import Dir, coord_to_xy, input_as_strings_iter, turn_right


# Given a (start) and b (end), return the direction to move to get from a to b,
# or None if they are the same point or not on the same line. Only handles cardinal
# directions.
def inline(a: complex, b: complex) -> Optional[Dir]:
    ax, ay = coord_to_xy(a)
    bx, by = coord_to_xy(b)

    if a == b:
        return None
    elif ax == bx:
        return Dir.SOUTH if ay < by else Dir.NORTH
    elif ay == by:
        return Dir.EAST if ax < bx else Dir.WEST
    else:
        return None


grid = {}
startpos = pos = 0
d = Dir.NORTH
for y, line in enumerate(input_as_strings_iter("202406.txt")):
    for x, c in enumerate(line):
        coord = x + (1j * y)
        if c == "#":
            grid[coord] = True
        elif c == "^":
            pos = coord
            startpos = coord
            grid[coord] = False
        elif c == ".":
            grid[coord] = False
        else:
            raise Exception(f"Unknown char {c}")

# visited: DefaultDict[complex, Set[Dir]] = defaultdict(set)
visited: Set[Tuple[complex, Dir]] = set()
visited.add((startpos, Dir.NORTH))
obstacles: Set[complex] = set()
while True:
    np = pos + d.value
    if np not in grid:
        break
    if grid[np]:
        # obstacle
        d = turn_right(d)
    else:
        # We want to see if we added an obstacle at np, which would force us to turn right, would we end up in a position and direction that we've been in before?
        if np != startpos and np not in obstacles:
            nd = turn_right(d)
            for v in (v for v, d in visited if d == nd and inline(pos, v) == nd):
                obstacles.add(np)
        pos = np
        visited.add((pos, d))

# assert len(visited) == 5444  # so I don't fuck it up during part 2
unique_visited = {p for p, _ in visited}
print(f"Part one: {len(unique_visited)}")
print(f"Part two: {len(obstacles)}")
