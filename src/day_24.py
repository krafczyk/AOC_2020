import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 24')
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

def hash_numpy(array):
    return hash(array.data.tobytes())

D = {
    'e': np.array([2,0], np.int),
    'w': np.array([-2,0], np.int),
    'se': np.array([1,-2], np.int),
    'sw': np.array([-1,-2], np.int),
    'ne': np.array([1, 2], np.int),
    'nw': np.array([-1, 2], np.int),
}

tile_set = set()
hash_map = {}

for line in lines:
    directions = line.strip()
    p = np.array([0,0], np.int)
    i = 0
    while i < len(directions):
        if directions[i] == 'e':
            p += D['e']
            i += 1
        elif directions[i] == 'w':
            p += D['w']
            i += 1
        elif directions[i] == 's':
            if directions[i+1] == 'e':
                p += D['se']
                i += 2
            elif directions[i+1] == 'w':
                p += D['sw']
                i += 2
            else:
                raise RuntimeError("unexpected south!")
        elif directions[i] == 'n':
            if directions[i+1] == 'e':
                p += D['ne']
                i += 2
            elif directions[i+1] == 'w':
                p += D['nw']
                i += 2
            else:
                raise RuntimeError("unexpected north!")
        else:
            raise RuntimeError("Unexpected")
    p_hash = hash_numpy(p)
    if p_hash in tile_set:
        tile_set.remove(p_hash)
    else:
        tile_set.add(p_hash)
    if p_hash not in hash_map:
        hash_map[p_hash] = p

print(f"Day 24 task 1: {len(tile_set)}")

num_days = 0
max_days = 100
while num_days < max_days:
    # Build set of locations to consider this 'day'
    consider_locations = set()
    for p_hash in tile_set:
        # Get tile neighbors
        p = hash_map[p_hash]
        Ds = np.stack(list(D.values()),axis=0)
        Ns = Ds+np.stack([p]*len(Ds),axis=0)
        for p in Ns:
            pos_hash = hash_numpy(p)
            if pos_hash not in consider_locations:
                consider_locations.add(pos_hash)
                hash_map[pos_hash] = p

    # Add black tiles to new map
    new_tile_set = set()
    for p_hash in consider_locations:
        # Get tile neighbors
        p = hash_map[p_hash]
        Ds = np.stack(list(D.values()),axis=0)
        Ns = Ds+np.stack([p]*len(Ds),axis=0)
        neighbors = set(map(lambda n: hash_numpy(n), list(Ns)))
        # Count number of neighbors that are black
        n_black = len(tile_set.intersection(neighbors))
        if p_hash in tile_set:
            # The tile is black.
            if n_black == 1 or n_black == 2:
                new_tile_set.add(p_hash)
        else:
            # The tile is white
            if n_black == 2:
                new_tile_set.add(p_hash)

    # Swap maps
    tile_set = new_tile_set
    num_days += 1
    print(f"Day {num_days}: {len(tile_set)}")


print(f"Day 24 task 2: {len(tile_set)}")
