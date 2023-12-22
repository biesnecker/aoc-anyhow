from collections import deque
from grid import grid_wh

grid = set()
sx, sy = None, None
with open("202321.txt", "r") as f:
    for y, line in enumerate(f):
        for x, c in enumerate(line.strip()):
            if c == ".":
                grid.add((x, y))
            elif c == "S":
                grid.add((x, y))
                sx, sy = x, y
assert sx is not None and sy is not None


def reachable(grid, start, max_steps):
    grid_width, grid_height = grid_wh(grid)
    q = deque([(start, 0)])
    visited = {}
    while q:
        (x, y), steps = q.popleft()
        if (x, y) in visited:
            continue
        visited[(x, y)] = steps
        assert steps < max_steps + 1
        if steps == max_steps:
            continue
        for dx, dy in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            nx, ny = x + dx, y + dy
            ex, ey = nx % grid_width, ny % grid_height
            if (ex, ey) in grid:
                q.append(((nx, ny), steps + 1))
    return visited


def reachable_in(rm, s):
    return len([k for k, v in rm.items() if v <= s and v % 2 == s % 2])


def part_one(grid):
    rm = reachable(grid, (sx, sy), 64)
    return reachable_in(rm, 64)


def part_two(grid):
    steps = 26501365
    grid_width, _ = grid_wh(grid)
    r0 = steps % grid_width
    r1 = r0 + grid_width
    r2 = r0 + 2 * grid_width
    rm = reachable(grid, (sx, sy), r2)

    s0 = reachable_in(rm, r0)
    s1 = reachable_in(rm, r1)
    s2 = reachable_in(rm, r2)

    # Make a quadratic equation out of this:
    a = (s0 - 2 * s1 + s2) // 2
    b = (-3 * s0 + 4 * s1 - s2) // 2
    c = s0
    n = steps // grid_width
    # print(f"Equation: {a}n^2 + {b}n + {c} where n = {n}")
    return a * n * n + b * n + c


print(f"Part one: {part_one(grid)}")
print(f"Part two: {part_two(grid)}")
