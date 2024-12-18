from utils import (
    input_as_list_of_numbers_iter,
    xy_to_coord,
    coord_to_xy,
    get_neighbors_cardinal,
    coord_in_bounds,
)
from collections import deque

input = []
for [x, y] in input_as_list_of_numbers_iter("202418.txt", split_on=","):
    input.append(xy_to_coord(x, y))


def can_navigate(steps):
    grid = {c for c in input[:steps]}
    q = deque([(0, xy_to_coord(0, 0))])
    visited = set()
    target = xy_to_coord(70, 70)
    x_bound = 70
    y_bound = 70
    while q:
        cost, pos = q.popleft()
        if pos == target:
            return cost
        for _, npos in get_neighbors_cardinal(pos):
            nx, ny = coord_to_xy(npos)
            if (
                not coord_in_bounds(npos, range(x_bound + 1), range(y_bound + 1))
                or npos in visited
                or npos in grid
            ):
                continue
            visited.add(npos)
            q.append((cost + 1, npos))
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
