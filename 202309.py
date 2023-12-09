with open("202309.txt", "r") as f:
    sequences = [list(map(int, line.strip().split())) for line in f]


def gen_previous_row(nums):
    for i in range(1, len(nums)):
        yield nums[i] - nums[i - 1]


def all_zeros(nums):
    if len(nums) == 0:
        return True
    return all(n == 0 for n in nums)


def extend_sequence(nums):
    seqs = [nums]
    while not all_zeros(nums):
        nums = list(gen_previous_row(nums))
        seqs.append(nums)
    pseed = None
    nseed = None
    for i in range(len(seqs) - 1, -1, -1):
        if pseed is None:
            pseed = seqs[i][0]
        else:
            pseed = seqs[i][0] - pseed
        if nseed is None:
            nseed = seqs[i][-1]
        else:
            nseed += seqs[i][-1]
    return (pseed, nseed)


psum, nsum = tuple(map(sum, zip(*map(extend_sequence, sequences))))

print(f"Part one: {nsum}")

print(f"Part two: {psum}")
