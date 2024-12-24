from utils import input_as_list_of_numbers

inp = input_as_list_of_numbers("202402.txt")


def is_valid(nums, skipping=False):
    if skipping:
        for i in range(len(nums)):
            nnums = nums[:i] + nums[i + 1 :]
            if is_valid(nnums):
                return True
        return False

    diffs = []
    for i in range(1, len(nums)):
        diffs.append(nums[i] - nums[i - 1])
    if any(d == 0 or abs(d) > 3 for d in diffs):
        return False
    ds = [d > 0 for d in diffs]
    return all(d == ds[0] for d in ds)


part_one = sum(is_valid(nums) for nums in inp)

print(f"Part one: {part_one}")

part_two = sum(is_valid(nums, skipping=True) for nums in inp)

print(f"Part two: {part_two}")
