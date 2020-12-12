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

D_map = {
    'N': np.array([0,1]),
    'S': np.array([0,-1]),
    'E': np.array([1,0]),
    'W': np.array([-1,0]),
}

Rot_R = np.array([[0, 1],[-1,0]])
Rot_L = np.array([[0, -1], [1, 0]])

dirs = ['N', 'S', 'E', 'W']
cur_dir = np.array([1,0])
cur_pos = np.array([0,0])

for direction in directions:
    if direction[0] in dirs:
        cur_pos += D_map[direction[0]]*direction[1]
    elif direction[0] == 'F':
        cur_pos += cur_dir*direction[1]
    elif direction[0] == 'R':
        num = direction[1]//90
        if num > 0:
            for i in range(num):
                cur_dir = np.matmul(Rot_R, cur_dir)
        else:
            for i in range(num):
                cur_dir = np.matmul(Rot_L, cur_dir)
    elif direction[0] == 'L':
        num = direction[1]//90
        if num > 0:
            for i in range(num):
                cur_dir = np.matmul(Rot_L, cur_dir)
        else:
            for i in range(num):
                cur_dir = np.matmul(Rot_R, cur_dir)
    else:
        raise RuntimeError("Unsupported direction: {direction}")

print(f"Day 12 task 1: Manhattan distance: {np.abs(cur_pos).sum()}")

waypoint_pos = np.array([10, 1])
cur_pos = np.array([0,0])

for direction in directions:
    if direction[0] in dirs:
        waypoint_pos += D_map[direction[0]]*direction[1]
    elif direction[0] == 'R':
        num = direction[1]//90
        if num > 0:
            for i in range(num):
                waypoint_pos = np.matmul(Rot_R, waypoint_pos)
        else:
            for i in range(num):
                waypoint_pos = np.matmul(Rot_L, waypoint_pos)
    elif direction[0] == 'L':
        num = direction[1]//90
        if num > 0:
            for i in range(num):
                waypoint_pos = np.matmul(Rot_L, waypoint_pos)
        else:
            for i in range(num):
                waypoint_pos = np.matmul(Rot_R, waypoint_pos)
    elif direction[0] == 'F':
        cur_pos += waypoint_pos*direction[1]
    else:
        raise RuntimeError("Unsupported direction: {direction}")

print(f"Day 12 task 2: Manhattan distance: {np.abs(cur_pos).sum()}")
