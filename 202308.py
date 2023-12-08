import math

paths = {}

with open("202308.txt", "r") as f:
    for i, line in enumerate(f):
        if i == 0:
            dirs = line.strip()
        elif i == 1:
            continue
        else:
            [a, b, c, d, e, f, g, h, i] = [x for x in line.strip() if x.isalpha()]
            paths["".join([a, b, c])] = ("".join([d, e, f]), "".join([g, h, i]))

idx = 0
steps = 0
cur = "AAA"
while True:
    if cur == "ZZZ":
        print(f"Part one: {steps}")
        break
    (left, right) = paths[cur]
    if dirs[idx] == "L":
        cur = left
    elif dirs[idx] == "R":
        cur = right
    else:
        raise ValueError(f"Invalid direction: {dirs[idx]}")
    idx = (idx + 1) % len(dirs)
    steps += 1


def cycle_length(starting):
    idx = 0
    steps = 0
    cur = starting
    while True:
        if cur.endswith("Z"):
            return steps
        (left, right) = paths[cur]
        if dirs[idx] == "L":
            cur = left
        elif dirs[idx] == "R":
            cur = right
        else:
            raise ValueError(f"Invalid direction: {dirs[idx]}")
        idx = (idx + 1) % len(dirs)
        steps += 1


cycles = {n: cycle_length(n) for n in paths if n.endswith("A")}
assert all(n % len(dirs) == 0 for n in cycles.values())
part_two = math.lcm(*cycles.values())
print(f"Part two: {part_two}")
