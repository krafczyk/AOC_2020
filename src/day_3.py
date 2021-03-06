import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 3')
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

ny = len(lines)
nx = len(lines[0].strip())

for line in lines:
    if len(line.strip()) != nx:
        raise RuntimeError("Invalid map! Some lines aren't of equal length!")

mx = 3
my = 1

def num_trees(mx, my):
    x = 0
    y = 0

    n_trees = 0
    while y < ny:
        if lines[y][x] == '#':
            n_trees += 1
        y = y+my
        x = (x+mx)%nx

    return n_trees

trees_1_1 = num_trees(1,1)
trees_3_1 = num_trees(3,1)
trees_5_1 = num_trees(5,1)
trees_7_1 = num_trees(7,1)
trees_1_2 = num_trees(1,2)

print(f"Day 3 task 1: {trees_3_1} trees.")

task_2 = trees_1_1*trees_3_1*trees_5_1*trees_7_1*trees_1_2

print(f"Day 3 task 2: {task_2}")
