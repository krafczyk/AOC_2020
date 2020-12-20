import argparse
import os
import sys
import re
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 19')
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

rule_dict = {}
rule_re = re.compile("([0-9]*): (.*)")
# Find rules
for line in lines:
    matches = rule_re.findall(line.strip())
    if len(matches) != 1:
        continue
    line_num = int(matches[0][0])
    rule_line = matches[0][1]
    rule_dict[line_num] = rule_line

def multiply_string_lists(list_a, list_b):
    new_list = []
    for la in list_a:
        for lb in list_b:
            new_list.append(la+lb)
    return new_list

letter_re = re.compile("\"[a-z]\"")
def decompose_rule(rule):
    if letter_re.search(rule) is not None:
        return [str(rule[1])]
    else:
        # first, break the rule into sections separated by bars.
        rule_parts = rule.split('|')
        all_answers = []
        for part in rule_parts:
            part = part.strip().split(" ")
            section_answers = None
            for i in range(len(part)):
                new_answers = decompose_rule(rule_dict[int(part[i])])
                if section_answers is None:
                    section_answers = new_answers
                else:
                    section_answers = multiply_string_lists(section_answers, new_answers)
            if section_answers is None:
                raise RuntimeError("Strange Situation!")

            all_answers += section_answers
        return all_answers



num_rules = len(rule_dict.keys())
print(f"num_rules: {num_rules}")
messages = []
for line in lines[num_rules+1:]:
    messages.append(line.strip())

#print("Messages:")
#for message in messages:
#    print(message)


if rule_dict[0] != "8 11":
    rule_0_matches = decompose_rule(rule_dict[0])
    num_matches = 0
    for message in messages:
        if message in rule_0_matches:
            num_matches += 1
    print(f"Day 19 task 1: {num_matches}")
    print("Detected known test case, quitting")
    sys.exit(0)

rule_42_matches = decompose_rule(rule_dict[42])
rule_31_matches = decompose_rule(rule_dict[31])

num_match = 0
for message in messages:
    i = 0
    advance = False
    for seq in rule_42_matches:
        if message[i:i+len(seq)] == seq:
            i += len(seq)
            advance = True
            break
    if not advance:
        continue

    advance = False
    for seq in rule_42_matches:
        if message[i:i+len(seq)] == seq:
            i += len(seq)
            advance = True
            break
    if not advance:
        continue

    advance = False
    for seq in rule_31_matches:
        if message[i:i+len(seq)] == seq:
            i += len(seq)
            advance = True
            break
    if not advance:
        continue

    if i == len(message):
        num_match += 1

print(f"Day 19 task 1: {num_match}")

# From testing, we can see that rule 42 and 31 each have independent 
#print(set(rule_42_matches).intersection(set(rule_31_matches)))

num_match = 0
matches = []
for message in messages:
    num_42 = 0
    num_31 = 0
    i = 0
    while True:
        advance = False
        for seq in rule_42_matches:
            if message[i:i+len(seq)] == seq:
                i += len(seq)
                advance = True
                break
        if not advance:
            break
        else:
            num_42 += 1

    while True:
        advance = False
        for seq in rule_31_matches:
            if message[i:i+len(seq)] == seq:
                i += len(seq)
                advance=True
                break
        if not advance:
            break
        else:
            num_31 += 1

    if i != len(message):
        continue

    if num_42 > num_31 and num_31 >= 1:
        matches.append(message)
        num_match += 1

print(f"Day 19 task 2: {num_match}")
