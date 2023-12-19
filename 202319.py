import math
import re

with open("202319.txt", "r") as f:
    [workflows_raw, parts_raw] = f.read().split("\n\n")
    first_workflow = None
    workflows = {}
    for w in workflows_raw.strip().split("\n"):
        [label, rest] = w.strip().split("{")
        rules = []
        for r in rest[:-1].split(","):
            if r == "A" or r == "R":
                rules.append(r)
            elif m := re.match(r"([a-z])([\>|\<])(\d+):(\w+)", r):
                rules.append((m.group(1), m.group(2), int(m.group(3)), m.group(4)))
            else:
                rules.append(("J", r))
        workflows[label] = rules
        if first_workflow is None:
            first_workflow = label

    parts = []
    for p in parts_raw.strip().split("\n"):
        res = {}
        for attr in p.strip()[1:-1].split(","):
            [name, value] = attr.split("=")
            res[name] = int(value)
        parts.append(res)


def accept_reject(workflows, part):
    current = "in"
    while True:
        rules = workflows[current]
        for rule in rules:
            match rule:
                case "A":
                    return True
                case "R":
                    return False
                case ("J", label):
                    current = label
                    break
                case (attr, ">", value, label):
                    if part[attr] > value:
                        if label == "A":
                            return True
                        elif label == "R":
                            return False
                        else:
                            current = label
                            break
                case (attr, "<", value, label):
                    if part[attr] < value:
                        if label == "A":
                            return True
                        elif label == "R":
                            return False
                        else:
                            current = label
                            break
                case unmatched:
                    raise ValueError(f"Unmatched rule: {unmatched}")


def combos(workflows):
    s = [("in", {k: (1, 4000) for k in "xmas"})]
    accepted = []

    while s:
        (wf, part) = s.pop()
        rules = workflows[wf]
        for rule in rules:
            match rule:
                case "A":
                    # Accepted unconditionally.
                    accepted.append(part)
                    break
                case "R":
                    # Rejected unconditionally.
                    break
                case ("J", label):
                    # Jump to another workflow without altering the ranges.
                    s.append((label, part))
                    break
                case (attr, ">", value, label) if part[attr][0] > value:
                    # The range is entirely above the value, so we can pass it all on.
                    if label == "A":
                        accepted.append(part)
                        break
                    elif label == "R":
                        break
                    else:
                        s.append((label, part))
                        break
                case (attr, ">", value, label) if part[attr][1] <= value:
                    # The range is entirely below the value, so we can ignore this rule.
                    continue
                case (attr, ">", value, label):
                    # The range is partially above the value, so we need to split it.
                    if label == "A":
                        accepted.append({**part, attr: (value + 1, part[attr][1])})
                    elif label != "R":
                        s.append((label, {**part, attr: (value + 1, part[attr][1])}))
                    # Now adjust the range to what's below the value.
                    part[attr] = (part[attr][0], value)
                case (attr, "<", value, label) if part[attr][1] < value:
                    # The range is entirely below the value, so we can pass it all on.
                    if label == "A":
                        accepted.append(part)
                        break
                    elif label == "R":
                        break
                    else:
                        s.append((label, part))
                        break
                case (attr, "<", value, label) if part[attr][0] >= value:
                    # The range is entirely above the value, so we can ignore this rule.
                    continue
                case (attr, "<", value, label):
                    # The range is partially below the value, so we need to split it.
                    if label == "A":
                        accepted.append({**part, attr: (part[attr][0], value - 1)})
                    elif label != "R":
                        s.append((label, {**part, attr: (part[attr][0], value - 1)}))
                    # Now adjust the range to what's above the value.
                    part[attr] = (value, part[attr][1])
                case unmatched:
                    raise ValueError(f"Unmatched rule: {unmatched}")
    return sum(math.prod(a[c][1] - a[c][0] + 1 for c in "xmas") for a in accepted)


part_one = sum(sum(part.values()) for part in parts if accept_reject(workflows, part))
print(f"Part one: {part_one}")
part_two = combos(workflows)
print(f"Part two: {part_two}")
