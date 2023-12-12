from collections import Counter

options = {}
all_ingredients = Counter()
with open("202021.txt", "r") as f:
    for line in f:
        ingredients, allergens = line.strip().split(" (contains ")
        ingredients = ingredients.split()
        for ingredient in ingredients:
            all_ingredients[ingredient] += 1
        allergens = allergens[:-1].split(", ")
        for allergen in allergens:
            if allergen not in options:
                options[allergen] = set(ingredients)
            else:
                options[allergen] &= set(ingredients)

while not all(len(v) == 1 for v in options.values()):
    for allergen, ingredients in options.items():
        if len(ingredients) == 1:
            for other_allergen, other_ingredients in options.items():
                if other_allergen != allergen:
                    other_ingredients -= ingredients

all_allergens = {k: next(iter(v)) for k, v in options.items()}
part_one = sum(
    v for k, v in all_ingredients.items() if k not in set(all_allergens.values())
)
print(f"Part one: {part_one}")

part_two = ",".join(v for _, v in sorted(all_allergens.items(), key=lambda x: x[0]))
print(f"Part two: {part_two}")
