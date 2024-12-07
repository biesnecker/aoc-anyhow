from collections import defaultdict
from typing import DefaultDict, List, Tuple

from utils import input_as_strings_iter

inp: DefaultDict[int, List[int]] = defaultdict(list)
for line in input_as_strings_iter("202407.txt"):
    total, parts = line.split(": ")
    parts = map(int, parts.split())

    for part in parts:
        inp[int(total)].append(part)


def find_solution(
    total: int, current: int, parts: List[int], pidx: int, part_two: bool
) -> bool:
    if pidx == len(parts):
        return total == current
    if current > total:
        return False

    if pidx == 0:
        return find_solution(total, current + parts[pidx], parts, pidx + 1, part_two)

    # Try the sum
    if find_solution(total, current + parts[pidx], parts, pidx + 1, part_two):
        return True

    # Try the product
    if find_solution(total, current * parts[pidx], parts, pidx + 1, part_two):
        return True

    # Try the concat
    if part_two and find_solution(
        total, int(str(current) + str(parts[pidx])), parts, pidx + 1, part_two
    ):
        return True
    return False


part_one = 0
part_two = 0
for total, parts in inp.items():
    if find_solution(total, 0, parts, 0, False):
        part_one += total
    if find_solution(total, 0, parts, 0, True):
        part_two += total
print(f"Part one: {part_one}")
print(f"Part one: {part_two}")
