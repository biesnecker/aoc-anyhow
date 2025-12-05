import bisect

with open("202505.txt") as f:
    lines = [line.strip() for line in f]

idx = lines.index("")
ranges = sorted(
    (range(int(a), int(b) + 1) for a, b in (line.split("-") for line in lines[:idx])),
    key=lambda r: r.start,
)
ingredients = [int(line) for line in lines[idx + 1 :]]

merged = [ranges[0]]
for r in ranges[1:]:
    prev = merged[-1]
    if r.start <= prev.stop:
        merged[-1] = range(prev.start, max(r.stop, prev.stop))
    else:
        merged.append(r)


def contains(n):
    i = bisect.bisect_right(merged, n, key=lambda r: r.start) - 1
    return i >= 0 and n in merged[i]


print(sum(contains(i) for i in ingredients))  # Part 1
print(sum(r.stop - r.start for r in merged))  # Part 2
