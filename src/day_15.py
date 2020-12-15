import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 15')
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

nums = list(map(lambda s: int(s), lines[0].split(',')))

nums_array = np.array(nums)

while len(nums) < 2020:
    last_where = np.where(nums_array == nums_array[-1])[0]
    if len(last_where) == 1:
        nums.append(0)
    else:
        nums.append(last_where[-1]-last_where[-2])
    nums_array = np.array(nums)

print(f"Day 15 task 1: {nums_array[-1]}")
