import argparse
import os
import sys
import re
import string

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

passport_component_re = re.compile("([^ \n]*):([^ \n]*)")

required_fields = ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid']

def year_validator(low_yr, high_yr):
    def _validator(data):
        if len(data) != 4:
            return False
        for i in range(4):
            if data[i] not in string.digits:
                return False
        yr = int(data)
        if yr < low_yr:
            return False
        if yr > high_yr:
            return False
        return True
    return _validator

height_re = re.compile("([0-9]*)(cm|in)")

def height_validator(data):
    match = height_re.search(data)
    if match is None:
        return False
    num = int(match.group(1))
    unit = match.group(2)
    if unit == 'cm':
        if num < 150:
            return False
        if num > 193:
            return False
        return True
    elif unit == 'in':
        if num < 59:
            return False
        if num > 76:
            return False
        return True
    return False

def hcl_validator(data):
    if len(data) != 7:
        return False
    if data[0] != '#':
        return False
    for i in range(6):
        if data[i+1] not in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']:
            return False
    return True

def ecl_validator(data):
    if data not in ['amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth']:
        return False
    else:
        return True

def pid_validator(data):
    if len(data) != 9:
        return False
    for i in range(9):
        if data[i] not in string.digits:
            return False
    return True

field_validators = {
    'byr': year_validator(1920, 2002),
    'iyr': year_validator(2010, 2020),
    'eyr': year_validator(2020, 2030),
    'hgt': height_validator,
    'hcl': hcl_validator,
    'ecl': ecl_validator,
    'pid': pid_validator,
}

num_valid_passports_1 = 0
num_valid_passports_2 = 0
for passport in passports:
    passport_data = passport_component_re.findall(passport)
    passport_dict = {}
    for d in passport_data:
        passport_dict[d[0]] = d[1]

    valid_1 = True
    valid_2 = True
    for field in required_fields:
        if field not in passport_dict.keys():
            valid_1 = False
            valid_2 = False
            break
        else:
            if not field_validators[field](passport_dict[field]):
                valid_2 = False
                break

    if valid_1:
        num_valid_passports_1 += 1

    if valid_2:
        num_valid_passports_2 += 1

print(f"Day 4 task 1: {num_valid_passports_1} valid passports")
print(f"Day 4 task 2: {num_valid_passports_2} valid passports")
