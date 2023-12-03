import itertools

processing_rules = True
rules = {}
messages = []

with open("202019.txt", "r") as f:
    for line in f:
        if line == "\n":
            processing_rules = False
            continue
        if processing_rules:
            [rule_id, rule] = line.strip().split(": ")
            rule_id = int(rule_id)
            if rule[0] == '"':
                rules[rule_id] = rule[1]
            else:
                rules[rule_id] = [
                    list(map(int, option.split(" "))) for option in rule.split(" | ")
                ]
        else:
            messages.append(line.strip())

part_one = 0
generated = {}


def generate(rule_id):
    if rule_id in generated:
        return generated[rule_id]
    rule = rules[rule_id]

    # handle the string case
    if isinstance(rule, str):
        generated[rule_id] = [rule]
        return [rule]

    options = []

    # handle the list case
    for option in rule:
        for combo in itertools.product(*[generate(rule_id) for rule_id in option]):
            options.append("".join(combo))

    generated[rule_id] = options
    return set(options)


rule_zero = set(generate(0))
for message in messages:
    if message in rule_zero:
        part_one += 1

print(f"Part one: {part_one}")

part_two = 0

leftover = []
for message in messages:
    if message in rule_zero:
        part_two += 1
        continue
    leftover.append(message)

# Only rules 8 and 11 are recursive, and they're only depended on by rule 0.
# Rule 8 is "42 | 42 8", and rule 11 is "42 31 | 42 11 31".

# First check rule 8, which is just rule 42 repeated one or more times.

rule_42 = set(generate(42))

rule_31 = set(generate(31))


for message in leftover:
    matches_42 = 0
    matches_31 = 0
    while message[:8] in rule_42:
        matches_42 += 1
        message = message[8:]
    while message[:8] in rule_31:
        matches_31 += 1
        message = message[8:]
    if message == "" and matches_42 > matches_31 and matches_31 > 0:
        part_two += 1

print(f"Part two: {part_two}")
