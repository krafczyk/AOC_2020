import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 11')
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

nx = len(lines[0].strip())
ny = len(lines)

# Initialize memory
seat_map = np.zeros((nx, ny), dtype=np.uint8)
new_seat_map = np.zeros((nx, ny), dtype=np.uint8)

# Initialize map
for j in range(ny):
    for i in range(nx):
        seat_map[i, j] = ord(lines[j][i])

print("Initial Map:")
def show_map(seat_map):
    for j in range(ny):
        line = ""
        for i in range(nx):
            line += chr(seat_map[i, j])
        print(line)
show_map(seat_map)

def count_occupied_neighbors(i, j, seat_map):
    num_occupied = 0
    for dx in range(-1,2):
        for dy in range(-1, 2):
            if (dx == dy) and (dx == 0):
                # Skip middle point
                continue
            I = i+dx
            J = j+dy
            if I < 0 or J < 0:
                continue
            if I >= nx or J >= ny:
                continue
            if chr(seat_map[I,J]) == '#':
                num_occupied += 1
    return num_occupied

num_rounds = 0
while True:
    # Build new map
    for i in range(nx):
        for j in range(ny):
            #print(f"position: {i},{j}")
            seat_char = chr(seat_map[i,j])
            if seat_char == '.':
                new_seat_map[i,j] = ord('.')
            elif seat_char == 'L':
                neighbors_occupied = count_occupied_neighbors(i, j, seat_map)
                #print(f'number of neighbors: {neighbors_occupied}')
                if neighbors_occupied == 0:
                    new_seat_map[i,j] = ord('#')
                else:
                    new_seat_map[i,j] = ord('L')
            elif seat_char == '#':
                neighbors_occupied = count_occupied_neighbors(i, j, seat_map)
                #print(f'number of neighbors: {neighbors_occupied}')
                if neighbors_occupied >= 4:
                    new_seat_map[i,j] = ord('L')
                else:
                    new_seat_map[i,j] = ord('#')
            else:
                raise RuntimeError("This shouldn't happen.")
    # Iterate counter
    num_rounds += 1
    # Check for repetition
    if np.all(new_seat_map == seat_map):
        break
    # Swap buffers
    temp = new_seat_map
    new_seat_map = seat_map
    seat_map = temp

num_occupied = 0
for i in range(nx):
    for j in range(ny):
        if seat_map[i,j] == ord('#'):
            num_occupied += 1

print(f"Day 11 task 1: Map repeats after {num_rounds} rounds. There are {num_occupied} seats occupied.")
show_map(seat_map)
