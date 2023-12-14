import numpy as np

with open("202314.txt", "r") as f:
    grid = np.array(
        [
            [0 if c == "." else 1 if c == "O" else 2 for c in line]
            for line in f.read().splitlines()
        ],
        dtype=int,
    )


def align_ones(array):
    oc = 0
    zc = 0

    for i in range(len(array)):
        if array[i] == 1:
            oc += 1
        elif array[i] == 0:
            zc += 1
        else:
            if oc > 0:
                s = i - oc - zc
                array[s : s + zc] = 0
                array[s + zc : i] = 1
            zc = 0
            oc = 0
    # handle the leftovers
    if oc > 0:
        s = len(array) - oc - zc
        array[s : s + zc] = 0
        array[s + zc : len(array)] = 1
    return array


def cycle(grid):
    for _ in range(4):
        grid = np.rot90(grid, axes=(1, 0))
        for row in grid:
            align_ones(row)
    return grid


def score(grid):
    nrows = len(grid)
    factors = np.arange(nrows, 0, -1).reshape(nrows, 1)
    return np.sum(np.where(grid == 1, 1, 0) * factors)


part_one = np.rot90(grid, axes=(1, 0))
for row in part_one:
    align_ones(row)
print(f"Part one: {score(np.rot90(part_one))}")

seen = {}
rev = {}
i = 0
for i in range(1000000000):
    grid = cycle(grid)
    if (s := grid.tobytes()) in seen:
        last_seen = seen[s]
        cycle_length = i - last_seen

        # Calculate where in the cycle the billionth iteration is.
        offset = (1000000000 - i) % cycle_length
        print(f"Part two: {score(rev[last_seen + offset])}")
        break
    seen[s] = i
    rev[i] = grid
    i += 1
