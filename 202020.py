import functools
import itertools
import operator

import networkx
import numpy as np

tiles = {}

with open("202020.txt", "r") as f:
    for tiledata in f.read().strip().split("\n\n"):
        a, *tilelines = tiledata.splitlines()
        num = int(a.strip(":").split()[1])
        tiles[num] = np.array(
            [[c == "#" for c in l] for l in tilelines], dtype=np.uint8
        )


def nptobin(s):
    return int("".join([str(k) for k in s]), 2)


def get_borders(n):
    return [nptobin(n[0]), nptobin(n[:, -1]), nptobin(n[-1]), nptobin(n[:, 0])]


def get_flips(tile):
    res = tile
    for f in [True, False]:
        for i in range(4):
            yield res
            res = np.rot90(res)
        res = np.flip(tile, 1)


borders = {}

for n, tile in tiles.items():
    borders[n] = set.union(*[set(get_borders(fl)) for fl in get_flips(tile)])

grph = networkx.Graph()

for i, j in itertools.combinations(borders, 2):
    if len(borders[i] & borders[j]) == 2:
        grph.add_edge(i, j)

corners = [n for n in grph if len(grph[n]) == 2]
part_one = functools.reduce(operator.mul, corners)
print(f"Part one: {part_one}")


def ext(pt):
    used = set(tile for tile, _ in grd.values())
    tile, img = grd[pt]
    border = get_borders(img)
    for nb in grph[tile]:
        if nb not in used:
            for fl in get_flips(tiles[nb]):
                if get_borders(fl)[0] == border[2]:
                    grd[(pt[0] + 1, pt[1])] = (nb, fl)
                if get_borders(fl)[3] == border[1]:
                    grd[(pt[0], pt[1] + 1)] = (nb, fl)


for fl in get_flips(tiles[corners[0]]):
    grd = {}
    grd[(0, 0)] = (corners[0], fl)
    ext((0, 0))
    if len(grd) == 3:
        break

for i in range(12):
    for j in range(12):
        ext((i, j))

image = np.concatenate(
    [
        np.concatenate([grd[i, j][1][1:-1, 1:-1] for j in range(12)], axis=1)
        for i in range(12)
    ],
    axis=0,
)

monster_str = (
    "                  # \n"
    "#    ##    ##    ###\n"
    " #  #  #  #  #  #   ".splitlines()
)

monster = np.array([[c == "#" for c in l] for l in monster_str], dtype=np.uint8)

for image in get_flips(image):
    count = 0
    for i in range(image.shape[0] - monster.shape[0] + 1):
        for j in range(image.shape[1] - monster.shape[1] + 1):
            check = image[i : i + monster.shape[0], j : j + monster.shape[1]]
            if (check & monster == monster).all():
                count += 1
    if count:
        break
part_two = int(np.sum(image) - count * np.sum(monster))
print(f"Part two: {part_two}")
