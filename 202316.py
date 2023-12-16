from collections import deque
from enum import IntEnum

with open("202316.txt", "r") as f:
    grid = [[c for c in line.strip()] for line in f]


class Direction(IntEnum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3


max_x = len(grid[0])
max_y = len(grid)


def delta(d):
    match d:
        case Direction.UP:
            return (0, -1)
        case Direction.DOWN:
            return (0, 1)
        case Direction.LEFT:
            return (-1, 0)
        case Direction.RIGHT:
            return (1, 0)
        case _:
            raise ValueError(f"Invalid direction: {d}")


def run_beam(grid, x, y, d):
    energized = set()
    seen = set()
    q = deque([(x, y, d)])

    while q:
        x, y, d = q.popleft()
        dx, dy = delta(d)
        # Find the next non-empty cell in the current direction.
        fell_off = False
        while True:
            x += dx
            y += dy

            if x < 0 or x >= max_x or y < 0 or y >= max_y:
                fell_off = True
                break

            energized.add((x, y))
            if grid[y][x] == "|" and d in (Direction.UP, Direction.DOWN):
                continue
            elif grid[y][x] == "-" and d in (Direction.LEFT, Direction.RIGHT):
                continue
            elif grid[y][x] != ".":
                break
        if fell_off:
            continue
        new_beams = []
        match (grid[y][x], d):
            case ("/", Direction.UP):
                new_beams.append((x, y, Direction.RIGHT))
            case ("/", Direction.DOWN):
                new_beams.append((x, y, Direction.LEFT))
            case ("/", Direction.LEFT):
                new_beams.append((x, y, Direction.DOWN))
            case ("/", Direction.RIGHT):
                new_beams.append((x, y, Direction.UP))
            case ("\\", Direction.UP):
                new_beams.append((x, y, Direction.LEFT))
            case ("\\", Direction.DOWN):
                new_beams.append((x, y, Direction.RIGHT))
            case ("\\", Direction.LEFT):
                new_beams.append((x, y, Direction.UP))
            case ("\\", Direction.RIGHT):
                new_beams.append((x, y, Direction.DOWN))
            case ("|", Direction.LEFT) | ("|", Direction.RIGHT):
                new_beams.append((x, y, Direction.UP))
                new_beams.append((x, y, Direction.DOWN))
            case ("-", Direction.UP) | ("-", Direction.DOWN):
                new_beams.append((x, y, Direction.LEFT))
                new_beams.append((x, y, Direction.RIGHT))
                pass
            case tile:
                raise ValueError(f"Unexpected: {tile, x, y, d}")
        for nx, ny, nd in new_beams:
            if (nx, ny, nd) not in seen:
                q.append((nx, ny, nd))
                seen.add((nx, ny, nd))
    return len(energized)


print(f"Part one: {run_beam(grid, -1, 0, Direction.RIGHT)}")

part_two = 0
for y in range(max_y):
    part_two = max(part_two, run_beam(grid, -1, y, Direction.RIGHT))
    part_two = max(part_two, run_beam(grid, max_x, y, Direction.LEFT))
for x in range(max_x):
    part_two = max(part_two, run_beam(grid, x, -1, Direction.DOWN))
    part_two = max(part_two, run_beam(grid, x, max_y, Direction.UP))
print(f"Part two: {part_two}")
