import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 10')
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
    joltages = np.array(list(map(lambda s: int(s.strip()), f.readlines())))

print(f"Number of Joltage adapters: {len(joltages)}")

num_dict = {}
for i in range(joltages.shape[0]):
    joltage = joltages[i]
    num_dict[joltage] = num_dict.get(joltage, 0)+1

print(f"There are {len(num_dict.keys())} unique joltages")

max_number = 0
for key in num_dict:
    if num_dict[key] > max_number:
        max_number = num_dict[key]

print(f"There are at most {max_number} versions of one joltage adapter.")

max_joltage = joltages.max()

joltages = np.append(joltages, [0, max_joltage+3])
sorted_joltages = np.sort(joltages)

differences = sorted_joltages[1:]-sorted_joltages[:-1]

num_1_diffs = np.where(differences == 1)[0].shape[0]
num_3_diffs = np.where(differences == 3)[0].shape[0]

print(sorted_joltages)

print(f"{num_1_diffs} differences of 1 jolt")
print(f"{num_3_diffs} differences of 3 jolts")
print(f"Day 10 task 1: {num_1_diffs*num_3_diffs}")
