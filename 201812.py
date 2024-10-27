from collections import defaultdict


def torule(s):
    return (s[0] == "#", s[1] == "#", s[2] == "#", s[3] == "#", s[4] == "#")


def nextgen(current, rules):
    start = min(current)
    stop = max(current)
    nextgen = set()
    for i in range(start - 2, stop + 3):
        rule = (
            i - 2 in current,
            i - 1 in current,
            i in current,
            i + 1 in current,
            i + 2 in current,
        )
        if rule in rules:
            nextgen.add(i)
    return nextgen


with open("201812.txt", "r") as f:
    initial = f.readline().strip().split(":")[1].strip()
    current = {i for i, c in enumerate(initial) if c == "#"}

    print(current)

    f.readline()  # skip blank line

    rules = set()
    for line in f:
        if line.strip() == "":
            break
        parts = line.strip().split(" => ")
        if parts[1] == "#":
            rules.add(torule(parts[0]))

    for i in range(20):
        current = nextgen(current, rules)

    print(f"Part One: {sum(current)}")

    # Need to find the period.
    seen = set()

    current = {i for i, c in enumerate(initial) if c == "#"}
    last_sum = 0
    diff = 0
    s = 0
    for _ in range(2000):
        current = nextgen(current, rules)
        s = sum(current)
        diff = s - last_sum
        last_sum = s
    print(f"Part Two: {s + (50000000000 - 2000) * diff}")
