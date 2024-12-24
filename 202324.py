import re

import numpy as np
import z3

with open("202324.txt", "r") as f:
    hail = [[int(x) for x in re.findall(r"-?\d+", line.strip())] for line in f]


def intersect_rays(p1, d1, p2, d2):
    A = np.array([d1, -d2]).T
    b = p2 - p1

    # Check for parallel lines
    if np.isclose(np.linalg.det(A), 0):
        return None

    t1, t2 = np.linalg.solve(A, b)

    if t1 < 0 or t2 < 0:
        return None

    intersection = p1 + t1 * d1

    return intersection


min_i = 200000000000000
max_i = 400000000000000

part_one = 0
for i in range(len(hail) - 1):
    for j in range(i + 1, len(hail)):
        p1 = np.array([hail[i][0], hail[i][1]])
        d1 = np.array([hail[i][3], hail[i][4]])
        p2 = np.array([hail[j][0], hail[j][1]])
        d2 = np.array([hail[j][3], hail[j][4]])
        inter = intersect_rays(p1, d1, p2, d2)
        if inter is not None and np.all(inter >= min_i) and np.all(inter <= max_i):
            part_one += 1
print(f"Part one: {part_one}")


rock = z3.RealVector("r", 6)
time = z3.RealVector("t", 3)
s = z3.Solver()
s.add(
    *[
        rock[d] + rock[d + 3] * t == hail[d] + hail[d + 3] * t
        for t, hail in zip(time, hail)
        for d in range(3)
    ]
)
s.check()

part_two = s.model().eval(sum(rock[:3]))
print(f"Part two: {part_two}")
