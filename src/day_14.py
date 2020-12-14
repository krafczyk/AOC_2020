import argparse
import os
import sys
import re

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 14')
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

mask_re = re.compile("mask = ([01X]*)")
mem_re = re.compile("mem\[([0-9]*)\] = ([0-9]*)")

memory = {}

current_mask_A = 0
current_mask_B = 0
for line in lines:
    mask_matches = mask_re.findall(line)
    if len(mask_matches) > 0:
        mask_match = mask_matches[0]
        current_mask_A = int(mask_match.replace('X', '0'), 2)
        current_mask_B = int(mask_match.replace('X', '1'), 2)
    else:
        mem_matches = mem_re.findall(line)
        if len(mem_matches) != 1:
            raise RuntimeError("Problem matching line!")
        location = int(mem_matches[0][0])
        value = int(mem_matches[0][1])
        value = value | current_mask_A
        value = value & current_mask_B
        memory[location] = value

total = 0
for location in memory:
    total += memory[location]

print(f"Day 14 task 1: {total}")
