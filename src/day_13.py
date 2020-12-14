import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 13')
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

earliest_timestamp = int(lines[0].strip())

bus_list = list(map(lambda s: int(s), filter(lambda s: s != 'x', lines[1].strip().split(','))))

bus_nums = np.array(bus_list)
time_to_next = bus_nums*((earliest_timestamp//bus_nums)+1)-earliest_timestamp
i_bus = np.argmin(time_to_next, axis=0)

print(f"Day 13 task 1: {bus_nums[i_bus]*time_to_next[i_bus]}")

# Major assumptions, first slot of bus list is not zero. Thus p0 | t., The pi are mutually prime.
# All examples have these features.
# We thus find all N_i i > 0 s.t. t = p0*Pi_i pi*Ni

init_data = lines[1].strip().split(',')
bus_data = list(map(lambda p: (int(p[0]), p[1]), filter(lambda p: p[0] != 'x', zip(init_data, range(len(init_data))))))
periods = list(map(lambda p: p[0], bus_data))
offsets = list(map(lambda p: p[1], bus_data))

p0 = periods[0]

periods = periods[1:]
offsets = offsets[1:]

def smallest_N(D, F, A):
    # Smallest N s.t. D | F*N+A
    N = 0
    while (F*N+A)%D != 0:
        N += 1
    return N

def build_value(periods, Ns):
    answer = 0
    factor = 1
    for i in range(len(Ns)):
        answer += p0*factor*Ns[i]
        factor *= periods[i]
    return answer

Ns = []
factor = p0
for i in range(len(periods)):
    pi = periods[i]
    ai = offsets[i]

    const = build_value(periods, Ns)
    new_N = smallest_N(periods[i], factor, const+ai)
    Ns.append(new_N)
    factor *= periods[i]

print(f"Day 13 task 2: {build_value(periods, Ns)}")
