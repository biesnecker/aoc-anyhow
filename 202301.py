part1 = 0
with open("202301.txt", "r") as f:
    for line in f:
        nums = [c for c in line.strip() if c.isdigit()]
        assert len(nums) > 0
        part1 += int(nums[0]) * 10 + int(nums[-1])
print(f"Part One: {part1}")

part2 = 0
with open("202301.txt", "r") as f:
    for line in f:
        nums = []
        for idx, c in enumerate(line):
            stub = line[idx:]
            if c.isdigit():
                nums.append(int(c))
            elif c == 'o' and stub.startswith("one"):
                nums.append(1)
            elif c == 't' and stub.startswith("two"):
                nums.append(2)
            elif c == 't' and stub.startswith("three"):
                nums.append(3)
            elif c == 'f' and stub.startswith("four"):
                nums.append(4)
            elif c == 'f' and stub.startswith("five"):
                nums.append(5)
            elif c == 's' and stub.startswith("six"):
                nums.append(6)
            elif c == 's' and stub.startswith("seven"):
                nums.append(7)
            elif c == 'e' and stub.startswith("eight"):
                nums.append(8)
            elif c == 'n' and stub.startswith("nine"):
                nums.append(9)
        assert len(nums) > 0
        part2 += int(nums[0]) * 10 + int(nums[-1])
print(f"Part Two: {part2}")
