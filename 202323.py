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


def dfs(G, start, end):
    cache_keys = {node: i for i, node in enumerate(G.nodes)}
    cache = {}

    def dfs_helper(node, seen):
        if node == end:
            return 0
        if (ck := (node, seen)) in cache:
            return cache[ck]
        res = 0
        neighbors = set(G.neighbors(node))
        if end in neighbors:
            res = G.edges[node, end]["weight"]
        else:
            for neighbor in neighbors:
                if neighbor == end:
                    # if we're at a node that connects to the end, then we have
                    # to choose the end, because otherwise we've blocked our
                    # own path.
                    res = max(res, G.edges[node, neighbor]["weight"])
                    break
                if seen & (nck := 1 << cache_keys[neighbor]):
                    continue
                res = max(
                    res,
                    G.edges[node, neighbor]["weight"]
                    + dfs_helper(neighbor, seen | nck),
                )
        cache[ck] = res
        return res

    return dfs_helper(start, 1 << cache_keys[start])


part_one = dfs(compressed_graph(grid, slopes=True), (sx, sy), (ex, ey))
part_two = dfs(compressed_graph(grid, slopes=False), (sx, sy), (ex, ey))

print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
