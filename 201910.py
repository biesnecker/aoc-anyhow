import math
from collections import defaultdict

with open("201910.txt", "r") as f:
    asteroids = {
        (x, y) for y, line in enumerate(f) for x, c in enumerate(line) if c == "#"
    }


def angle(start, end):
    result = math.atan2(end[0] - start[0], start[1] - end[1]) * 180 / math.pi
    if result < 0:
        return 360 + result
    return result


def visible(x, y):
    slopes = set()
    visible = set()
    for ox, oy in asteroids:
        if ox == x and oy == y:
            continue
        dx, dy = ox - x, oy - y
        gcd = math.gcd(dx, dy)
        if (slope := (dx // gcd, dy // gcd)) not in slopes:
            slopes.add(slope)
            visible.add((ox, oy))
    return visible


part_one = 0
bestx, besty = None, None
for x, y in asteroids:
    slopes = set()
    for ox, oy in asteroids:
        if ox == x and oy == y:
            continue
        dx, dy = ox - x, oy - y
        gcd = math.gcd(dx, dy)
        slopes.add((dx // gcd, dy // gcd))
    if len(slopes) > part_one:
        part_one = len(slopes)
        bestx, besty = x, y
print(f"Part one: {part_one}")
assert bestx is not None and besty is not None

part_two = 0
asteroids.remove((bestx, besty))  # remove the monitoring station

# part 2
angles = sorted(
    ((angle((bestx, besty), end), end) for end in asteroids),
    key=lambda x: (x[0], abs(bestx - x[1][0]) + abs(besty - x[1][1])),
)

last_angle = None
idx = 0
cnt = 0
solution = None
while cnt < 200:
    if not angles:
        break
    if idx >= len(angles):
        idx = 0
        last_angle = None
    if last_angle == angles[idx][0]:
        idx += 1
        continue
    solution = angles.pop(idx)
    last_angle = solution[0]
    cnt += 1
print(f"Part two: {solution[1][0] * 100 + solution[1][1]}")
