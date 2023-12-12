from functools import cache


def get_data(folds=1):
    data = []
    with open("202312.txt", "r") as f:
        for line in f:
            [a, b] = line.strip().split()
            nums = tuple(map(int, b.split(","))) * folds
            pattern = (
                "?".join([a] * folds) + "."
            )  # adding a trailing dot avoids range checking in r()
            data.append((pattern, nums))
    return data


@cache
def r(pattern, nums):
    if nums == ():
        # If we've used all the numbers, it's only valid if there's not a
        # known # left in the pattern.
        return 0 if "#" in pattern else 1
    n = nums[0]
    res = 0
    # pattern length - (sum of remaining numbers plus padding) + 1
    for i in range(len(pattern) - (sum(nums) + len(nums)) + 1):
        if pattern[i + n] == "#":
            # padding space can't be a known #
            continue
        if "#" in pattern[:i]:
            # can't not use a known # before the window, and since we have no
            # window after this one can be valid either.
            break
        if "." not in pattern[i : i + n]:
            # If there's not a known . in the window, we can use it.
            res += r(pattern[i + n + 1 :], nums[1:])
    return res


part_one = 0
for pattern, nums in get_data():
    part_one += r(pattern, nums)
print(f"Part one: {part_one}")

part_two = 0
for pattern, nums in get_data(folds=5):
    part_two += r(pattern, nums)
print(f"Part two: {part_two}")
