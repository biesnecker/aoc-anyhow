import itertools
import math
from collections import namedtuple

seeds = []
mappings = []

mapping = namedtuple("mapping", ["dst", "src"])


def make_mapping(dstart, sstart, size):
    return mapping(range(dstart, dstart + size), range(sstart, sstart + size))


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
            g = [list(map(int, ln.split())) for ln in group[1:]]
            g = sorted(
                [make_mapping(*r) for r in g],
                key=lambda x: x[1].start,
            )
            mappings.append(g)


def get_mapping(ranges, val):
    for m in ranges:
        if val in m.src:
            return m.dst[m.src.index(val)]
    return val  # fallthrough if nothing matches


def get_seed_mappings(seeds):
    for s in seeds:
        for m in mappings:
            s = get_mapping(m, s)
        yield s


part_one = min(get_seed_mappings(seeds))
print(f"Part one: {part_one}")


def gen_next_ranges(r, mappings):
    for m in mappings:
        if m.src.stop < r.start:
            continue  # range is before our range.
        elif m.src.start > r.stop:
            break  # we've gone past our range.
        if r.start < m.src.start:
            # need to yield a range that gets us up to the beginning of rng.
            # These are the fallthrough cases, so there is no mapping.
            yield range(r.start, m.src.start)
            r = range(m.src.start, r.stop)
        assert r.start >= m.src.start
        # nxt is the maximum overlap between r and m.src.
        nxt = range(max(r.start, m.src.start), min(r.stop, m.src.stop))
        # convert the source range into the destination range for nxt
        start_index = m.src.index(nxt.start)
        stop_index = m.src.index(nxt.stop - 1)
        yield range(m.dst[start_index], m.dst[stop_index] + 1)
        if nxt.stop == r.stop:
            return
        r = range(nxt.stop, r.stop)
    if r.start < r.stop:
        yield r


seed_ranges = []
for idx in range(0, len(seeds), 2):
    seed_ranges.append(range(seeds[idx], seeds[idx] + seeds[idx + 1]))
seed_ranges = sorted(seed_ranges, key=lambda x: x.start)


def find_min_r(r, mappings):
    if len(mappings) == 0:
        return r.start
    m = math.inf
    for nr in gen_next_ranges(r, mappings[0]):
        m = min(m, find_min_r(nr, mappings[1:]))
    return m


part_two = min(find_min_r(r, mappings) for r in seed_ranges)
print(f"Part two: {part_two}")
