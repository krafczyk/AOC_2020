import argparse
import os
import sys

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 1')
parser.add_argument('--input', help="Path to the input file", type=str, required=True)

# Parse Arguments
args = parser.parse_args()

# Get input filepath
input_filepath = args.input

# Check input file exists
if not os.path.exists(input_filepath):
    print(f"ERROR file {input_filepath} doesn't exist!")
    sys.exit(1)

# Read file
with open(input_filepath, 'r') as f:
    lines = f.readlines()

numbers = list(map(lambda s: int(s), lines))

print(f"There are {len(numbers)} numbers.")

found = False
for i in range(len(numbers)):
    num_i = numbers[i]
    for j in range(i+1,len(numbers)):
        num_j = numbers[j]
        if num_i+num_j == 2020:
            print(f"Found the numbers! {num_i} and {num_j} sum to 2020!")
            print(f"Day 1 task 1 solution: {num_i*num_j}")
            found = True
            break
    if found:
        break

if not found:
    print("ERROR! There aren't two numbers in the input data which sum to 2020!")

found = False
for i in range(len(numbers)):
    num_i = numbers[i]
    for j in range(i+1, len(numbers)):
        num_j = numbers[j]
        for k in range(j+1, len(numbers)):
            num_k = numbers[k]
            if num_i+num_j+num_k == 2020:
                print(f"Found the numbers! {num_i}, {num_j}, and {num_k} sum to 2020!")
                print(f"Day 1 task 2 solution: {num_i*num_j*num_k}")
                found = True
                break
        if found:
            break
    if found:
        break

if not found:
    print("ERROR! There aren't three numbers in the input data which sum to 2020!")
