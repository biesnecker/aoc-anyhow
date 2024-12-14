from utils import input_as_strings_iter
from typing import List, Tuple
import re
import statistics

type Input = List[List[Tuple[int, int]]]

input: Input = []
for line in input_as_strings_iter("202414.txt"):
    matches = re.match(r"p=(-?\d+),(-?\d+) v=(-?\d+),(-?\d+)", line)
    input.append(
        [
            (int(matches.group(1)), int(matches.group(2))),
            (int(matches.group(3)), int(matches.group(4))),
        ]
    )


def score(input: Input, width: int, height: int, step: int) -> int:
    quads = [0, 0, 0, 0]
    for [(px, py), (vx, vy)] in input:
        nx = (px + vx * step) % width
        ny = (py + vy * step) % height
        if nx == width // 2:
            continue
        if ny == height // 2:
            continue
        if nx < width // 2:
            quads[0 + (ny < height // 2)] += 1
        else:
            quads[2 + (ny < height // 2)] += 1

    return quads[0] * quads[1] * quads[2] * quads[3]


print(f"Part one: {score(input, 101, 103, 100)}")


def find_min_variance(input: Input, width: int, height: int) -> Tuple[int, int]:
    min_x_variance = float("inf")
    min_x_step = 0
    min_y_variance = float("inf")
    min_y_step = 0
    for step in range(width):
        xs = [(px + vx * step) % width for [(px, _), (vx, _)] in input]
        xvar = statistics.variance(xs)
        if xvar < min_x_variance:
            min_x_variance = xvar
            min_x_step = step
    for step in range(height):
        ys = [(py + vy * step) % height for [(_, py), (_, vy)] in input]
        yvar = statistics.variance(ys)
        if yvar < min_y_variance:
            min_y_variance = yvar
            min_y_step = step
    return (min_x_step, min_y_step)


def display(input: Input, width: int, height: int, step: int) -> None:
    grid = [["." for _ in range(width)] for _ in range(height)]
    for [(px, py), (vx, vy)] in input:
        nx = (px + vx * step) % width
        ny = (py + vy * step) % height
        grid[ny][nx] = "#"
    for row in grid:
        print("".join(row))


x, y = find_min_variance(input, 101, 103)
part_two = 101 * (51 * (y - x) % 103) + x
display(input, 101, 103, part_two)
print(f"Part two: {part_two}")
