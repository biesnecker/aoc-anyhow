import math
from collections import defaultdict

s = []

with open("201820.txt", "r") as f:
    path = f.read().strip()

visited = {(0, 0, 0)}  # (x, y, distance)

(x, y, d) = (0, 0, 0)
for c in path[1:-1]:
    if c == "N":
        y -= 1
        d += 1
        visited.add((x, y, d))
    elif c == "S":
        y += 1
        d += 1
        visited.add((x, y, d))
    elif c == "E":
        x += 1
        d += 1
        visited.add((x, y, d))
    elif c == "W":
        x -= 1
        d += 1
        visited.add((x, y, d))
    elif c == "(":
        s.append((x, y, d))
    elif c == "|":
        (x, y, d) = s[-1]
    elif c == ")":
        (x, y, d) = s.pop()

min_for_coords = defaultdict(lambda: math.inf)
for x, y, d in visited:
    min_for_coords[(x, y)] = min(min_for_coords[(x, y)], d)

print(f"Part one: {max(min_for_coords.values())}")

print(f"Part two: {len([d for d in min_for_coords.values() if d >= 1000])}")
