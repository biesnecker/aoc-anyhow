from enum import IntEnum

from intcode import OutputInterrupt, intcode_from_file

c = intcode_from_file("201917.txt")


class Tile(IntEnum):
    SCAFFOLD = ord("#")
    SPACE = ord(".")


class Direction(IntEnum):
    UP = ord("^")
    DOWN = ord("v")
    LEFT = ord("<")
    RIGHT = ord(">")


grid = {}
robots = None
y = 0
x = 0
while not c.halted:
    try:
        c.run()
    except OutputInterrupt:
        match c.pop_output():
            case 10:
                x = 0
                y += 1
            case Tile.SCAFFOLD:
                grid[(x, y)] = Tile.SCAFFOLD
                x += 1
            case Tile.SPACE:
                x += 1
            case Direction.UP:
                grid[(x, y)] = Tile.SCAFFOLD
                robot = ((x, y), Direction.UP)
                x += 1
            case Direction.DOWN:
                grid[(x, y)] = Tile.SCAFFOLD
                robot = ((x, y), Direction.DOWN)
                x += 1
            case Direction.LEFT:
                grid[(x, y)] = Tile.SCAFFOLD
                robot = ((x, y), Direction.LEFT)
                x += 1
            case Direction.RIGHT:
                grid[(x, y)] = Tile.SCAFFOLD
                robot = ((x, y), Direction.RIGHT)
                x += 1
            case unk:
                raise Exception(f"Unknown value: {unk}")


def debug_print(grid, robot, seen={}):
    (rc, rd) = robot
    min_x = min(x for (x, _) in grid.keys())
    max_x = max(x for (x, _) in grid.keys())
    min_y = min(y for (_, y) in grid.keys())
    max_y = max(y for (_, y) in grid.keys())

    for y in range(min_y, max_y + 1):
        line = []
        for x in range(min_x, max_x + 1):
            if (x, y) not in grid:
                line.append(".")
            elif (x, y) in seen:
                line.append("O")
            elif (x, y) == rc:
                match rd:
                    case Direction.UP:
                        line.append("^")
                    case Direction.DOWN:
                        line.append("v")
                    case Direction.LEFT:
                        line.append("<")
                    case Direction.RIGHT:
                        line.append(">")
            else:
                line.append("#")
        print("".join(line))


def is_intersection(grid, x, y):
    for dx, dy in [(1, 0), (-1, 0), (0, -1), (0, 1)]:
        nx = x + dx
        ny = y + dy
        if (nx, ny) not in grid or grid[(nx, ny)] != Tile.SCAFFOLD:
            return False
    return True


part_one = 0
for (x, y), t in grid.items():
    if t == Tile.SCAFFOLD and is_intersection(grid, x, y):
        part_one += x * y
print(f"Part one: {part_one}")


def next_coord(rx, ry, d):
    match d:
        case Direction.UP:
            return (rx, ry - 1)
        case Direction.DOWN:
            return (rx, ry + 1)
        case Direction.LEFT:
            return (rx - 1, ry)
        case Direction.RIGHT:
            return (rx + 1, ry)


def next_move(grid, rx, ry, d):
    nm = next_coord(rx, ry, d)
    if nm in grid and grid[nm] == Tile.SCAFFOLD:
        return (None, d)
    else:
        match d:
            case Direction.UP:
                possible = {"L": Direction.LEFT, "R": Direction.RIGHT}
            case Direction.DOWN:
                possible = {"R": Direction.LEFT, "L": Direction.RIGHT}
            case Direction.LEFT:
                possible = {"L": Direction.DOWN, "R": Direction.UP}
            case Direction.RIGHT:
                possible = {"R": Direction.DOWN, "L": Direction.UP}
        for turn, p in possible.items():
            nm = next_coord(rx, ry, p)
            if nm in grid and grid[nm] == Tile.SCAFFOLD:
                return (turn, p)
        return ("S", None)


((rx, ry), d) = robot

seen = set()
streak = 0
path = []

while True:
    (turn, d) = next_move(grid, rx, ry, d)
    if turn is None:
        seen.add((rx, ry))
        streak += 1
        rx, ry = next_coord(rx, ry, d)
    elif turn == "S":
        if streak > 0:
            path.append(str(streak))
            streak = 0
        break
    else:
        if streak > 0:
            path.append(str(streak))
            streak = 0
        path.append(turn)


def encode_program(p, sra, srb, src):
    p = ",".join(map(str, p))
    sra = ",".join(map(str, sra))
    srb = ",".join(map(str, srb))
    src = ",".join(map(str, src))
    return (p, sra, srb, src)


def valid_program(p, sra, srb, src):
    return len(p) <= 20 and len(sra) <= 20 and len(srb) <= 20 and len(src) <= 20


def remove_prefixes(prog, full, pxs):
    while True:
        removed_any = False
        for ltr, p in pxs.items():
            if len(p) > len(full):
                continue
            elif full[: len(p)] == p:
                full = full[len(p) :]
                prog.append(ltr)
                removed_any = True
        if not removed_any:
            return (prog, full)


def path_to_program(path):
    for i in range(2, 13):
        for j in range(2, 13):
            for k in range(2, 13):
                p = path[:]
                prog = []
                sra = p[:i]
                (prog, p) = remove_prefixes(prog, p, {"A": sra})

                srb = p[:j]
                (prog, p) = remove_prefixes(prog, p, {"B": srb, "A": sra})

                src = p[:k]
                (prog, p) = remove_prefixes(prog, p, {"C": src, "B": srb, "A": sra})

                if len(p) == 0:
                    prog = encode_program(prog, sra, srb, src)
                    if valid_program(*prog):
                        return prog


prog, sra, srb, src = path_to_program(path)

input = []
for p in [prog, sra, srb, src]:
    for c in p:
        input.append(ord(c))
    input.append(10)
input.extend([ord("n"), 10])

c = intcode_from_file("201917.txt", input, mod={0: 2})
output = []
while not c.halted:
    try:
        c.run()
    except OutputInterrupt:
        output.append(c.pop_output())
print(f"Part two: {output[-1]}")
