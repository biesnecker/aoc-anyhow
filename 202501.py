from typing import Tuple

input = []

with open("202501.txt", "r") as f:
    for line in f:
        line = line.strip()
        d = line[0]
        amt = int(line[1:])
        input.append((d, amt))


def partOne(input: list[Tuple[str, int]]) -> int:
    res = 0
    pos = 50
    for row in input:
        match row:
            case ("L", amt):
                pos = (pos - amt) % 100
            case ("R", amt):
                pos = (pos + amt) % 100
            case _:
                raise Exception(f"Invalid input: {row}")
        if pos == 0:
            res += 1
    return res


def partTwo(input: list[Tuple[str, int]]) -> int:
    res = 0
    pos = 50
    for row in input:
        match row:
            case ("L", amt):
                rots = amt // 100
                rest = amt % 100
                res += rots
                if rest >= pos and pos != 0:
                    res += 1
                pos = (pos - rest) % 100
            case ("R", amt):
                rots = amt // 100
                rest = amt % 100
                res += rots
                if rest >= (100 - pos) and pos != 0:
                    res += 1
                pos = (pos + rest) % 100
            case _:
                raise Exception(f"Invalid input: {row}")
    return res


print(partOne(input))
print(partTwo(input))
