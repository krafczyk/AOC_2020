import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 12')
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

directions = []
for line in lines:
    directions.append((line[0], int(line[1:])))

Ds = [
    np.array([1,0]),
    np.array([0,-1]),
    np.array([-1,0]),
    np.array([0, 1]),
]

D_map = {
    'N': np.array([0,1]),
    'S': np.array([0,-1]),
    'E': np.array([1,0]),
    'W': np.array([-1,0]),
}

dirs = ['N', 'S', 'E', 'W']
cur_dir = 0
cur_pos = np.array([0,0])

for direction in directions:
    if direction[0] in dirs:
        cur_pos += D_map[direction[0]]*direction[1]
    elif direction[0] == 'F':
        cur_pos += Ds[cur_dir]*direction[1]
    elif direction[0] == 'R':
        cur_dir = ((cur_dir+(direction[1]//90))%4)
    elif direction[0] == 'L':
        cur_dir = ((cur_dir-(direction[1]//90))%4)
    else:
        raise RuntimeError("Unsupported direction: {direction}")

print(f"Day 12 task 1: Manhattan distance: {np.abs(cur_pos).sum()}")
