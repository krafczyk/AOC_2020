import argparse
import os
import sys
import re

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 21')
parser.add_argument('--input', help="Path to the input file", type=str, required=True)

# Parse Arguments
args = parser.parse_args()

# Get input filepath
input_filepath = args.input

# Check input file exists
if not os.path.exists(input_filepath):
    print(f"ERROR file {input_filepath} doesn't exist!")
    sys.exit(1)

with open(input_filepath, 'r') as f:
    lines = f.readlines()

recipe_re = re.compile("^([a-z ]*) \(contains ([a-z\, ]*)\)$")
items_re = re.compile("([a-z]+)")

food_list = []
for line in lines:
    match = recipe_re.match(line.strip())
    if match is None:
        raise RuntimeError("Error matching food recipe")
    ingredients = set(items_re.findall(match.group(1)))
    allergens = set(items_re.findall(match.group(2)))
    food_list.append((ingredients, allergens))

def render_set(the_set):
    line = ""
    for item in the_set:
        line += item+" "
    return line

#print("Found the following foods:")
#for food in food_list:
#    print(f"{render_set(food[0])} (contains {render_set(food[1])})")

# Build set of all allergens
allergens = set()
ingredients = set()
for food in food_list:
    ingredients = ingredients.union(food[0])
    allergens = allergens.union(food[1])

#print(f"Found these ingredients: {ingredients}")
#print(f"Found these allergens: {allergens}")

# Build restricted set of allergens.
allergen_possibilities = {}
for food in food_list:
    food_allergens = food[1]
    food_ingredients = food[0]
    for allergen in food_allergens:
        possibilities = allergen_possibilities.get(allergen, None)
        if possibilities is None:
            possibilities = food_ingredients
        else:
            possibilities = possibilities.intersection(food_ingredients)
        allergen_possibilities[allergen] = possibilities

#print("Found the following allergen possibilities")
#print(allergen_possibilities)

all_possible_allergens = set()
for allergen in allergen_possibilities:
    all_possible_allergens = all_possible_allergens.union(allergen_possibilities[allergen])

#print("Found the following suspicious ingredients:")
#print(all_possible_allergens)

#print("These ingredients can't have any allergens:")
non_allergenics = ingredients.difference(all_possible_allergens)
#print(non_allergenics)

count_occurances = 0
for food in food_list:
    for ingredient in non_allergenics:
        if ingredient in food[0]:
            count_occurances += 1

print(f"Day 21 task 1: {count_occurances}")

allergen_possibilities_only_allergens = {}
for allergen in allergen_possibilities:
    allergen_possibilities_only_allergens[allergen] = allergen_possibilities[allergen].difference(non_allergenics)

allergen_map = {}

while len(allergen_possibilities_only_allergens) > 0:
    found_allergen = None
    found_ingredient = None
    for allergen in allergen_possibilities_only_allergens:
        if len(allergen_possibilities_only_allergens[allergen]) == 1:
            found_allergen = allergen
            found_ingredient = list(allergen_possibilities_only_allergens[allergen])[0]
            allergen_map[found_allergen] = found_ingredient
            break
    if found_allergen is None:
        raise RuntimeError("Should always find at least one allergen")
    # Remove the found allergen
    del allergen_possibilities_only_allergens[found_allergen]
    # Remove the found ingredient
    for allergen in allergen_possibilities_only_allergens:
        allergen_possibilities_only_allergens[allergen] = allergen_possibilities_only_allergens[allergen].difference(set([found_ingredient]))

canonical_dangerous_ingredient_list = ','.join(list(map(lambda a: allergen_map[a], sorted(list(allergen_map.keys())))))
print(f"Day 21 task 2: {canonical_dangerous_ingredient_list}")


