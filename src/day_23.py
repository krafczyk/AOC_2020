import argparse
import os
import sys
import numpy as np
import time

class Cup(object):
    def __init__(self, number):
        self.left = None
        self.right = None
        self.number = number

    def __str__(self):
        return f"{self.number}"

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 23')
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

initial = []
for char in lines[0].strip():
    num = int(char)
    initial.append(num)

def decrement(num, max_num):
    return ((num-2)%max_num)+1

def build_cup_map(initial):
    # Build cup map
    cup_map = {}
    for num in initial:
        cup_map[num] = Cup(num)

    # hook up cups
    cup0 = cup_map[initial[0]]
    cup0.right = cup_map[initial[1]]
    cup0.left = cup_map[initial[-1]]

    cupl = cup_map[initial[-1]]
    cupl.right = cup_map[initial[0]]
    cupl.left = cup_map[initial[-2]]

    for i in range(1,len(initial)-1):
        cupi = cup_map[initial[i]]
        cupi.left = cup_map[initial[i-1]]
        cupi.right = cup_map[initial[i+1]]

    return cup_map

def run_step(cup_map, current_cup, max_element):
    preserve_grp_l = current_cup.right
    preserve_grp_r = cup_map[preserve_grp_l.number].right.right
    preserved_nums = [
        preserve_grp_l.number,
        preserve_grp_l.right.number,
        preserve_grp_l.right.right.number
    ]

    destination = decrement(current_cup.number, max_element)
    while destination in preserved_nums:
        destination = decrement(destination, max_element)

    # Remove preserved section
    current_cup.right = preserve_grp_r.right
    preserve_grp_r.right.left = current_cup

    # Add preserved section back
    destination_node = cup_map[destination]
    destination_node_neighbor = destination_node.right 
    destination_node.right = preserve_grp_l
    preserve_grp_l.left = destination_node
    destination_node_neighbor.left = preserve_grp_r
    preserve_grp_r.right = destination_node_neighbor

    return current_cup.right

def run_steps(cup_map, current_cup, num_steps, max_element):
    step_i = 0
    while step_i < num_steps:
        current_cup = run_step(cup_map, current_cup, max_element)
        step_i += 1
    return current_cup

cup_map_1 = build_cup_map(initial)
current_cup = cup_map_1[initial[0]]

run_steps(cup_map_1, current_cup, 100, 9)

result = ""
node = cup_map_1[1]
while node.right != cup_map_1[1]:
    result = result+f"{node.right.number}"
    node = node.right

print(f"Day 23 task 1: {result}")

# Extend cups
for i in range(10,1000000+1):
   initial.append(i)

cup_map_2 = build_cup_map(initial)
current_cup = cup_map_2[initial[0]]

run_steps(cup_map_2, current_cup, 10000000, 1000000)

val_1 = cup_map_2[1].right.number
val_2 = cup_map_2[1].right.right.number

print(f"val_1: {val_1}")
print(f"val_2: {val_2}")
print(f"Day 23 task 2: {val_1*val_2}")
