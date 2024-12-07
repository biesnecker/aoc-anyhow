import math
from collections import defaultdict
from typing import DefaultDict, List, Tuple

from utils import input_as_strings_iter

inp: DefaultDict[int, List[int]] = defaultdict(list)
for line in input_as_strings_iter("202407.txt"):
    total, parts = line.split(": ")
    parts = map(int, parts.split())

    for part in parts:
        inp[int(total)].append(part)


def find_solution_backwards(total: int, parts: List[int]) -> Tuple[bool, bool]:
    s: List[Tuple[int, int, bool]] = [(total, len(parts) - 1, False)]

    found_one = False
    found_two = False

    while s:
        current, pidx, used_two = s.pop()

        assert pidx >= 0

        if pidx == 0:
            if current == parts[pidx]:
                if used_two:
                    found_two = True
                else:
                    # Part one solutions work for both
                    found_one = True
                    found_two = True
                if found_one and found_two:
                    # short-circuit
                    return (True, True)
            continue

        if current % parts[pidx] == 0:
            # We can divide
            s.append((current // parts[pidx], pidx - 1, used_two))
        if current - parts[pidx] >= 0:
            # We can subtract
            s.append((current - parts[pidx], pidx - 1, used_two))

        c = str(current)
        p = str(parts[pidx])
        if c.endswith(p) and len(c) > len(p):
            # We can de-concat
            s.append((int(c.removesuffix(p)), pidx - 1, True))

    return (found_one, found_two)


part_one = 0
part_two = 0
for total, parts in inp.items():
    one, two = find_solution_backwards(total, parts)
    if one:
        part_one += total
        part_two += total
    elif two:
        part_two += total
print(f"Part one: {part_one}")
print(f"Part one: {part_two}")
