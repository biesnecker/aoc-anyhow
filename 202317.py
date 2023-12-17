from enum import IntEnum
import heapq
import math

with open("202317.txt", "r") as f:
    grid = [[int(c) for c in line.strip()] for line in f]


class Direction(IntEnum):
    UP = 0
    LEFT = 1
    DOWN = 2
    RIGHT = 3


def options(d, steps, max_steps_per_direction=3, min_steps_before_turn=0):
    match d:
        case Direction.UP | Direction.DOWN:
            if steps >= min_steps_before_turn:
                yield Direction.LEFT
                yield Direction.RIGHT
        case Direction.LEFT | Direction.RIGHT:
            if steps >= min_steps_before_turn:
                yield Direction.UP
                yield Direction.DOWN
        case _:
            raise ValueError(f"Invalid direction: {d}")
    if steps < max_steps_per_direction:
        yield d  # can still go straight ahead.


def min_path(grid, max_steps_per_direction=3, min_steps_before_turn=0):
    x, y = 0, 0
    s = [(0, x, y, Direction.RIGHT, 0)]
    visited = {}
    min_heat_loss = math.inf
    while s:
        heat_loss, x, y, d, steps = heapq.heappop(s)
        if (
            x == len(grid[0]) - 1
            and y == len(grid) - 1
            and steps >= min_steps_before_turn
        ):
            # Reached the target.
            min_heat_loss = min(min_heat_loss, heat_loss)
            continue
        if heat_loss >= min_heat_loss:
            continue
        if (key := (x, y, d, steps)) in visited and visited[key] <= heat_loss:
            continue
        visited[key] = heat_loss
        for nd in options(d, steps, max_steps_per_direction, min_steps_before_turn):
            dx, dy = [(0, -1), (-1, 0), (0, 1), (1, 0)][nd]
            nx, ny = x + dx, y + dy
            if nx < 0 or nx >= len(grid[0]) or ny < 0 or ny >= len(grid):
                continue
            n_heat_loss = heat_loss + grid[ny][nx]
            if n_heat_loss >= min_heat_loss:
                continue
            heapq.heappush(
                s,
                (
                    n_heat_loss,
                    nx,
                    ny,
                    nd,
                    steps + 1 if d == nd else 1,
                ),
            )
    return min_heat_loss


print(f"Part one: {min_path(grid)}")
print(f"Part one: {min_path(grid, 10, 4)}")
