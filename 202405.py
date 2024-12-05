from collections import defaultdict
from typing import DefaultDict, Dict, List, Set

from utils import input_as_strings_iter

deps: DefaultDict[int, Set[int]] = defaultdict(set)
orders: List[List[int]] = []
in_deps = True
for line in input_as_strings_iter("202405.txt"):
    line = line.strip()
    if line == "":
        in_deps = False
        continue
    if in_deps:
        a, b = list(map(int, line.split("|")))
        deps[b].add(a)
    else:
        orders.append(list(map(int, line.split(","))))


def reorder(g: Dict[int, Set[int]], order_set: Set[int]) -> int:
    # topological sort
    new_order = []
    q = [k for k, v in g.items() if len(v) == 0]
    while q:
        n = q.pop()
        new_order.append(n)
        for k, v in g.items():
            if n in v:
                g[k].remove(n)
                if len(g[k]) == 0:
                    q.append(k)
    return new_order[len(new_order) // 2]


part_one = 0
part_two = 0
for order in orders:
    assert len(order) % 2 == 1  # should always be odd
    ok = True
    seen = set()
    order_set = set(order)
    # create a graph of dependencies for this printing order
    g = {k: deps[k] & order_set for k in order}
    for page in order:
        if len(g[page] - seen) > 0:
            ok = False
            part_two += reorder(g, order_set)
            break
        seen.add(page)
    if ok:
        part_one += order[len(order) // 2]
print(f"Part one: {part_one}")
print(f"Part two: {part_two}")
