from utils import input_as_numbers, window
from itertools import pairwise
from collections import Counter

codes = input_as_numbers("202422.txt")


def step(code: int) -> int:
    code ^= code << 6
    code %= 16777216
    code ^= code >> 5
    code %= 16777216
    code ^= code << 11
    return code % 16777216


def codes_from_seed(code: int, steps=2000) -> int:
    codes = [code]
    for _ in range(steps):
        code = step(code)
        codes.append(code)
    return codes


def prices(codes: list[int]) -> list[int]:
    return [c % 10 for c in codes]


def diffs(codes: list[int]) -> list[int]:
    return [b - a for a, b in pairwise(codes)]


codes = [1, 10, 100, 2024]

part_one = 0
part_two = 0
c = Counter()
for code in codes:
    cfs = codes_from_seed(code, steps=2000)
    part_one += cfs[-1]
    p = prices(cfs)
    d = diffs(p)
    distinct = set()
    for g in window(d, 4):
        distinct.add(tuple(g))
    for x in distinct:
        c[x] += 1
print(f"Part one: {part_one}")
print(c.most_common(3))
