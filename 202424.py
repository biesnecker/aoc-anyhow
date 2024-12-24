import re
from functools import cache
from typing import Dict, List, Set, Tuple

from utils import input_as_strings_iter

inputs: Dict[str, int] = dict()
net: Dict[str, Tuple[str, List[str]]] = dict()
all_wires: Set[str] = set()
part_one = True
for line in input_as_strings_iter("202424.txt"):
    if line == "":
        part_one = False
        continue
    elif part_one:
        label, value = line.split(": ")
        inputs[label] = int(value)
        all_wires.add(label)
    else:
        [a, op, b, c] = re.match(r"(.{3}) (AND|OR|XOR) (.{3}) -> (.{3})", line).groups()
        net[c] = (op, [a, b])
        all_wires.add(a)
        all_wires.add(b)
        all_wires.add(c)


@cache
def resolve(wire: str) -> int:
    if wire in inputs:
        return inputs[wire]
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


z = {wire: resolve(wire) for wire in all_wires if wire.startswith("z")}
part_one = sum(z[wire] << i for i, wire in enumerate(sorted(z.keys())))
print(f"Part one: {part_one}")


def part_two():
    faulty = set()
    last_z = sorted(z.keys())[-1]

    def is_input_wire(*wires: str) -> bool:
        return all(wire.startswith("x") or wire.startswith("y") for wire in wires)

    def is_output_wire(*wires: List[str]) -> bool:
        return all(wire.startswith("z") for wire in wires)

    def is_first_bit(*wires: List[str]) -> bool:
        return all(wire.endswith("00") for wire in wires)

    for output, (op, [a, b]) in net.items():
        is_faulty = False
        if is_output_wire(output) and output != last_z:
            # All outputs except the last one should be fed by an XOR
            is_faulty = op != "XOR"
        elif not is_output_wire(output) and not is_input_wire(a, b):
            # No intermediate gates should be an XOR
            is_faulty = op == "XOR"
        elif is_input_wire(a, b) and not is_first_bit(a, b):
            # If the wire is being fed by two input wires, but not the first bits
            # (because they start the chain and are special) then XOR should feed
            # into XOR (for addition) and AND should feed into OR (for carry).
            expected = "XOR" if op == "XOR" else "OR"

            feeds = False
            for c, (op2, [a2, b2]) in net.items():
                if c == output:
                    continue
                if (a2 == output or b2 == output) and op2 == expected:
                    feeds = True
                if feeds:
                    break
            is_faulty = not feeds
        if is_faulty:
            faulty.add(output)
    return ",".join(sorted(faulty))


print(f"Part two: {part_two()}")
