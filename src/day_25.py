import argparse
import os
import sys

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 25')
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

try:
    pub_key_1 = int(lines[0].strip())
    pub_key_2 = int(lines[1].strip())
except Exception as e:
    print(f"There was an error reading the input data!")
    raise e

subject_number = 7
div = 20201227

def find_loop_number(pub_key):
    value = 1
    loop_number = 0
    while value != pub_key:
        value *= 7
        value = value%div
        loop_number += 1

    return loop_number

loop_number_1 = find_loop_number(pub_key_1)
loop_number_2 = find_loop_number(pub_key_2)
print(f"loop number 1: {loop_number_1}")
print(f"loop number 2: {loop_number_2}")

i = 0
v = 1
while i < loop_number_1:
    v *= pub_key_2
    v = v%div
    i += 1

print(f"Day 25 task 1: {v}")

i = 0
v = 1
while i < loop_number_2:
    v *= pub_key_1
    v = v%div
    i += 1

print(f"Day 25 task 1: {v}")
