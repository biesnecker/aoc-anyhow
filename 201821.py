import re

prog = []
ipr = 0


class OpCode:
    ADDR = 1
    ADDI = 2
    MULR = 3
    MULI = 4
    BANR = 5
    BANI = 6
    BORR = 7
    BORI = 8
    SETR = 9
    SETI = 10
    GTIR = 11
    GTRI = 12
    GTRR = 13
    EQIR = 14
    EQRI = 15
    EQRR = 16


with open("201821.txt", "r") as f:
    for line in f.readlines():
        if line[0] == "#":
            ipr = int(line[4])
        else:
            m = re.match(r"([a-z]+) (\d+) (\d+) (\d+)", line.strip())
            assert m is not None
            i, a, b, c = m.groups()
            if i == "addr":
                i = OpCode.ADDR
            elif i == "addi":
                i = OpCode.ADDI
            elif i == "mulr":
                i = OpCode.MULR
            elif i == "muli":
                i = OpCode.MULI
            elif i == "banr":
                i = OpCode.BANR
            elif i == "bani":
                i = OpCode.BANI
            elif i == "borr":
                i = OpCode.BORR
            elif i == "bori":
                i = OpCode.BORI
            elif i == "setr":
                i = OpCode.SETR
            elif i == "seti":
                i = OpCode.SETI
            elif i == "gtir":
                i = OpCode.GTIR
            elif i == "gtri":
                i = OpCode.GTRI
            elif i == "gtrr":
                i = OpCode.GTRR
            elif i == "eqir":
                i = OpCode.EQIR
            elif i == "eqri":
                i = OpCode.EQRI
            elif i == "eqrr":
                i = OpCode.EQRR
            else:
                raise Exception(f"Unknown opcode: {i}")
            prog.append((i, int(a), int(b), int(c)))


def execute(p, ipr, reg=0, part=0):
    r = [reg, 0, 0, 0, 0, 0]

    seen = set()

    while 0 <= r[ipr] < len(p):
        if r[ipr] == 28:
            assert p[r[ipr]][0] == OpCode.EQRR
            if part == 0:
                return r[4]
            else:
                if r[4] not in seen:
                    print(f"Candidate: {r[4]}")
                    if len(seen) % 1000 == 0:
                        print(f"Total Candidates: {len(seen)}")
                    seen.add(r[4])
                else:
                    return r[4]
        i, a, b, c = p[r[ipr]]
        if i == OpCode.ADDR:
            r[c] = r[a] + r[b]
        elif i == OpCode.ADDI:
            r[c] = r[a] + b
        elif i == OpCode.MULR:
            r[c] = r[a] * r[b]
        elif i == OpCode.MULI:
            r[c] = r[a] * b
        elif i == OpCode.BANR:
            r[c] = r[a] & r[b]
        elif i == OpCode.BANI:
            r[c] = r[a] & b
        elif i == OpCode.BORR:
            r[c] = r[a] | r[b]
        elif i == OpCode.BORI:
            r[c] = r[a] | b
        elif i == OpCode.SETR:
            r[c] = r[a]
        elif i == OpCode.SETI:
            r[c] = a
        elif i == OpCode.GTIR:
            r[c] = 1 if a > r[b] else 0
        elif i == OpCode.GTRI:
            r[c] = 1 if r[a] > b else 0
        elif i == OpCode.GTRR:
            r[c] = 1 if r[a] > r[b] else 0
        elif i == OpCode.EQIR:
            r[c] = 1 if a == r[b] else 0
        elif i == OpCode.EQRI:
            r[c] = 1 if r[a] == b else 0
        elif i == OpCode.EQRR:
            r[c] = 1 if r[a] == r[b] else 0
        else:
            raise Exception(f"Unknown opcode {i}")
        r[ipr] += 1


print(f"Part One: {execute(prog, ipr, reg=0, part=0)}")
print(f"Part Two: {execute(prog, ipr, reg=0, part=1)}")
