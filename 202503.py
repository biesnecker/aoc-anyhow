input = []
with open("202503.txt", "r") as f:
    for line in f.readlines():
        input.append(list(map(int, line.strip())))


def max_joltage(row: list[int], n: int) -> int:
    lptr = 0
    rptr = len(row) - n + 1
    res = 0
    while rptr <= len(row):
        num = max(row[lptr:rptr])
        res = res * 10 + num
        lptr = row[lptr:rptr].index(num) + lptr + 1
        rptr += 1
    return res


part1 = sum(map(lambda ns: max_joltage(ns, 2), input))
print(part1)
part2 = sum(map(lambda ns: max_joltage(ns, 12), input))
print(part2)
