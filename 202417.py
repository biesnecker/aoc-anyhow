import concurrent.futures
from typing import List

from utils import input_as_strings_iter

regs = [0, 0, 0]
instrs = []

regidx = 0
input_part_one = True
for line in input_as_strings_iter("202417.txt"):
    if line == "":
        input_part_one = False
        continue
    if input_part_one:
        regs[regidx] = int(line.split(": ")[1])
        regidx += 1
    else:
        instrs = list(map(int, line.split(": ")[1].split(",")))


def combo(reg: List[int], val: int) -> int:
    if val < 4:
        return val
    elif val == 4:
        return reg[0]
    elif val == 5:
        return reg[1]
    elif val == 6:
        return reg[2]
    else:
        raise ValueError(f"Invalid combo: {val}")


def part_one(regs: List[int], instrs: List[int]):
    regs = regs.copy()
    out = []
    ip = 0
    while ip >= 0 and ip < len(instrs) - 1:
        op = instrs[ip]
        if op == 0:
            regs[0] = regs[0] // int(2 ** combo(regs, instrs[ip + 1]))
            ip += 2
        elif op == 1:
            regs[1] = regs[1] ^ instrs[ip + 1]
            ip += 2
        elif op == 2:
            regs[1] = combo(regs, instrs[ip + 1]) % 8
            ip += 2
        elif op == 3:
            if regs[0] == 0:
                ip += 2
            else:
                ip = instrs[ip + 1]
        elif op == 4:
            regs[1] = regs[1] ^ regs[2]
            ip += 2
        elif op == 5:
            out.append(combo(regs, instrs[ip + 1]) % 8)
            ip += 2
        elif op == 6:
            regs[1] = regs[0] // int(2 ** combo(regs, instrs[ip + 1]))
            ip += 2
        elif op == 7:
            regs[2] = regs[0] // int(2 ** combo(regs, instrs[ip + 1]))
            ip += 2
        else:
            raise ValueError(f"Invalid op: {op}")
    return out


res = part_one(regs, instrs)
print(f"Part one: {','.join(map(str, res))}")
