import argparse
import os
import sys
import copy
import numpy as np

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

init_player1_deck = []
init_player2_deck = []

i = 1
while lines[i].strip() != "":
    init_player1_deck.append(int(lines[i].strip()))
    i += 1

i += 2
while i < len(lines):
    init_player2_deck.append(int(lines[i].strip()))
    i += 1

player1_deck = np.array(init_player1_deck)
player2_deck = np.array(init_player2_deck)

while (len(player1_deck) > 0) and (len(player2_deck) > 0):
    # Draw cards from top of deck
    p1_card = player1_deck[0]
    p2_card = player2_deck[0]
    player1_deck = player1_deck[1:]
    player2_deck = player2_deck[1:]
    if p1_card > p2_card:
        player1_deck = np.append(player1_deck, max(p1_card, p2_card))
        player1_deck = np.append(player1_deck, min(p1_card, p2_card))
    else:
        player2_deck = np.append(player2_deck, max(p1_card, p2_card))
        player2_deck = np.append(player2_deck, min(p1_card, p2_card))

if len(player1_deck) > 0:
    winner_deck = player1_deck
else:
    winner_deck = player2_deck

def compute_score(deck):
    idx = np.linspace(deck.shape[0], 1, num=deck.shape[0], dtype=np.int)
    return np.multiply(deck, idx).sum()

print(f"Day 22 task 1: {compute_score(winner_deck)}")

current_player1_deck = np.array(init_player1_deck)
current_player2_deck = np.array(init_player2_deck)

history = [[]]

# Loop continuously
prev_level = 0
while True:
    if len(history) != prev_level:
        if len(history) == 1 and (len(history[-1])+1) == 1:
            print(f"====== New Game Level: {len(history)} Turn Number: {len(history[-1])+1} ======= !!!!!!")
        elif len(history) == 1:
            print(f"====== New Game Level: {len(history)} Turn Number: {len(history[-1])+1} =======")
        else:
            print(f"New Game Level: {len(history)} Turn Number: {len(history[-1])+1}")
        prev_level = len(history)
    # First, check whether we've seen this deck on this game level before.
    seen_before = False
    for decks in history[-1]:
        if np.all(current_player1_deck == decks[0]) and np.all(current_player2_deck == decks[1]):
            seen_before = True
            break
    if seen_before:
        # This configuration has been seen before in this game. Player 1 wins, and we return to the previous game!
        # First, check whether this is the top level game, if it is, set the winner_deck
        if len(history) == 1:
            winner_deck = current_player1_deck
            # Break out of the loop.
            break

        # First, discard this game as it's over.
        history.pop(-1)

        # Restore the last state from previous game
        current_player1_deck = np.copy(history[-1][-1][0])
        current_player2_deck = np.copy(history[-1][-1][1])

        # Take the top card off the decks
        p1_card = current_player1_deck[0]
        p2_card = current_player2_deck[0]
        current_player1_deck = current_player1_deck[1:]
        current_player2_deck = current_player2_deck[1:]

        # Winner (p1) gets the cards on bottom of deck, with winner on top.
        current_player1_deck = np.append(current_player1_deck, p1_card)
        current_player1_deck = np.append(current_player1_deck, p2_card)

        # Ready for next loop
    else:
        # We haven't seen this set of cards before.
        # Save current state to the latest game's history.
        history[-1].append((np.copy(current_player1_deck), np.copy(current_player2_deck)))

        # Check whether this is the final state of the game!
        if current_player1_deck.shape[0] == 0:
            # Player 2 has won!
            if len(history) == 1:
                winner_deck = current_player2_deck
                break

            # Otherwise, we back out of the current game.
            # First, discard this game as it's over.
            history.pop(-1)

            # Restore the last state from previous game
            current_player1_deck = np.copy(history[-1][-1][0])
            current_player2_deck = np.copy(history[-1][-1][1])

            # Take the top card off the decks
            p1_card = current_player1_deck[0]
            p2_card = current_player2_deck[0]
            current_player1_deck = current_player1_deck[1:]
            current_player2_deck = current_player2_deck[1:]

            # Winner (p2) gets the cards on bottom of deck, with winner on top.
            current_player2_deck = np.append(current_player2_deck, p2_card)
            current_player2_deck = np.append(current_player2_deck, p1_card)

        elif current_player2_deck.shape[0] == 0:
            # Player 1 has won!
            if len(history) == 1:
                winner_deck = current_player1_deck
                break

            # Otherwise, we back out of the current game.
            # First, discard this game as it's over.
            history.pop(-1)

            # Restore the last state from previous game
            current_player1_deck = np.copy(history[-1][-1][0])
            current_player2_deck = np.copy(history[-1][-1][1])

            # Take the top card off the decks
            p1_card = current_player1_deck[0]
            p2_card = current_player2_deck[0]
            current_player1_deck = current_player1_deck[1:]
            current_player2_deck = current_player2_deck[1:]

            # Winner (p1) gets the cards on bottom of deck, with winner on top.
            current_player1_deck = np.append(current_player1_deck, p1_card)
            current_player1_deck = np.append(current_player1_deck, p2_card)

        else:
            # Nonempty decks, Draw cards.
            p1_card = current_player1_deck[0]
            p2_card = current_player2_deck[0]
            current_player1_deck = current_player1_deck[1:]
            current_player2_deck = current_player2_deck[1:]

            if (current_player1_deck.shape[0] >= p1_card) and (current_player2_deck.shape[0] >= p2_card):
                # Start a new game level.
                history.append([])

                # Get the recursed decks.
                current_player1_deck = current_player1_deck[:p1_card]
                current_player2_deck = current_player2_deck[:p2_card]
            else:
                # We play normally this round.
                if p1_card > p2_card:
                    # Player 1 wins this round.
                    current_player1_deck = np.append(current_player1_deck, p1_card)
                    current_player1_deck = np.append(current_player1_deck, p2_card)
                else:
                    # Player 2 wins this round
                    current_player2_deck = np.append(current_player2_deck, p2_card)
                    current_player2_deck = np.append(current_player2_deck, p1_card)

print(f"Day 22 task 2: {compute_score(winner_deck)}")
