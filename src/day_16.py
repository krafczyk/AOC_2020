import argparse
import os
import sys
import re

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 16')
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

rule_re = re.compile("([a-z ]*): ([0-9]*)-([0-9]*) or ([0-9]*)-([0-9]*)")
ticket_re = re.compile("([0-9]+),?")

# Extract rules
rules = {}
i = 0
while lines[i].strip() != "":
    matches = rule_re.findall(lines[i])
    if len(matches) != 1:
        raise RuntimeError("Problem finding rule!")
    range1 = (int(matches[0][1]), int(matches[0][2]))
    range2 = (int(matches[0][3]), int(matches[0][4]))
    rules[matches[0][0]] = (range1, range2)
    i += 1

#print("Extracted rules:")
#print(rules)

i += 2

matches = ticket_re.findall(lines[i])
if len(matches) == 0:
    raise RuntimeError("Problem extracting my ticket!")

my_ticket = list(map(lambda s: int(s), matches))

#print(f"My ticket: {my_ticket}")

nearby_tickets = []

i += 3
while i < len(lines):
    matches = ticket_re.findall(lines[i])
    if len(matches) == 0:
        raise RuntimeError(f"Can't get ticket numbers from line {lines[i]}")
    nearby_tickets.append(list(map(lambda s: int(s), matches)))
    i += 1

#print("Nearby Ticktes:")
#print(nearby_tickets)

def follows_rule(number, rule):
    range1 = rule[0]
    if number >= range1[0] and number <= range1[1]:
        return True
    range2 = rule[1]
    if number >= range2[0] and number <= range2[1]:
        return True
    return False

invalid_total = 0
for ticket in nearby_tickets:
    for number in ticket:
        number_invalid = True
        for rule_name in rules:
            rule = rules[rule_name]
            if follows_rule(number, rule):
                number_invalid = False
                break
        if number_invalid:
            invalid_total += number

print(f"Day 16 task 1: {invalid_total}")
