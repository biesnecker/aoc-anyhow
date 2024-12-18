from utils import (
    input_as_list_of_numbers_iter,
    xy_to_coord,
    coord_to_xy,
    get_neighbors_cardinal,
)
import heapq

input = []
for [x, y] in input_as_list_of_numbers_iter("202418.txt", split_on=","):
    input.append(xy_to_coord(x, y))


def can_navigate(steps):
    grid = {c for c in input[:steps]}
    q = [(0, 0, 0)]
    visited = set()
    target = xy_to_coord(70, 70)
    x_bound = 70
    y_bound = 70
    while q:
        cost, x, y = heapq.heappop(q)
        pos = xy_to_coord(x, y)
        if pos == target:
            return cost
        for _, npos in get_neighbors_cardinal(pos):
            x, y = coord_to_xy(npos)
            if (
                x < 0
                or y < 0
                or x > x_bound
                or y > y_bound
                or npos in visited
                or npos in grid
            ):
                continue
            visited.add(npos)
            heapq.heappush(q, (cost + 1, x, y))
    return None


part_one = can_navigate(1024)
assert part_one is not None
print("Part One:", part_one)

i = 1024
j = len(input) - 1
while i < j:
    mid = (i + j) // 2
    if can_navigate(mid) is None:
        j = mid - 1
    else:
        i = mid
x, y = coord_to_xy(input[i])
print(f"Part Two: {x},{y}")
