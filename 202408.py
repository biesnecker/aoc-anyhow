from collections import defaultdict
from itertools import combinations
from typing import DefaultDict, List

from utils import coord_to_xy, input_as_strings_iter, xy_to_coord

stations: DefaultDict[str, List[complex]] = defaultdict(list)
max_x = max_y = 0
for y, line in enumerate(input_as_strings_iter("202408.txt")):
    for x, c in enumerate(line):
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        if c != ".":
            stations[c].append(xy_to_coord(x, y))

part_one: set[complex] = set()
part_two: set[complex] = set()
for station, coords in stations.items():
    if len(coords) == 1:
        continue

    # Add the stations themselves into the part_two set
    part_two.update(coords)

    for a, b in combinations(coords, 2):
        ax, ay = coord_to_xy(a)
        bx, by = coord_to_xy(b)

        sf = 1
        finished_c = False
        finished_d = False
        while True:
            if not finished_c:
                cx, cy = (sf + 1) * ax - sf * bx, (sf + 1) * ay - sf * by
                if cx >= 0 and cx <= max_x and cy >= 0 and cy <= max_y:
                    coord = xy_to_coord(cx, cy)
                    part_two.add(coord)
                    if sf == 1:
                        part_one.add(coord)
                else:
                    finished_c = True
            if not finished_d:
                dx, dy = (sf + 1) * bx - sf * ax, (sf + 1) * by - sf * ay
                if dx >= 0 and dx <= max_x and dy >= 0 and dy <= max_y:
                    coord = xy_to_coord(dx, dy)
                    part_two.add(coord)
                    if sf == 1:
                        part_one.add(coord)
                else:
                    finished_d = True

            if finished_c and finished_d:
                # both have gone off the map
                break
            # increment the scale factor
            sf += 1

print(f"Part one: {len(part_one)}")
print(f"Part two: {len(part_two)}")
