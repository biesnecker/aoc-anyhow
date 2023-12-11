from collections import deque

grid = {}
sx, sy = -1, -1

with open("202310.txt", "r") as f:
    for y, line in enumerate(f):
        for x, char in enumerate(line.strip()):
            grid[(x, y)] = char
            if char == "S":
                sx, sy = x, y
assert sx != -1 and sy != -1


def possible(grid, x, y):
    if (x, y) not in grid:
        return
    match grid[(x, y)]:
        case "-":
            if (x + 1, y) in grid and grid[(x + 1, y)] in connects_from_left:
                yield (x + 1, y)
            if (x - 1, y) in grid and grid[(x - 1, y)] in connects_from_right:
                yield (x - 1, y)
        case "|":
            if (x, y + 1) in grid and grid[(x, y + 1)] in connects_from_top:
                yield (x, y + 1)
            if (x, y - 1) in grid and grid[(x, y - 1)] in connects_from_bottom:
                yield (x, y - 1)
        case "F":
            if (x + 1, y) in grid and grid[(x + 1, y)] in connects_from_left:
                yield (x + 1, y)
            if (x, y + 1) in grid and grid[(x, y + 1)] in connects_from_top:
                yield (x, y + 1)
        case "7":
            if (x, y + 1) in grid and grid[(x, y + 1)] in connects_from_top:
                yield (x, y + 1)
            if (x - 1, y) in grid and grid[(x - 1, y)] in connects_from_right:
                yield (x - 1, y)
        case "L":
            if (x + 1, y) in grid and grid[(x + 1, y)] in connects_from_left:
                yield (x + 1, y)
            if (x, y - 1) in grid and grid[(x, y - 1)] in connects_from_bottom:
                yield (x, y - 1)
        case "J":
            if (x - 1, y) in grid and grid[(x - 1, y)] in connects_from_right:
                yield (x - 1, y)
            if (x, y - 1) in grid and grid[(x, y - 1)] in connects_from_bottom:
                yield (x, y - 1)
        case x:
            raise ValueError(f"Invalid tile: {x}")


connects_from_top = {"|", "L", "J"}
connects_from_bottom = {"|", "F", "7"}
connects_from_left = {"-", "J", "7"}
connects_from_right = {"-", "F", "L"}

# figure out what S is.
maybe_s = {"|", "-", "F", "7", "L", "J"}
top_connects = (sx, sy - 1) in grid and grid[(sx, sy - 1)] in connects_from_bottom
bottom_connects = (sx, sy + 1) in grid and grid[(sx, sy + 1)] in connects_from_top
left_connects = (sx - 1, sy) in grid and grid[(sx - 1, sy)] in connects_from_right
right_connects = (sx + 1, sy) in grid and grid[(sx + 1, sy)] in connects_from_left
match (top_connects, bottom_connects, left_connects, right_connects):
    case (True, True, False, False):
        grid[(sx, sy)] = "|"
    case (False, False, True, True):
        grid[(sx, sy)] = "-"
    case (True, False, True, False):
        grid[(sx, sy)] = "J"
    case (True, False, False, True):
        grid[(sx, sy)] = "L"
    case (False, True, True, False):
        grid[(sx, sy)] = "7"
    case (False, True, False, True):
        grid[(sx, sy)] = "F"
    case x:
        raise ValueError(f"Invalid outlets for S: {x}")
print(grid[(sx, sy)])

q = deque([(sx, sy, 0)])
visited = {(sx, sy)}
max_steps = -1
while q:
    (x, y, steps) = q.popleft()
    print(x, y, steps, grid[(x, y)])
    max_steps = max(max_steps, steps)
    for nx, ny in possible(grid, x, y):
        print(f"Possible: {nx}, {ny} ({grid[(nx, ny)]})")
        if (nx, ny) not in visited:
            visited.add((nx, ny))
            q.append((nx, ny, steps + 1))
print(f"Part one: {max_steps}")
