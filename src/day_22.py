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

memoization = {}

def hash_decks(decks):
    return hash((hash(decks[0].data.tobytes()), hash(decks[1].data.tobytes())))

history = [[]]

# Loop continuously
prev_level = 0
num_rounds = 0
while True:
    if len(history) != prev_level:
        if len(history) == 1 and (len(history[-1])+1) == 1:
            print(f"====== New Game Level: {len(history)} Turn Number: {len(history[-1])+1} ======= !!!!!!")
        elif len(history) == 1:
            print(f"====== New Game Level: {len(history)} Turn Number: {len(history[-1])+1} =======")
        else:
            print(f"New Game Level: {len(history)} Turn Number: {len(history[-1])+1}")
        prev_level = len(history)
    #print(f"Game level: {len(history)} turn {len(history[-1])+1}")
    #print(f"player1: {current_player1_deck.shape} {current_player1_deck}")
    #print(f"player2: {current_player2_deck.shape} {current_player2_deck}")
    #if num_rounds >= 10000:
    #    sys.exit(0)
    #num_rounds += 1

    game_winner = None
    # First, check whether we've seen this deck to completion before.
    deck_hash = hash_decks((current_player1_deck, current_player2_deck))
    #if deck_hash in memoization:
    #    print("Found game in our memoization!")
    #    game_winner = memoization[deck_hash]
    #else:
    if True:
        # First, check whether we've seen this deck on this game level before.
        seen_before = False
        for decks in history[-1]:
            if (current_player1_deck.shape == decks[0].shape) and (current_player2_deck.shape == decks[1].shape):
                if np.all(np.equal(current_player1_deck, decks[0])) and np.all(np.equal(current_player2_deck, decks[1])):
                    seen_before = True
                    break
        if seen_before:
            #print("Game repeated! Player 1 wins!")
            game_winner = 1
        else:
            # We haven't seen this set of cards before.
            # Save current state to the latest game's history.
            history[-1].append((np.copy(current_player1_deck), np.copy(current_player2_deck)))

            # Check whether this is the final state of the game!
            if current_player1_deck.shape[0] == 0:
                #print("Player 2 wins!")
                # Player 2 has won!
                game_winner = 2
            elif current_player2_deck.shape[0] == 0:
                #print("Player 1 wins!")
                # Player 2 has won!
                game_winner = 1
            elif (current_player1_deck.shape[0]-1 >= current_player1_deck[0]) and (current_player2_deck.shape[0]-1 >= current_player2_deck[0]):
                # Check if we need to recurse.
                # Start a new game level
                #print(f"Recursing at level {len(history)} turn {len(history[-1])}")
                history.append([])

                # Get the recursed decks.
                current_player1_deck = current_player1_deck[1:current_player1_deck[0]+1]
                current_player2_deck = current_player2_deck[1:current_player2_deck[0]+1]
                continue

    turn_winner = None
    if game_winner is not None:
        turn_winner = game_winner
        #print("Someone won the game!")
        # Someone has won the game.
        if len(history) == 1:
            #print("Whole game is over")
            # The game is over.
            if game_winner == 1:
                winner_deck = current_player1_deck
            else:
                winner_deck = current_player2_deck
            break

        else:
            #print("Memoizing game")
            # Memoize the history of this game.
            #for decks in history[-1]:
            #    decks_hash = hash_decks(decks)
            #    if decks_hash in memoization:
            #        if game_winner != memoization[decks_hash]:
            #            raise RuntimeError("Sanity check failed! deck had a different winner before!")
            #    else:
            #        memoization[decks_hash] = game_winner
            # Pop the old game off the history
            history.pop(-1)

            #print("Restoring previous game state")
            # Restore previous decks.
            current_player1_deck = history[-1][-1][0]
            current_player2_deck = history[-1][-1][1]

    p1_card = current_player1_deck[0]
    p2_card = current_player2_deck[0]
    if turn_winner is None:
        #print("Winner not determined yet!")
        if p1_card > p2_card:
            turn_winner = 1
        else:
            turn_winner = 2

    if turn_winner == 1:
        #print("Player 1 won the turn")
        # Player 1 won the turn.
        current_player1_deck = np.append(current_player1_deck[1:], [p1_card, p2_card])
        current_player2_deck = current_player2_deck[1:]
    else:
        #print("Player 2 won the turn")
        # Player 2 won the turn.
        current_player1_deck = current_player1_deck[1:]
        current_player2_deck = np.append(current_player2_deck[1:], [p2_card, p1_card])

print(f"Day 22 task 2: {compute_score(winner_deck)}")
