import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 13')
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

earliest_timestamp = int(lines[0].strip())

bus_list = list(map(lambda s: int(s), filter(lambda s: s != 'x', lines[1].strip().split(','))))

bus_nums = np.array(bus_list)
time_to_next = bus_nums*((earliest_timestamp//bus_nums)+1)-earliest_timestamp
i_bus = np.argmin(time_to_next, axis=0)

print(f"Day 13 task 1: {bus_nums[i_bus]*time_to_next[i_bus]}")
