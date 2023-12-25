from collections import deque
import networkx as nx


with open("202323.txt", "r") as f:
    grid = [line.strip() for line in f]
    mx = len(grid[0])
    my = len(grid)

sx, sy = next((x, 0) for x in range(mx) if grid[0][x] == ".")
ex, ey = next((x, my - 1) for x in range(mx) if grid[my - 1][x] == ".")


def neighbors(x, y, *, slopes=True):
    if not slopes:
        deltas = [(0, 1, "v"), (0, -1, "^"), (1, 0, ">"), (-1, 0, "<")]
    else:
        match grid[y][x]:
            case ".":
                deltas = [(0, 1, "v"), (0, -1, "^"), (1, 0, ">"), (-1, 0, "<")]
            case "^":
                deltas = [(0, -1, "^")]
            case "v":
                deltas = [(0, 1, "v")]
            case ">":
                deltas = [(1, 0, ">")]
            case "<":
                deltas = [(-1, 0, "<")]
            case unexpected:
                raise ValueError(f"Unexpected character {unexpected}")
    for dx, dy, c in deltas:
        if (
            0 <= (nx := x + dx) < mx
            and 0 <= (ny := y + dy) < my
            and grid[ny][nx] != "#"
        ):
            yield nx, ny, c


def compressed_graph(grid, *, slopes):
    G = nx.Graph()
    for i, j in ((i, j) for i in range(mx) for j in range(my) if grid[j][i] != "#"):
        for neighbor in neighbors(i, j):
            G.add_edge((i, j), neighbor[:2])
    intersections = set()
    for node in G.nodes:
        if G.degree(node) != 2:
            intersections.add(node)
    H = nx.DiGraph()
    for node in intersections:
        # BFS from this intersection to the next reachable intersection, and add
        # an edge between them with a weight equal to the distance between them.
        # If slopes is True and the path encounters a slope in the wrong
        # direction, then the path is invalid and we'll skip it.
        q = deque([(node, 0, node)])
        seen = set()
        while q:
            ((x, y), d, start) = q.popleft()
            if (x, y) in seen:
                continue
            seen.add((x, y))
            if (x, y) != start and (x, y) in intersections:
                H.add_edge(start, (x, y), weight=d)
                continue
            for neighbor in neighbors(x, y, slopes=slopes):
                if slopes and grid[y][x] != "." and grid[y][x] != neighbor[2]:
                    continue  # can't go up a slope in the wrong direction
                q.append((neighbor[:2], d + 1, start))
    return H


for slopes in (True, False):
    g = compressed_graph(grid, slopes=slopes)
    res = 0
    c = 0
    for path in nx.all_simple_edge_paths(g, (sx, sy), (ex, ey)):
        res = max(res, sum(g.edges[n]["weight"] for n in path))
    if slopes:
        print(f"Part one: {res}")
    else:
        print(f"Part two: {res}")
