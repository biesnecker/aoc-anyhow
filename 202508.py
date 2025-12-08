import math
from collections import Counter, deque

type coord = tuple[int, int, int]

with open("202508.txt", "r") as f:
    coords: list[coord] = [
        (x, y, z)
        for line in f
        for x, y, z in [(int(num) for num in line.strip().split(","))]
    ]


edges = [
    ((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2, a, b)
    for i, a in enumerate(coords)
    for b in coords[i + 1 :]
]
edges.sort()

parents = {}


def find(x):
    if x not in parents:
        parents[x] = x
    if parents[x] != x:
        parents[x] = find(parents[x])
    return parents[x]


def union(x, y):
    parents[find(x)] = find(y)


i = 0
nc = len(coords)

while nc > 1:
    _, a, b = edges[i]
    i += 1

    if find(a) != find(b):
        union(a, b)
        nc -= 1
        last_edge = (a, b)

    if i == 1000:
        cs = Counter(find(c) for c in coords)
        print(math.prod(size for _, size in cs.most_common(3)))

print(last_edge[0][0] * last_edge[1][0])
