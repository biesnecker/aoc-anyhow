import re
from collections import defaultdict


class Block:
    def __init__(self, id, start, end):
        self.id = id
        x1, y1, z1 = start
        x2, y2, z2 = end
        self.x1 = min(x1, x2)
        self.x2 = max(x1, x2)
        self.y1 = min(y1, y2)
        self.y2 = max(y1, y2)
        self.z1 = min(z1, z2)
        self.z2 = max(z1, z2)

    def __repr__(self):
        return f"Block #{self.id} ({self.x1}, {self.y1}, {self.z1}, {self.x2}, {self.y2}, {self.z2})"

    def xy(self):
        for y in range(self.y1, self.y2 + 1):
            for x in range(self.x1, self.x2 + 1):
                yield (x, y)

    def height(self):
        return self.z2 - self.z1 + 1


blocks = []
with open("202322.txt", "r") as f:
    for i, line in enumerate(f):
        x1, y1, z1, x2, y2, z2 = map(int, re.findall(r"-?\d+", line))
        blocks.append(Block(i, (x1, y1, z1), (x2, y2, z2)))
blocks = sorted(blocks, key=lambda b: b.z1)

floor = defaultdict(lambda: (0, None))
supports = defaultdict(set)
supported_by = defaultdict(set)

for block in blocks:
    heights = defaultdict(list)
    for x, y in block.xy():
        (z, support) = floor[(x, y)]
        if z > 0:
            heights[z].append(support)
    if len(heights) > 0:
        max_height = max(heights.keys())
        for support in heights[max_height]:
            supports[support].add(block.id)
            supported_by[block.id].add(support)
    else:
        max_height = 0
    floor_height = max_height + block.height()
    for x, y in block.xy():
        floor[(x, y)] = (floor_height, block.id)

part_one = 0
for block in blocks:
    if len(supports[block.id]) == 0:
        part_one += 1  # this block doesn't support anything
    else:
        for b in supports[block.id]:
            # This block only has one supporter, so it will fall.
            if len(supported_by[b]) <= 1:
                break
        else:
            part_one += 1
print(f"Part one: {part_one}")


def would_fall(block_id):
    if len(supports[block_id]) == 0:
        return 0  # nothing will fall if this block doesn't support anything.
    falling = {b for b in supports[block_id] if len(supported_by[b]) == 1}
    all_falling = set(falling)
    while len(falling) > 0:
        new_falling = set()
        for block in falling:
            for b in supports[block]:
                if len(supported_by[b] - all_falling) == 0:
                    new_falling.add(b)
        all_falling |= new_falling
        falling = new_falling
    return len(all_falling)


part_two = sum(would_fall(block.id) for block in blocks)
print(f"Part two: {part_two}")
