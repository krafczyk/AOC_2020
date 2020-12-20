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


for tile in tiles:
    print()
    print(tile)
    print("North border:")
    print(Tile.render_bool_array(tile.get_border('N')))
    print("South border:")
    print(Tile.render_bool_array(tile.get_border('S')))
    print("East border:")
    print(Tile.render_bool_array(tile.get_border('E')))
    print("West border:")
    print(Tile.render_bool_array(tile.get_border('W')))

