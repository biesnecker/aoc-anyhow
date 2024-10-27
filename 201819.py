import re

prog = []
ipr = 0

with open("201819.txt", "r") as f:
    for line in f.readlines():
        if line[0] == "#":
            ipr = int(line[4])
        else:
            m = re.match(r"([a-z]+) (\d+) (\d+) (\d+)", line.strip())
            assert m is not None
            i, a, b, c = m.groups()
            prog.append((i, int(a), int(b), int(c)))


def execute(p, ipr, reg=0):
    r = [reg, 0, 0, 0, 0, 0]

    while 0 <= r[ipr] < len(p):
        # Yay reverse engineering
        if r[ipr] == 1:
            return sum([x for x in range(1, r[5] + 1) if r[5] % x == 0])
        i, a, b, c = p[r[ipr]]
        if i == "addr":
            r[c] = r[a] + r[b]
        elif i == "addi":
            r[c] = r[a] + b
        elif i == "mulr":
            r[c] = r[a] * r[b]
        elif i == "muli":
            r[c] = r[a] * b
        elif i == "banr":
            r[c] = r[a] & r[b]
        elif i == "bani":
            r[c] = r[a] & b
        elif i == "borr":
            r[c] = r[a] | r[b]
        elif i == "bori":
            r[c] = r[a] | b
        elif i == "setr":
            r[c] = r[a]
        elif i == "seti":
            r[c] = a
        elif i == "gtir":
            r[c] = 1 if a > r[b] else 0
        elif i == "gtri":
            r[c] = 1 if r[a] > b else 0
        elif i == "gtrr":
            r[c] = 1 if r[a] > r[b] else 0
        elif i == "eqir":
            r[c] = 1 if a == r[b] else 0
        elif i == "eqri":
            r[c] = 1 if r[a] == b else 0
        elif i == "eqrr":
            r[c] = 1 if r[a] == r[b] else 0
        else:
            raise Exception(f"Unknown opcode {i}")

        r[ipr] += 1

    return r[0]  # never reachable after reverse engineering of prog


print(f"Part One: {execute(prog, ipr)}")
print(f"Part Two: {execute(prog, ipr, 1)}")
