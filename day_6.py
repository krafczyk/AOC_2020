import argparse
import os
import sys

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 6')
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
    group_forms = f.read().split('\n\n')

sum_1 = 0
for group_form in group_forms:
    counts = {}
    forms = group_form.replace('\n', '')
    for i in range(len(forms)):
        let = forms[i]
        counts[let] = counts.get(let, 0)+1

    sum_1 += len(counts.keys())

print(f"Day 6 task 1: {sum_1}")
