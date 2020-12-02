import argparse
import os
import sys
import re

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 2')
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

line_re = re.compile('(\d+)-(\d+) (.): (.*)$')

line_decomp = []
num_valid = 0
for line in lines:
    match = line_re.search(line)
    if not match:
        raise RuntimeError(f"Couldn't match line {line}")
    low = int(match.group(1))
    high = int(match.group(2))
    let = match.group(3)
    password = match.group(4)

    num_let = len(list(filter(lambda l: l == let, password)))

    if num_let >= low and num_let <= high:
        num_valid += 1

print(f"Task 1: There are {num_valid} valid passwords")
