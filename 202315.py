from collections import defaultdict
from functools import reduce

with open("202315.txt", "r") as f:
    initseq = f.read().strip().split(",")


def hash(s):
    return reduce(lambda acc, c: ((acc + ord(c)) * 17) % 256, s, 0)


part_one = sum(hash(s) for s in initseq)
print(f"Part one: {part_one}")

# Take advantage of python dictionaries remembering the order in which elements
# were inserted.
boxes = defaultdict(dict)

for s in initseq:
    if (idx := s.find("-")) != -1:
        cmd = (s[:idx], "-")
    elif (idx := s.find("=")) != -1:
        cmd = (s[:idx], "=", int(s[idx + 1 :]))
    else:
        raise ValueError(f"Invalid command: {s}")

    match cmd:
        case (label, "-"):
            h = hash(label)
            if label in boxes[h]:
                del boxes[h][label]
        case (label, "=", value):
            h = hash(label)
            boxes[h][label] = value
        case _:
            raise ValueError(f"Invalid command: {cmd}")

part_two = sum(
    (box_id + 1) * (slot_id + 1) * focal_length
    for box_id, box in boxes.items()
    for slot_id, focal_length in enumerate(box.values())
)
print(f"Part two: {part_two}")
