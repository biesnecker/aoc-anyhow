from collections import defaultdict

with open("201503.txt", "r") as f:
    dirs = [c for c in f.readline().strip()]


def walk(dirs, walkers):
    grid = defaultdict(bool)
    grid[(0, 0)] = len(walkers)
    for i, c in enumerate(dirs):
        match c:
            case "^":
                walkers[i % len(walkers)][1] -= 1
            case "v":
                walkers[i % len(walkers)][1] += 1
            case "<":
                walkers[i % len(walkers)][0] -= 1
            case ">":
                walkers[i % len(walkers)][0] += 1
        grid[tuple(walkers[i % len(walkers)])] = True
    return sum(grid.values())


part_one = walk(dirs, [[0, 0]])
print(f"Part one: {part_one}")

part_two = walk(dirs, [[0, 0], [0, 0]])
print(f"Part two: {part_two}")
