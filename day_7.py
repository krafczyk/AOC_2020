import argparse
import os
import sys
import re

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 7')
parser.add_argument('--input', help="Path to the input file", type=str, required=True)

# Parse Arguments
args = parser.parse_args()

# Get input filepath
input_filepath = args.input

# Check input file exists
if not os.path.exists(input_filepath):
    print(f"ERROR file {input_filepath} doesn't exist!")
    sys.exit(1)

init_re = re.compile('([a-z]* [a-z]*) bags contain')
child_re = re.compile('([0-9]*) ([a-z]* [a-z]*) bags?')

with open(input_filepath, 'r') as f:
    lines = f.readlines()

# Read rule mapping in
rule_dict = {}
for line in lines:
    match = init_re.search(line.strip())
    bag_name = match.group(1)
    children = list(filter(lambda c: c[1] != 'no other',child_re.findall(line)))
    rule_dict[bag_name] = children

#for bag in rule_dict:
#    print(f"{bag} bags contain {rule_dict[bag]}")

# Get unique bag names
unique_bag_names = set()
for key in rule_dict:
    unique_bag_names.add(key)
    for child in rule_dict[key]:
        unique_bag_names.add(child[1])

def contains_bag(bag, target):
    for child in rule_dict[bag]:
        if child[1] == target:
            return True
        elif contains_bag(child[1], target):
            return True
    return False

num_1 = 0
target_bag = 'shiny gold'
for bag in unique_bag_names:
    if bag != target_bag:
        if contains_bag(bag, target_bag):
            num_1 += 1

print(f"Day 7 task 1: {num_1} bags contain {target_bag}")

