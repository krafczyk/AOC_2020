import argparse
import os
import sys
import numpy as np
import re

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 20')
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

tile_number_re = re.compile("Tile ([0-9]*):")

class Tile(object):
    @staticmethod
    def render_bool_array(array):
        if len(array.shape) > 2:
            raise RuntimeError("arrays more than 2d are currently unsupported.")
        if len(array.shape) == 1:
            line = ""
            for i in range(array.shape[0]):
                if array[i]:
                    line += '#'
                else:
                    line += '.'
            return line
        else:
            result = ""
            for j in range(array.shape[1]):
                line = ""
                for i in range(array.shape[0]):
                    if array[i,j]:
                        line += '#'
                    else:
                        line += '.'
                line += '\n'
                result += line
            return result[:-1]


    def __init__(self, number, tile_map):
        self.number = number
        self.tile_map = tile_map

    def __str__(self):
        result = f"Tile {self.number}:\n"
        result += Tile.render_bool_array(self.tile_map)
        return result

    def get_border(self, side):
        if side == 'N':
            return self.tile_map[:,0]
        elif side == 'S':
            return self.tile_map[:,-1]
        elif side == 'E':
            return self.tile_map[-1,:]
        elif side == 'W':
            return self.tile_map[0,:]
        else:
            raise RuntimeError("Unrecognized tile side: {side}")


tiles = []
i = 0
while i < len(lines):
    the_line = lines[i]
    matches = tile_number_re.findall(the_line)
    if len(matches) != 1:
        raise RuntimeError(f"Unexpected line!: {the_line.strip()}")

    tile_map = np.zeros((10,10), dtype=bool)
    for k in range(10):
        for j in range(10):
            if lines[i+k+1][j] == '#':
                tile_map[j,k] = True
    tiles.append(Tile(int(matches[0]), tile_map))
    i += 12

# Test
tile_matches = {}
for i in range(len(tiles)):
    tile_i = tiles[i]
    matches_i = tile_matches.get(tile_i.number, [])
    for D_i in ['N', 'S', 'E', 'W']:
        side_i = tile_i.get_border(D_i)
        for j in range(i+1,len(tiles)):
            tile_j = tiles[j]
            matches_j = tile_matches.get(tile_j.number, [])
            for D_j in ['N', 'S', 'E', 'W']:
                side_j = tile_j.get_border(D_j)
                if np.all(side_i == side_j) or np.all(side_i[::-1] == side_j):
                    matches_i.append(tile_j.number)
                    matches_j.append(tile_i.number)
            tile_matches[tile_j.number] = matches_j
    tile_matches[tile_i.number] = matches_i

min_matches = len(tile_matches[list(tile_matches.keys())[0]])
max_matches = len(tile_matches[list(tile_matches.keys())[0]])

match_nums = {}
for num in tile_matches:
    matches = tile_matches[num]
    num_matches = len(matches)
    match_nums[num_matches] = match_nums.get(num_matches, 0)+1

value = 1
for num in tile_matches:
    matches = tile_matches[num]
    if len(matches) == 2:
        value *= num

print(f"Day 20 task 1: {value}")
