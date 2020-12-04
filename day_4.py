import argparse
import os
import sys
import re

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 4')
parser.add_argument('--input', help="Path to the input file", type=str, required=True)

# Parse Arguments
args = parser.parse_args()

# Get input filepath
input_filepath = args.input

# Check input file exists
if not os.path.exists(input_filepath):
    print(f"ERROR file {input_filepath} doesn't exist!")
    sys.exit(1)

# Load passport data
with open(input_filepath, 'r') as f:
    data = f.read()

passports = data.split('\n\n')

passport_component_re = re.compile("([^ \n]*):[^ \n]*")

required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']
optional_fields = ['cid']

num_valid_passports = 0
for passport in passports:
    passport_fields = passport_component_re.findall(passport)

    valid = True
    for field in required_fields:
        if field not in passport_fields:
            valid = False
            break

    if valid:
        num_valid_passports += 1

print(f"Day 4 task 1: {num_valid_passports} valid passports")
