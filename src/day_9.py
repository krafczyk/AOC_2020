import argparse
import os
import sys

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 9')
parser.add_argument('--input', help="Path to the input file", type=str, required=True)
parser.add_argument('--preamble-length', help="Length of the preamble", type=int, default=25)

# Parse Arguments
args = parser.parse_args()

# Get input filepath
input_filepath = args.input

# Check input file exists
if not os.path.exists(input_filepath):
    print(f"ERROR file {input_filepath} doesn't exist!")
    sys.exit(1)

with open(input_filepath, 'r') as f:
    nums = list(map(lambda l: int(l.strip()), f.readlines()))

print(f"Input is {len(nums)} numbers long")

preamble_len = args.preamble_length

print(f"Using preamble length of {preamble_len}")

for N in range(preamble_len, len(nums)):
    target_num = nums[N]
    is_valid = False
    for i in range(0, preamble_len-1):
        num_i = nums[N-(i+1)]
        for j in range(i+1, preamble_len):
            num_j = nums[N-(j+1)]
            if num_i+num_j == target_num:
                is_valid = True
                break
        if is_valid:
            break

    if not is_valid:
        print(f"Day 9 task 1: {target_num} is the first number that isn't the sum of two of the previous {preamble_len} numbers")
        break
