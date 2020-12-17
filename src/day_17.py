import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 17')
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

# Report stats about input
print("Initial position:")
for line in lines:
    print(line.strip())

print(f"nx,ny: {nx},{ny}")

# Allocate Set
conway_set = set()

# Initialize set
for x in range(nx):
    for y in range(ny):
        if lines[y][x] == '#':
            conway_set.add((x,y,0))

print(f"conway_set: {conway_set}")

d = np.arange(-1,2)
mg = np.meshgrid(d, d, d)
D = np.stack(mg, axis=3).reshape((3**3,3))
D = D[np.apply_along_axis(np.sum, 1, np.apply_along_axis(np.abs, 1, np.abs(D)))!= 0]

def get_set_extent(conway_set):
    conway_list = list(conway_set)
    first_val = list(conway_set)[0]
    range_x = [first_val[0], first_val[0]]
    range_y = [first_val[1], first_val[1]]
    range_z = [first_val[2], first_val[2]]

    for pos in conway_list:
        range_x[0] = min(range_x[0], pos[0])
        range_x[1] = max(range_x[1], pos[0])
        range_y[0] = min(range_y[0], pos[1])
        range_y[1] = max(range_y[1], pos[1])
        range_z[0] = min(range_z[0], pos[2])
        range_z[1] = max(range_z[1], pos[2])
    return (range_x, range_y, range_z)

def display_set(conway_set, ranges=None):
    if ranges is None:
        ranges = get_set_extent(conway_set)

    range_x = ranges[0]
    range_y = ranges[1]
    range_z = ranges[2]

    for z in range(range_z[0],range_z[1]+1):
        print(f"z={z}")
        for y in range(range_y[0], range_y[1]+1):
            line = ""
            for x in range(range_x[0], range_x[1]+1):
                if (x,y,z) in conway_set:
                    line += '#'
                else:
                    line += '.'
            print(line)
        print()

print("Initial extent:")
print(get_set_extent(conway_set))

print("Initial state:")
display_set(conway_set)

num_steps = 0
while num_steps < 6:
    # Detect min/max values for each position
    (range_x, range_y, range_z) = get_set_extent(conway_set)

    new_conway_set = set()
    for x in range(range_x[0]-1, range_x[1]+2):
        for y in range(range_y[0]-1, range_y[1]+2):
            for z in range(range_z[0]-1, range_z[1]+2):
                pos = (x,y,z)
                neighbors = set(map(tuple, list(D+np.array(pos))))
                num_neighbors = len(neighbors.intersection(conway_set))
                if pos in conway_set:
                    if num_neighbors >= 2 and num_neighbors <= 3:
                        new_conway_set.add(pos)
                else:
                    if num_neighbors == 3:
                        new_conway_set.add(pos)
    num_steps += 1
    conway_set = new_conway_set

print(f"Day 17 task 1: {len(conway_set)}")

d = np.arange(-1,2)
mg = np.meshgrid(d, d, d, d)
D = np.stack(mg, axis=4).reshape((3**4,4))
D = D[np.apply_along_axis(np.sum, 1, np.apply_along_axis(np.abs, 1, np.abs(D)))!= 0]

def get_set_extent(conway_set):
    conway_list = list(conway_set)
    first_val = list(conway_set)[0]
    range_x = [first_val[0], first_val[0]]
    range_y = [first_val[1], first_val[1]]
    range_z = [first_val[2], first_val[2]]
    range_w = [first_val[3], first_val[3]]

    for pos in conway_list:
        range_x[0] = min(range_x[0], pos[0])
        range_x[1] = max(range_x[1], pos[0])
        range_y[0] = min(range_y[0], pos[1])
        range_y[1] = max(range_y[1], pos[1])
        range_z[0] = min(range_z[0], pos[2])
        range_z[1] = max(range_z[1], pos[2])
        range_w[0] = min(range_z[0], pos[3])
        range_w[1] = max(range_z[1], pos[3])
    return (range_x, range_y, range_z, range_w)

def display_set(conway_set, ranges=None):
    if ranges is None:
        ranges = get_set_extent(conway_set)

    range_x = ranges[0]
    range_y = ranges[1]
    range_z = ranges[2]
    range_w = ranges[3]

    for w in range(range_w[0],range_w[1]+1):
        for z in range(range_z[0],range_z[1]+1):
            print(f"z={z}, w={w}")
            for y in range(range_y[0], range_y[1]+1):
                line = ""
                for x in range(range_x[0], range_x[1]+1):
                    if (x,y,z) in conway_set:
                        line += '#'
                    else:
                        line += '.'
                print(line)
            print()

conway_set = set()

# Initialize set
for x in range(nx):
    for y in range(ny):
        if lines[y][x] == '#':
            conway_set.add((x,y,0,0))

num_steps = 0
while num_steps < 6:
    # Detect min/max values for each position
    (range_x, range_y, range_z, range_w) = get_set_extent(conway_set)

    new_conway_set = set()
    for x in range(range_x[0]-1, range_x[1]+2):
        for y in range(range_y[0]-1, range_y[1]+2):
            for z in range(range_z[0]-1, range_z[1]+2):
                for w in range(range_w[0]-1, range_w[1]+2):
                    pos = (x,y,z,w)
                    neighbors = set(map(tuple, list(D+np.array(pos))))
                    num_neighbors = len(neighbors.intersection(conway_set))
                    if pos in conway_set:
                        if num_neighbors >= 2 and num_neighbors <= 3:
                            new_conway_set.add(pos)
                    else:
                        if num_neighbors == 3:
                            new_conway_set.add(pos)
    num_steps += 1
    conway_set = new_conway_set

print(f"Day 17 task 2: {len(conway_set)}")
