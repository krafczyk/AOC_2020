import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 5')
parser.add_argument('--input', help="Path to the input file", type=str, required=True)

# Parse Arguments
args = parser.parse_args()

# Get input filepath
input_filepath = args.input

# Check input file exists
if not os.path.exists(input_filepath):
    print(f"ERROR file {input_filepath} doesn't exist!")
    sys.exit(1)

nrows = 128
ncols = 8

with open(input_filepath, 'r') as f:
    lines = f.readlines()

seat_ids = []
max_seat_id = 0
for line in lines:
    row_data = line[:7]
    row_data = row_data.replace('F', '0')
    row_data = row_data.replace('B', '1')
    row = int(row_data, 2)
    col_data = line[7:]
    col_data = col_data.replace('L', '0')
    col_data = col_data.replace('R', '1')
    col = int(col_data, 2)

    seat_id = row*8+col
    if seat_id > max_seat_id:
        max_seat_id = seat_id

    seat_ids.append(seat_id)

print(f"Task 1: {max_seat_id}")

# Sort them
seat_ids = sorted(seat_ids)
seat_arr = np.array(seat_ids)
diffs = seat_arr[1:]-seat_arr[:len(seat_ids)-1]
spots = np.where(diffs==2)
idx = spots[0][0]

print(f"Task 2: {seat_ids[idx]+1}")
