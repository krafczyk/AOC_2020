import argparse
import os
import sys
import numpy as np

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

invalid_num = 0
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
        invalid_num = target_num
        break

print(f"Day 9 task 1: {invalid_num} is the first invalid number.")

nums = np.array(nums)
print(f"nums shape: {nums.shape}")
for L in range(2, len(nums)):
    print(f"Checking sums of length: {L}")
    sums = np.zeros((len(nums)-(L-1)))
    for i in range(0, L):
        sums += nums[i:i+(len(nums)-L+1)]
    Is = np.where(sums == invalid_num)[0]
    if Is.shape[0] > 0:
        i = Is[0]
        Range = nums[i:i+L]
        largest = Range.max()
        smallest = Range.min()
        print(f"Day 9 task 2: encryption weakness is: {largest+smallest}")
        break
