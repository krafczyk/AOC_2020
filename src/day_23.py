import argparse
import os
import sys
import numpy as np
import time

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

initial = np.array([],np.int)
for char in lines[0].strip():
    initial = np.append(initial, [int(char)])

def hash_numpy(array):
    return hash(array.data.tobytes())

def hash_list(the_list):
    return hash(tuple(the_list))

def get_next_sequence_numpy(sequence, max_val):
    pick_out = sequence[1:4]
    # Piece together
    sequence = np.concatenate([sequence[0:1],sequence[4:]], axis=0)
    # Find destination
    destination = ((sequence[0]-2)%max_val)+1
    while len(np.where(pick_out == destination)[0]) != 0:
        destination = ((destination-2)%max_val)+1

    # Get location of destination
    dest_idx = np.where(sequence == destination)[0][0]
    # Add picked out sequence back.
    sequence = np.concatenate([sequence[:dest_idx+1],pick_out,sequence[dest_idx+1:]], axis=0)
    # Rotate!
    return np.concatenate([sequence[1:],sequence[0:1]], axis=0)

def get_next_sequence_list(sequence, max_val):
    pick_out = sequence[1:4]
    # Piece together
    sequence = sequence[0:1]+sequence[4:]
    # Find destination
    destination = ((sequence[0]-2)%max_val)+1
    while True:
        try:
            pick_out.index(destination)
            destination = ((destination-2)%max_val)+1
        except:
            break

    # Get location of destination
    dest_idx = sequence.index(destination)
    # Add picked out sequence back.
    sequence = sequence[:dest_idx+1]+pick_out+sequence[dest_idx+1:]
    # Rotate!
    return sequence[1:]+sequence[0:1]

def get_history(numbers):
    initial_hash = hash_numpy(numbers)
    history = [initial_hash]

    max_number = numbers.max()
    periodic = False
    while not periodic:
        numbers = get_next_sequence_numpy(numbers, max_number)
        number_hash = hash_numpy(numbers)
        periodic = False
        if number_hash in history:
            # Now periodic!
            periodic = True
        history.append(number_hash)
    return history

def get_history_timing_numpy(numbers, num_steps):
    initial_hash = hash_list(numbers)
    history = [initial_hash]

    max_number = numbers.max()
    periodic = False
    step_i = 0
    start = time.time()
    while not periodic and step_i < num_steps:
        numbers = get_next_sequence_numpy(numbers, max_number)
        number_hash = hash_numpy(numbers)
        periodic = False
        if number_hash in history:
            # Now periodic!
            periodic = True
        history.append(number_hash)
        step_i += 1
    end = time.time()
    print(f"{(end-start)/num_steps*1000} ms per loop over {num_steps} loops numpy algorithm")

def get_history_timing_list(numbers, num_steps):
    initial_hash = hash_list(numbers)
    history = [initial_hash]

    max_number = 0
    for n in numbers:
        max_number = max(n,max_number)
    periodic = False
    step_i = 0
    start = time.time()
    while not periodic and step_i < num_steps:
        numbers = get_next_sequence_list(numbers, max_number)
        number_hash = hash_list(numbers)
        periodic = False
        if number_hash in history:
            # Now periodic!
            periodic = True
        history.append(number_hash)
        step_i += 1
    end = time.time()
    print(f"{(end-start)/num_steps*1000} ms per loop over {num_steps} loops list algorithm")

def get_value_in_sequence(initial, history, I):
    last_hash = history[-1]
    first_hash_idx = history.index(last_hash)
    #print(f"first_hash_idx: {first_hash_idx}")
    last_hash_idx = len(history)-1
    #print(f"last_hash_idx: {last_hash_idx}")
    period = last_hash_idx-first_hash_idx
    #print(f"period: {period}")
    runup = first_hash_idx
    if I < runup:
        target_hash = history[I]
    else:
        i = I-runup
        i = i%period
        target_hash = history[runup+i]

    numbers = np.copy(initial)
    max_number = initial.max()
    while hash_numpy(numbers) != target_hash:
        numbers = get_next_sequence_numpy(numbers, max_number)

    return numbers

history_1 = get_history(np.copy(initial))
sequence = get_value_in_sequence(np.copy(initial), history_1, 100)

#print(f"Sequence: {sequence}")

idx_1 = np.where(sequence == 1)[0][0]
sequence = np.concatenate([sequence[idx_1+1:],sequence[:idx_1]], axis=0)

print(f"Day 23 task 1: {sequence}")

numbers = np.concatenate([np.copy(initial), np.linspace(10, 1000000, num=(1000000-10+1), dtype=np.int)], axis=0)

get_history_timing_numpy(np.copy(numbers), 1000)
get_history_timing_list(list(numbers), 1000)


#history_2 = get_history(np.copy(numbers))
#sequence = get_value_in_sequence(np.copy(numbers), history_2, 10000000)
#
#idx_1 = np.where(sequence == 1)[0][0]
#sequence = np.concatenate([sequence[idx_1:],sequence[:idx_1]], axis=0)
#
#val_1 = sequence[1]
#val_2 = sequence[2]
#
#print(f"Day 23 task 2: {val_1*val_2}")
