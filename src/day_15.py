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

print(nums)

times_spoke = {}

for i in range(len(nums)):
    times_spoke[nums[i]] = [i]

num_said = 3
last_said = nums[-1]

def say_number(last_said, num_said):
    array = times_spoke[last_said]
    if len(array) == 1:
        # If last number was said only once, say 0
        said = 0
    else:
        said = array[-1]-array[-2]
    array = times_spoke.get(said, [])
    array.append(num_said)
    if len(array) > 2:
        del array[0]
    times_spoke[said] = array
    return said

while num_said < 2020:
    last_said = say_number(last_said, num_said)
    num_said += 1

print(f"Day 15 task 1: {last_said}")

while num_said < 30000000:
    last_said = say_number(last_said, num_said)
    num_said += 1

print(f"Day 15 task 2: {last_said}")
