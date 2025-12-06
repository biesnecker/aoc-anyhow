from collections import defaultdict
from math import prod


def calc(nums, op):
    return prod(nums) if op == "*" else sum(nums)


with open("202506.txt") as f:
    lines = [line.rstrip("\n") + " " for line in f]  # sentinel space at end

# Part 1: tokens grouped by position in split line
groups = defaultdict(list)
for line in lines:
    for i, tok in enumerate(line.split()):
        groups[i].append(tok)
print(sum(calc([int(t) for t in g[:-1]], g[-1]) for g in groups.values()))

# Part 2: read vertically by character column
nums, op, total = [], "", 0
for c in range(len(lines[0])):
    col = "".join(row[c] for row in lines)
    if "*" in col:
        op = "*"
    elif "+" in col:
        op = "+"
    digits = "".join(ch for ch in col if ch.isdigit())
    if digits:
        nums.append(int(digits))
    elif nums:
        total += calc(nums, op)
        nums, op = [], ""
print(total)
