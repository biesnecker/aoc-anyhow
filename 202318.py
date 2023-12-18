from enum import IntEnum


class Direction(IntEnum):
    RIGHT = 0
    DOWN = 1
    LEFT = 2
    UP = 3


with open("202318.txt", "r") as f:
    m = {
        "U": Direction.UP,
        "D": Direction.DOWN,
        "L": Direction.LEFT,
        "R": Direction.RIGHT,
    }
    instrs = [
        (m[a], int(b), (int(c[-2]), int(c[2:-2], 16)))
        for line in f
        if (parts := line.strip().split()) and len(parts) == 3
        for [a, b, c] in [parts]
    ]


# Pick's theorem:
# A = i + b / 2 - 1
# A is the area
# i is the number of internal points
# b is the number of boundary points
# https://en.wikipedia.org/wiki/Pick%27s_theorem
#
# Use the Shoelace formula to calculate the area of a polygon:
# https://en.wikipedia.org/wiki/Shoelace_formula
def area(instrs):
    vertices = []
    perimeter = 0
    x, y = 0, 0
    for d, n in instrs:
        dx, dy = [(1, 0), (0, 1), (-1, 0), (0, -1)][d]
        x += dx * n
        y += dy * n
        perimeter += n
        vertices.append((x, y))

    x, y = zip(*vertices)
    shoelace = 0.5 * abs(
        sum(x[i] * y[i - 1] - x[i - 1] * y[i] for i in range(len(vertices)))
    )
    return int(shoelace + perimeter / 2 + 1)


part_one = area([(a, b) for (a, b, _) in instrs])
print(f"Part one: {part_one}")

part_two = area([i for _, _, i in instrs])
print(f"Part two: {part_two}")
