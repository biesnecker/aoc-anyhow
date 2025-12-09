from bisect import bisect_left, bisect_right
from collections import defaultdict
from functools import cache
from itertools import combinations

with open("202509.txt", "r") as f:
    coords = [(int(x), int(y)) for line in f for x, y in [line.strip().split(",")]]

v_edges, h_edges = [], []
v_by_x, h_by_y = defaultdict(list), defaultdict(list)

for i in range(len(coords)):
    (x1, y1), (x2, y2) = coords[i], coords[(i + 1) % len(coords)]
    if x1 == x2:
        edge = (min(y1, y2), max(y1, y2))
        v_edges.append((x1, *edge))
        v_by_x[x1].append(edge)
    else:
        edge = (min(x1, x2), max(x1, x2))
        h_edges.append((y1, *edge))
        h_by_y[y1].append(edge)

v_edges_sorted = sorted(v_edges)
h_edges_sorted = sorted(h_edges)
v_xs = [e[0] for e in v_edges_sorted]
h_ys = [e[0] for e in h_edges_sorted]


@cache
def point_valid(x, y):
    if any(y1 <= y <= y2 for y1, y2 in v_by_x[x]):
        return True
    if any(x1 <= x <= x2 for x1, x2 in h_by_y[y]):
        return True
    return sum(1 for vx, vy1, vy2 in v_edges if vx > x and vy1 < y < vy2) % 2 == 1


def rect_valid(x1, x2, y1, y2):
    if not point_valid(x1, y2) or not point_valid(x2, y1):
        return False
    lo, hi = bisect_right(v_xs, x1), bisect_left(v_xs, x2)
    if any(vy2 > y1 and vy1 < y2 for _, vy1, vy2 in v_edges_sorted[lo:hi]):
        return False
    lo, hi = bisect_right(h_ys, y1), bisect_left(h_ys, y2)
    return not any(hx2 > x1 and hx1 < x2 for _, hx1, hx2 in h_edges_sorted[lo:hi])


def rect_area(p1, p2):
    return (abs(p2[0] - p1[0]) + 1) * (abs(p2[1] - p1[1]) + 1)


pairs = sorted(combinations(coords, 2), key=lambda p: rect_area(*p), reverse=True)

print(rect_area(*pairs[0]))  # Part 1

for a, b in pairs:
    x1, x2 = min(a[0], b[0]), max(a[0], b[0])
    y1, y2 = min(a[1], b[1]), max(a[1], b[1])
    if rect_valid(x1, x2, y1, y2):
        print(rect_area(a, b))  # Part 2
        break
