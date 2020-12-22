import argparse
import os
import sys

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 22')
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

player1_deck = []
player2_deck = []

i = 1
while lines[i].strip() != "":
    player1_deck.append(int(lines[i].strip()))
    i += 1

i += 2
while i < len(lines):
    player2_deck.append(int(lines[i].strip()))
    i += 1

print(player1_deck)
print(player2_deck)

num_turns = 0
while (len(player1_deck) > 0) and (len(player2_deck) > 0):
    # Draw cards from top of deck
    p1_card = player1_deck.pop(0)
    p2_card = player2_deck.pop(0)
    if p1_card > p2_card:
        player1_deck.append(max(p1_card, p2_card))
        player1_deck.append(min(p1_card, p2_card))
    else:
        player2_deck.append(max(p1_card, p2_card))
        player2_deck.append(min(p1_card, p2_card))
    num_turns += 1

print(f"Took {num_turns} to finish!")

if len(player1_deck) > 0:
    winner_deck = player1_deck
else:
    winner_deck = player2_deck

total = 0
for i in range(len(winner_deck)):
    total += winner_deck[len(winner_deck)-1-i]*(i+1)

print(f"Day 22 task 1: {total}")
