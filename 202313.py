import numpy as np

with open("202313.txt", "r") as f:
    blocks = [
        np.array([[c == "#" for c in line] for line in block.strip().splitlines()])
        for block in f.read().split("\n\n")
    ]


def mirror(block, smudges=0):
    for i in range(1, len(block)):
        n = min(i, len(block) - i)
        if np.sum(np.logical_xor(block[:i][::-1][:n], block[i:][:n])) == smudges:
            return i


def summary(blocks, smudges=0):
    return sum(
        100 * row if (row := mirror(block, smudges)) else mirror(block.T, smudges)
        for block in blocks
    )


print(f"Part one: {summary(blocks)}")
print(f"Part two: {summary(blocks, smudges=1)}")
