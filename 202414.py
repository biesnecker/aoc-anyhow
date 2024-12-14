from utils import input_as_strings_iter
from typing import List, Tuple
import re

type Input = List[List[Tuple[int, int]]]

input: Input = []
for line in input_as_strings_iter("202414.txt"):
    # p=65,86 v=-38,-3
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


def display(input: Input, width: int, height: int, step: int) -> None:
    grid = [["." for _ in range(width)] for _ in range(height)]
    for [(px, py), (vx, vy)] in input:
        nx = (px + vx * step) % width
        ny = (py + vy * step) % height
        grid[ny][nx] = "#"
    for row in grid:
        print("".join(row))


min_score = float("inf")
min_score_step = 0
for step in range(8000):
    s = score(input, 101, 103, step)
    if s < min_score:
        min_score = s
        min_score_step = step

display(input, 101, 103, min_score_step)
print(f"Part two: {min_score_step}")
