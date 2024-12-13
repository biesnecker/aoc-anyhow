import re
from itertools import groupby
from typing import List, Tuple

from utils import input_as_strings_iter


def solve(px: int, py: int, ax: int, ay: int, bx: int, by: int) -> int:
    det = ax * by - ay * bx
    if det == 0:
        return 0

    a = px * by - py * bx
    b = py * ax - px * ay

    # is there an integer solution?
    if a % det != 0 or b % det != 0:
        return 0

    a = a // det
    b = b // det

    # only non-negative solutions make sense
    if a >= 0 and b >= 0:
        return 3 * a + b

    return 0


input = []
for key, group in groupby(input_as_strings_iter("202413.txt"), lambda x: x != ""):
    if not key:
        continue
    res = []
    for s in group:
        a = re.match(r".+: X[+=](\d+), Y[+=](\d+)", s)
        assert a is not None
        ax = int(a.group(1))
        ay = int(a.group(2))
        res.append((ax, ay))
    assert len(res) == 3
    input.append(res)


part_one = 0
part_two = 0
for [(ax, ay), (bx, by), (px, py)] in input:
    part_one += solve(px, py, ax, ay, bx, by)
    part_two += solve(px + 10000000000000, py + 10000000000000, ax, ay, bx, by)
print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
