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

def ticket_is_valid(ticket):
    ticket_invalid = False
    for number in ticket:
        number_invalid = True
        for rule_name in rules:
            rule = rules[rule_name]
            if follows_rule(number, rule):
                number_invalid = False
                break
        if number_invalid:
            ticket_invalid = True
            break
    return not ticket_invalid

valid_nearby_tickets = list(filter(ticket_is_valid, nearby_tickets))

# Figure out which rules match all tickets in each ticket field.
valid_rules = {}
number_of_fields = len(valid_nearby_tickets[0])
for i in range(number_of_fields):
    for rule_name in rules:
        rule = rules[rule_name]
        valid_rule = True
        for ticket in valid_nearby_tickets:
            number = ticket[i]
            if not follows_rule(number, rule):
                valid_rule = False
                break
        if valid_rule:
            rule_list = valid_rules.get(i, [])
            rule_list.append(rule_name)
            valid_rules[i] = rule_list

print("valid rule map:")
print(valid_rules)

# Reduce map to final map
rule_field_map = {}
while len(valid_rules) > 0:
    # Find the field with only one rule
    next_field = None
    for field_i in valid_rules:
        if len(valid_rules[field_i]) == 1:
            next_field = field_i
            break
    if next_field is None:
        raise RuntimeError("Weird situation!")

    next_rule_name = valid_rules[next_field][0]
    rule_field_map[next_rule_name] = next_field

    # Clean the valid_rules map
    for i in range(number_of_fields):
        if i in valid_rules:
            rules_list = valid_rules[i]
            try:
                idx = rules_list.index(next_rule_name)
            except:
                continue
            del rules_list[idx]
            if len(rules_list) == 0:
                del valid_rules[i]
            else:
                valid_rules[i] = rules_list

print("field map:")
print(rule_field_map)

part_2_sol = 1
starts_with = 'departure'
for rule_name in rule_field_map:
    if rule_name[:len(starts_with)] == starts_with:
        part_2_sol *= my_ticket[rule_field_map[rule_name]]

print(my_ticket)
print(f"Day 16 part 2: {part_2_sol}")
