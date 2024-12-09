import sys
from dataclasses import dataclass
from typing import List, Union

from utils import input_as_string


def get_input() -> List[List[int]]:
    input = []
    block_id = 0
    is_block = True
    for c in input_as_string("202409.txt"):
        c = int(c)
        # If it's zero, we're going to skip it
        if c == 0:
            # It shouldn't be a block, zero-sized blocks make no sense
            assert not is_block
        elif is_block:
            input.append([block_id, c])
            block_id += 1
        else:
            input.append([None, c])
        is_block = not is_block
    return input


def part_one():
    input = get_input()
    p_one: List[int] = []
    i = 0
    j = len(input) - 1
    while i <= j:
        if input[i][0] is not None:
            block_id, size = input[i]
            # Block, write it directly to result
            for _ in range(size):
                p_one.append(block_id)
            i += 1
        elif input[j][0] is None:
            # Space at the end doesn't matter, skip it
            j -= 1
        else:
            assert input[i][0] is None and input[j][0] is not None
            # Move the smaller of the space that we have or the total in J we can move
            c = min(input[i][1], input[j][1])
            for _ in range(c):
                p_one.append(input[j][0])
            input[i][1] -= c
            input[j][1] -= c
            if input[i][1] == 0:
                i += 1
            if input[j][1] == 0:
                j -= 1
    part_one = sum(i * v for i, v in enumerate(p_one))
    print(f"Part one: {part_one}")


def part_two():
    input = get_input()
    j = len(input) - 1
    while j >= 0:
        # print(j, input[j])
        if input[j][0] is None:
            # It's a space
            j -= 1
            continue
        for i in range(0, j):
            # print(j, i)
            if input[i][0] is not None:
                # print(f"{i} is a block, skipping")
                # It's a block
                continue
            if input[i][1] < input[j][1]:
                # print(f"{i} is too small (has {input[i][1]} needs {input[j][1]})")
                # The space is too small
                continue
            if input[i][1] == input[j][1]:
                # print(f"{i} is exactly right, {input[i][1]} == {input[j][1]}")
                # Easy, just swap the blocks
                input[i] = input[j]
                input[j] = [None, input[j][1]]
                j -= 1
            else:
                assert input[i][1] > input[j][1]
                assert input[i][0] is None
                # print(f"{i} is bigger (has {input[i][1]} needs {input[j][1]})")
                # First shrink input[i] to remove the space the block is going to take
                block_id, size = input[j]
                input[i][1] -= size
                # Zero out the old block while j is still pointing to the right place.
                input[j] = [None, input[j][1]]
                # Insert the block
                input.insert(i, [block_id, size])
                # j is now pointing to the previous index, so no need to decrement.
            break
        j -= 1

    p_two = 0
    idx = 0
    for block_id, size in input:
        if block_id is None:
            idx += size
        else:
            p_two += sum(block_id * (idx + v) for v in range(size))
            idx += size
    print(f"Part two: {p_two}")


part_one()
part_two()
