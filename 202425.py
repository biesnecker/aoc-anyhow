from typing import List, Tuple

from utils import input_as_strings_iter

keys: List[Tuple[int, int, int, int, int]] = []
locks: List[Tuple[int, int, int, int, int]] = []

cur = [0, 0, 0, 0, 0]
is_key = False
for i, line in enumerate(input_as_strings_iter("202425.txt")):
    if i % 8 == 0:
        if line[0] == ".":
            is_key = True
    for j, c in enumerate(line):
        if c == "#":
            cur[j] += 1
    if i % 8 == 6:
        cur = tuple(map(lambda x: 0 if x == 0 else x - 1, cur))
        if is_key:
            keys.append(cur)
        else:
            locks.append(cur)
        cur = [0, 0, 0, 0, 0]
        is_key = False

part_one = sum(
    1
    for key in keys
    for lock in locks
    if all(kp + lp <= 5 for kp, lp in zip(key, lock))
)

print(f"Part one: {part_one}")
