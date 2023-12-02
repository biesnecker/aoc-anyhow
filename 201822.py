import heapq
import math

maxX = 2000
maxY = 2000

# input
with open("201822.txt", "r") as f:
    lines = f.readlines()
    depth = int(lines[0].split(" ")[1])
    [targetX, targetY] = map(int, lines[1].split(" ")[1].split(","))

erosion = [[None] * maxX for _ in range(maxY)]
erosion[0][0] = 0
erosion[targetX][targetY] = 0


def get_erosion_level(x, y, depth):
    if erosion[x][y] is not None:
        return erosion[x][y]
    if x == 0 and y == 0:
        geo = 0
    elif x == 0:
        geo = y * 48271
    elif y == 0:
        geo = x * 16807
    else:
        geo = get_erosion_level(x - 1, y, depth) * get_erosion_level(x, y - 1, depth)
    erosion[x][y] = (geo + depth) % 20183
    return erosion[x][y]


def get_risk(x, y, depth):
    return get_erosion_level(x, y, depth) % 3


part_one = sum(
    get_risk(x, y, depth) for x in range(targetX + 1) for y in range(targetY + 1)
)
print(f"Part one: {part_one}")

part_two = math.inf
# Tool: 0 = neither, 1 = torch, 2 = climbing gear
visited = set()

q = [(0, 0, 0, 1)]  # (time, distance, x, y, tool)
while q:
    time, x, y, tool = heapq.heappop(q)
    if time >= part_two:
        continue
    if (x, y, tool) in visited:
        continue
    visited.add((x, y, tool))
    if x == targetX and y == targetY:
        if tool != 1:  # need to have torch to find the target
            time += 7
        if time < part_two:
            part_two = time
        continue
    for new_x, new_y in [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)]:
        # Don't go out of bounds
        if new_x < 0 or new_y < 0 or new_x >= maxX or new_y >= maxY:
            continue
        # If the new square allows the tool we have, move there.
        if (
            tool != get_risk(new_x, new_y, depth)
            and (new_x, new_y, tool) not in visited
        ):
            heapq.heappush(q, (time + 1, new_x, new_y, tool))
            continue
        for possible_tool in range(3):
            if possible_tool == tool:
                continue  # already using this tool.
            elif possible_tool == get_risk(x, y, depth):
                continue  # can't switch to this tool in this square.
            elif possible_tool == get_risk(new_x, new_y, depth):
                continue  # can't use this tool in the new square.
            elif (new_x, new_y, possible_tool) not in visited:
                heapq.heappush(q, (time + 8, new_x, new_y, possible_tool))
print(f"Part two: {part_two}")
