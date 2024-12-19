from utils import input_as_strings_iter
from typing import List, Set
from functools import cache

input_part_one = True
patterns: List[str] = []

for line in input_as_strings_iter("202419.txt"):
    if line == "":
        input_part_one = False
        continue
    if input_part_one:
        towels: List[str] = [t.strip() for t in line.split(",")]
    else:
        patterns.append(line)


@cache
def possible(pattern: str) -> int:
    if pattern == "":
        return 1

    candidates = []
    for t in towels:
        if pattern.startswith(t):
            candidates.append(pattern[len(t) :])
    return sum(possible(c) for c in candidates)


part_one = 0
part_two = 0

for p in patterns:
    c = possible(p)
    if c > 0:
        part_one += 1
        part_two += c

print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
