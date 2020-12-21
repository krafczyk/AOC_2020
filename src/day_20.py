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
    edge_list = ['N', 'S', 'E', 'W']

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
                    if array[i,array.shape[1]-1-j]:
                        line += '#'
                    else:
                        line += '.'
                line += '\n'
                result += line
            return result[:-1]

    def rotate_right(self):
        self.tile_map = np.rot90(self.tile_map, k=1, axes=(1,0))

    def rotate_left(self):
        self.tile_map = np.rot90(self.tile_map, k=1, axes=(0,1))

    def fliplr(self):
        # quirk on our specific indexing
        self.tile_map = np.flipud(self.tile_map)

    def flipud(self):
        # quirk on our specific indexing
        self.tile_map = np.fliplr(self.tile_map)

    def __init__(self, number, tile_map):
        self.number = number
        self.tile_map = tile_map

    def __str__(self):
        result = f"Tile {self.number}:\n"
        result += Tile.render_bool_array(self.tile_map)
        return result

    def get_border(self, side):
        if side == 'N':
            return self.tile_map[:,-1]
        elif side == 'S':
            return self.tile_map[:,0]
        elif side == 'E':
            return self.tile_map[-1,:]
        elif side == 'W':
            return self.tile_map[0,:]
        else:
            raise RuntimeError("Unrecognized tile side: {side}")

    def does_match_border(self, border_array):
        for edge_I in Tile.edge_list:
            border_I = self.get_border(edge_I)
            if np.all(border_array == border_I) or np.all(border_array == border_I[::-1]):
                return True
        return False

tiles = {}
i = 0
while i < len(lines):
    the_line = lines[i]
    matches = tile_number_re.findall(the_line)
    if len(matches) != 1:
        raise RuntimeError(f"Unexpected line!: {the_line.strip()}")

    tile_map = np.zeros((10,10), dtype=bool)
    for k in range(10):
        for j in range(10):
            if lines[i+1+(9-k)][j] == '#':
                tile_map[j,k] = True
    new_tile = Tile(int(matches[0]), tile_map)
    tiles[int(matches[0])] = new_tile
    print(new_tile)
    i += 12

# Test
tile_matches = {}
for i in range(len(tiles)):
    tile_i = tiles[list(tiles.keys())[i]]
    matches_i = tile_matches.get(tile_i.number, [])
    for D_i in Tile.edge_list:
        side_i = tile_i.get_border(D_i)
        for j in range(i+1,len(tiles)):
            tile_j = tiles[list(tiles.keys())[j]]
            matches_j = tile_matches.get(tile_j.number, [])
            if tile_j.does_match_border(side_i):
                matches_i.append(tile_j.number)
                matches_j.append(tile_i.number)
            tile_matches[tile_j.number] = matches_j
    tile_matches[tile_i.number] = matches_i

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

print(f"Num pieces: {len(tiles)}")
num_side = int(len(tiles)**0.5)
print(f"num_tiles per side: {num_side}")

# 1 pick a corner piece.

init_tile_pick = None
for tile_number in tile_matches:
    if len(tile_matches[tile_number]) == 2:
        init_tile_pick = tile_number
        break

# Determine the edges which match to other pieces.
matching_edges = []
init_tile = tiles[init_tile_pick]
print("Want to use init_tile: ")
print(init_tile)
for edge_I in Tile.edge_list:
    edge_I_array = init_tile.get_border(edge_I)
    found_match = False
    for matching_tile_num in tile_matches[init_tile_pick]:
        matching_tile = tiles[matching_tile_num]
        if matching_tile.does_match_border(edge_I_array):
            found_match = True
            break
    if found_match:
        matching_edges.append(edge_I)
print(matching_edges)
matching_edges = sorted(matching_edges)
print(matching_edges)

# 2 Rotate until it's in the 'lower left'
if matching_edges == [ 'E', 'N']:
    pass
elif matching_edges == [ 'E', 'S']:
    init_tile.rotate_left()
elif matching_edges == [ 'S', 'W']:
    init_tile.rotate_right()
    init_tile.rotate_right()
elif matching_edges == [ 'N', 'W']:
    init_tile.rotate_right()
else:
    raise RuntimeError("Unexpected case in rotations!")

print("After rotation:")
print(init_tile)

# 3 Now, we assemble the puzzle starting in the lower left corner
puzzle_solution = []

