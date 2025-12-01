from typing import Tuple

input = []

with open("202501.txt", "r") as f:
    for line in f:
        line = line.strip()
        d = line[0]
        amt = int(line[1:])
        input.append((d, amt))

# Takes the input and the start position and returns the end position
# and the number of full rotations
def rotate(row: Tuple[str, int], pos: int) -> Tuple[int, int]:
    (d, amt) = row
    rots = amt // 100
    rest = amt % 100
    if d == "L":
        if rest >= pos and pos != 0:
            rots += 1
        pos = (pos - rest) % 100
    else:
        if rest >= (100 - pos) and pos != 0:
            rots += 1
        pos = (pos + rest) % 100
    return (pos, rots)


def partOne(input: list[Tuple[str, int]]) -> int:
    res = 0
    pos = 50
    for row in input:
        pos = rotate(row, pos)[0]
        if pos == 0:
            res += 1
    return res


def partTwo(input: list[Tuple[str, int]]) -> int:
    res = 0
    pos = 50
    for row in input:
        pos, rots = rotate(row, pos)
        res += rots
    return res


print(partOne(input))
print(partTwo(input))
