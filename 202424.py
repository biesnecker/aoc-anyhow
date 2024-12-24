import re
from functools import cache
from typing import Dict, List, Optional, Set, Tuple

from utils import input_as_strings_iter

known: Dict[str, Optional[int]] = dict()
net: Dict[str, Tuple[str, List[str]]] = dict()
all_wires: Set[str] = set()
part_one = True
for line in input_as_strings_iter("202424.txt"):
    if line == "":
        part_one = False
        continue
    elif part_one:
        label, value = line.split(": ")
        known[label] = int(value)
        all_wires.add(label)
    else:
        [a, op, b, c] = re.match(r"(.{3}) (AND|OR|XOR) (.{3}) -> (.{3})", line).groups()
        net[c] = (op, [a, b])
        all_wires.add(a)
        all_wires.add(b)
        all_wires.add(c)


@cache
def resolve(wire: str) -> int:
    if wire in known:
        return known[wire]
    op, [a, b] = net[wire]
    aval = resolve(a)
    bval = resolve(b)
    if op == "AND":
        return aval & bval
    elif op == "OR":
        return aval | bval
    elif op == "XOR":
        return aval ^ bval
    else:
        raise ValueError(f"Unknown operation: {op}")


x = {wire: resolve(wire) for wire in all_wires if wire.startswith("z")}
part_one = 0
for i, wire in enumerate(sorted(x.keys())):
    part_one |= x[wire] << i
print(f"Part one: {part_one}")
