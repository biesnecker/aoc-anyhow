from collections import defaultdict

DIM = 50

initial = defaultdict(lambda: ".")

with open("201818.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        for x, c in enumerate(line.strip()):
            initial[x + y * 1j] = c


def get_adj_counts(p):
    lumberyards = 0
    trees = 0
    for idx in [
        p - 1 - 1j,
        p - 1,
        p - 1 + 1j,
        p - 1j,
        p + 1j,
        p + 1 - 1j,
        p + 1,
        p + 1 + 1j,
    ]:
        if idx not in map:
            continue
        elif map[idx] == "|":
            trees += 1
        elif map[idx] == "#":
            lumberyards += 1
    return lumberyards, trees


def evolve(m):
    n = defaultdict(lambda: ".")
    for y in range(0, DIM):
        for x in range(0, DIM):
            p = x + y * 1j
            c = m[p]
            lumberyards, trees = get_adj_counts(p)
            if c == "." and trees >= 3:
                n[p] = "|"
            elif c == "|":
                if lumberyards >= 3:
                    n[p] = "#"
                else:
                    n[p] = "|"
            elif c == "#" and lumberyards > 0 and trees > 0:
                n[p] = "#"
    return n


def score(m):
    lumberyards = 0
    trees = 0
    for c in m.values():
        if c == "|":
            trees += 1
        elif c == "#":
            lumberyards += 1
    return lumberyards * trees


def debug_print_map(m):
    for y in range(0, DIM):
        for x in range(0, DIM):
            print(m[x + y * 1j], end="")
        print()
    print()


map = initial
scores = defaultdict(set)
for i in range(1000000):
    map = evolve(map)
    s = score(map)
    if i == 9:
        print(f"Part One: {s}")

    if s in scores and len(scores[s]) > 1:
        period = i - max(scores[s])
        if (i + 1) % period == 1000000000 % period:
            print(f"Part Two: {s}")
            break
    scores[s].add(i)
