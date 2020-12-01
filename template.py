import argparse
import os
import sys

parser = argparse.ArgumentParser('Solves Advent of Code Day X')
parser.add_argument('input', help="Path to the input file", type=str, required=True)

args = parser.parse_args()

input_filepath = args.input

if not os.path.exists(input_filepath):
    print(f"ERROR file {input_filepath} doesn't exist!")
    sys.exit(1)
