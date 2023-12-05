import itertools
import math

seeds = []
mappings = []

with open("202305.txt", "r") as f:
    groups = [
        list(v)
        for k, v in itertools.groupby(
            map(lambda ln: ln.strip(), f.readlines()), lambda x: x == ""
        )
        if not k
    ]
    for gid, group in enumerate(groups):
        if gid == 0:
            seeds = list(map(int, group[0].split(": ")[1].split()))
        else:
            g = sorted([list(map(int, ln.split())) for ln in group[1:]])
            mappings.append(g)


def get_mapping(ranges, val):
    for r in ranges:
        if r[1] <= val < (r[1] + r[2]):
            return r[0] + (val - r[1])
    return val  # fallthrough if nothing matches


def get_seed_mappings(seeds):
    for s in seeds:
        for m in mappings:
            s = get_mapping(m, s)
        yield s


part_one = min(get_seed_mappings(seeds))
print(f"Part one: {part_one}")
