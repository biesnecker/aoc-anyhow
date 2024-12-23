from collections import defaultdict
from itertools import combinations
from typing import DefaultDict, Iterable, Optional, Set

from utils import input_as_strings_iter

graph: DefaultDict[str, Set[str]] = defaultdict(set)
for line in input_as_strings_iter("202423.txt"):
    a, b = line.split("-")
    graph[a].add(b)
    graph[b].add(a)


part_one = 0
for a in graph.keys():
    if not a.startswith("t"):
        continue
    skip: Set[str] = set()
    for b, c in combinations((n for n in graph[a] if not n.startswith("t")), 2):
        if b in skip or c in skip:
            continue
        if a not in graph[b]:
            skip.add(b)
            continue
        if a not in graph[c]:
            skip.add(c)
            continue
        if b in graph[c] and c in graph[b]:
            part_one += 1
print(f"Part one: {part_one}")


def bron_kerbosch(
    p: Iterable[str],
    r: Optional[Iterable[str]] = None,
    x: Optional[Iterable[str]] = None,
):
    p = set(p)
    r = set(r or [])
    x = set(x or [])
    if not p and not x:
        yield r
    while p:
        v = p.pop()
        yield from bron_kerbosch(p & graph[v], r | {v}, x & graph[v])
        x.add(v)


part_two = ",".join(
    sorted(sorted(bron_kerbosch(graph.keys()), key=lambda x: -len(x))[0])
)
print(f"Part two: {part_two}")
