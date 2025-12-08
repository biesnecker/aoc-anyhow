import heapq
import math
from collections import Counter, defaultdict, deque
from typing import Iterator

type coord = tuple[int, int, int]

with open("202508.txt", "r") as f:
    coords: list[coord] = [
        (x, y, z)
        for line in f
        for x, y, z in [(int(num) for num in line.strip().split(","))]
    ]


def yield_all_pairs_by_distance(
    points: list[coord],
) -> Iterator[tuple[int, int, int]]:
    n = len(points)
    if n < 2:
        return

    def sq_dist(i: int, j: int) -> int:
        dx = points[i][0] - points[j][0]
        dy = points[i][1] - points[j][1]
        dz = points[i][2] - points[j][2]
        return dx * dx + dy * dy + dz * dz

    # Compute bounding box and cell size
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    zs = [p[2] for p in points]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    min_z, max_z = min(zs), max(zs)

    extent = max(max_x - min_x, max_y - min_y, max_z - min_z, 1)

    # Cell size: ~10 points per cell on average
    cell_size = max(1, int(extent / (n / 10) ** (1 / 3)))

    def cell(idx: int) -> tuple[int, int, int]:
        p = points[idx]
        return (p[0] // cell_size, p[1] // cell_size, p[2] // cell_size)

    # Build grid
    grid: dict[tuple[int, int, int], list[int]] = defaultdict(list)
    point_cells: list[tuple[int, int, int]] = []
    for i in range(n):
        c = cell(i)
        grid[c].append(i)
        point_cells.append(c)

    # Compute max shell we'd ever need
    cells_x = [c[0] for c in point_cells]
    cells_y = [c[1] for c in point_cells]
    cells_z = [c[2] for c in point_cells]
    max_shell = (
        max(
            max(cells_x) - min(cells_x),
            max(cells_y) - min(cells_y),
            max(cells_z) - min(cells_z),
        )
        + 1
    )

    shell_searched = [0] * n  # How far each point has searched
    seen: set[tuple[int, int]] = set()  # Pairs added to heap

    # Two kinds of heap entries:
    #   Pair:      (sq_dist, 0, i, j)
    #   Expansion: (lower_bound, 1, point_idx, shell)
    # Using 0/1 as second element ensures pairs come before same-priority expansions
    heap: list[tuple[int, int, int, int]] = []

    def shell_lower_bound_sq(r: int) -> int:
        """Minimum squared distance for pairs first seen in shell r."""
        if r <= 1:
            return 0
        return ((r - 1) * cell_size) ** 2

    def add_pairs_from_cell(i: int, cell_key: tuple[int, int, int]):
        """Add all pairs between point i and points in cell_key."""
        for j in grid.get(cell_key, ()):
            if i != j:
                pair = (i, j) if i < j else (j, i)
                if pair not in seen:
                    seen.add(pair)
                    heapq.heappush(heap, (sq_dist(i, j), 0, pair[0], pair[1]))

    def expand_to_shell(i: int, r: int):
        """Search cells at exactly Chebyshev distance r from point i's cell."""
        cx, cy, cz = point_cells[i]
        for dx in range(-r, r + 1):
            for dy in range(-r, r + 1):
                for dz in range(-r, r + 1):
                    if max(abs(dx), abs(dy), abs(dz)) == r:
                        add_pairs_from_cell(i, (cx + dx, cy + dy, cz + dz))

    # Initialize: search shells 0 and 1 for all points
    for i in range(n):
        expand_to_shell(i, 0)
        expand_to_shell(i, 1)
        shell_searched[i] = 1
        if 2 <= max_shell:
            heapq.heappush(heap, (shell_lower_bound_sq(2), 1, i, 2))

    while heap:
        entry = heapq.heappop(heap)
        _, entry_type, a, b = entry

        if entry_type == 1:
            # Expansion marker: a=point_idx, b=shell
            i, r = a, b
            if shell_searched[i] < r:
                expand_to_shell(i, r)
                shell_searched[i] = r
                if r + 1 <= max_shell:
                    heapq.heappush(heap, (shell_lower_bound_sq(r + 1), 1, i, r + 1))
        else:
            # Pair: a=i, b=j
            yield (a, b)


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
gen = yield_all_pairs_by_distance(coords)

while nc > 1:
    a, b = next(gen)
    i += 1

    if find(a) != find(b):
        union(a, b)
        nc -= 1
        last_edge = (a, b)

    if i == 1000:
        cs = Counter(find(c) for c in range(len(coords)))
        print(math.prod(size for _, size in cs.most_common(3)))

print(coords[last_edge[0]][0] * coords[last_edge[1]][0])