for y in range(num_side):
    line = []
    if y == 0:
        line.append(init_tile)
    else:
        # We assume last piece is already in place, and oriented properly.
        prev_piece = tiles[puzzle_solution[y-1][0].number]
        # We get the East border, as this is where we're building from.
        north_border = prev_piece.get_border('N')
        # Find out which piece matches this border.
        prev_matches = tile_matches[prev_piece.number]
        north_match_num = None
        for prev_match_num in prev_matches:
            prev_match_piece = tiles[prev_match_num]
            if prev_match_piece.does_match_border(north_border):
                north_match_num = prev_match_num
                break
        if north_match_num is None:
            raise RuntimeError("Couldn't find a piece which matches the north edge!")
        new_piece = tiles[north_match_num]
        # Find out which edge we match to of the prospective piece.
        edge_match = None
        for edge_J in Tile.edge_list:
            border = new_piece.get_border(edge_J)
            if np.all(north_border == border) or np.all(north_border == border[::-1]):
                edge_match = edge_J
                break
        if edge_match is None:
            raise RuntimeError("Couldn't find the matching edge!")

        # Rotate piece until the edge is in the 'S' position, as the new piece will sit to the North of the old.
        if edge_match == 'W':
            new_piece.rotate_right()
        elif edge_match == 'S':
            pass
        elif edge_match == 'E':
            new_piece.rotate_left()
        else:
            new_piece.flipud()

        # Check orientation one more time.
        if not np.all(north_border == new_piece.get_border('S')):
            new_piece.fliplr()

        # sanity check
        if not np.all(north_border == new_piece.get_border('S')):
            raise RuntimeError("Failed Sanity check!")

        # We have the right piece!
        line.append(new_piece)

    print("Starting new row with piece:")
    print(line[0])

    # Build rest of line
    for x in range(1,num_side):
        # We assume last piece is already in place, and oriented properly.
        prev_piece = tiles[line[x-1].number]
        #print("current prev piece:")
        #print(prev_piece)
        # We get the East border, as this is where we're building from.
        east_border = prev_piece.get_border('E')
        #print("matching this east border")
        #print(Tile.render_bool_array(east_border))
        # Find out which piece matches this border.
        prev_matches = tile_matches[prev_piece.number]
        east_match_num = None
        for prev_match_num in prev_matches:
            prev_match_piece = tiles[prev_match_num]
            if prev_match_piece.does_match_border(east_border):
                east_match_num = prev_match_num
                break
        if east_match_num is None:
            raise RuntimeError("Couldn't find a piece which matches the east edge!")
        new_piece = tiles[east_match_num]
        #print("Found the next piece:")
        #print(new_piece)
        # Find out which edge we match to of the prospective piece.
        edge_match = None
        for edge_J in Tile.edge_list:
            border = new_piece.get_border(edge_J)
            if np.all(east_border == border) or np.all(east_border == border[::-1]):
                edge_match = edge_J
                break
        if edge_match is None:
            raise RuntimeError("Couldn't find the matching edge!")

        #print(f"Matching edge: {edge_match}")

        # Rotate piece until the edge is in the 'W' position, as the new piece will sit to the East of the old.
        if edge_match == 'W':
            pass
        elif edge_match == 'S':
            new_piece.rotate_right()
        elif edge_match == 'E':
            new_piece.fliplr()
        else:
            new_piece.rotate_left()

        #print(f"After rotation:")
        #print(new_piece)

        # Check orientation one more time.
        #print("----final orientation comparison----")
        #print("prev_piece")
        #print(prev_piece)
        #print("new_piece")
        #print(new_piece)
        #print("east_border:")
        #print(Tile.render_bool_array(east_border))
        #print("new_piece west border:")
        #print(Tile.render_bool_array(new_piece.get_border('W')))
        if not np.all(east_border == new_piece.get_border('W')):
            #print("Flipping piece u/d")
            new_piece.flipud()

        #print("After adjustment")
        #print("prev_piece:")
        #print(prev_piece)
        #print("new_piece:")
        #print(new_piece)
        # sanity check
        if not np.all(east_border == new_piece.get_border('W')):
            raise RuntimeError("Failed Sanity check!")

        # We have the right piece!
        line.append(new_piece)
        print("Adding new piece")
        print(new_piece)
    # We've now completed a row.
    puzzle_solution.append(line)
    #sys.exit(0)

#puzzle_solution = list(reversed(puzzle_solution))

# Diagnostic to see that we have the actual solution.
for l_j in range(num_side):
    puzzle_line = puzzle_solution[num_side-1-l_j]
    for y in range(10):
        line = ""
        for l_i in range(num_side):
            puzzle_tile = puzzle_line[l_i]
            for x in range(10):
                if puzzle_tile.tile_map[x,9-y]:
                    line += '#'
                else:
                    line += '.'
            line += " "
        print(line)
    print()


# 4 Merge pieces into one array.

major_rows = []
for l_j in range(num_side):
    puzzle_line = puzzle_solution[l_j]
    row_views = []
    for l_i in range(num_side):
        puzzle_tile = puzzle_line[l_i]
        row_views.append(puzzle_tile.tile_map[1:-1,1:-1])
    major_rows.append(np.concatenate(row_views, axis=0))
final_array = np.concatenate(major_rows, axis=1)

# After pieced together:
print(Tile.render_bool_array(final_array))
print(final_array.shape)

# 5 Build sea monster stencil
sea_monster_str = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   ",
]

sea_monster_stencil = np.zeros((len(sea_monster_str[0]), len(sea_monster_str)), dtype=bool)
for j in range(len(sea_monster_str)):
    for i in range(len(sea_monster_str[0])):
        if sea_monster_str[len(sea_monster_str)-1-j][i] == '#':
            sea_monster_stencil[i,j] = True

# 6 Search for sea monsters
def build_monster_map(array):
    monster_map = np.zeros(array.shape, dtype=bool)
    for j in range(array.shape[1]-sea_monster_stencil.shape[1]):
        for i in range(array.shape[0]-sea_monster_stencil.shape[0]):
            if np.all((array[i:i+sea_monster_stencil.shape[0],j:j+sea_monster_stencil.shape[1]]&sea_monster_stencil) == sea_monster_stencil):
                # We found a sea monster
                monster_map[i:i+sea_monster_stencil.shape[0],j:j+sea_monster_stencil.shape[1]] = monster_map[i:i+sea_monster_stencil.shape[0],j:j+sea_monster_stencil.shape[1]]|sea_monster_stencil
    return monster_map

first = True
while True:
    i = 0
    while i < 4:
        monster_map = build_monster_map(final_array)
        if monster_map.sum() != 0:
            # Found monsters!
            break
        i += 1
        final_array = np.rot90(final_array, k=1, axes=(1,0))
    if monster_map.sum() != 0:
        break

    if not first:
        break
    else:
        final_array = np.flipud(final_array)
        first = False

monster_map = build_monster_map(final_array)
print(Tile.render_bool_array(monster_map))

roughness = final_array.sum()-monster_map.sum()
print(f"Day 20 task 2: {roughness}")
