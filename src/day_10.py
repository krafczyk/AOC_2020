import argparse
import os
import sys
import numpy as np

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 10')
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
    joltages = np.array(list(map(lambda s: int(s.strip()), f.readlines())))

print(f"Number of Joltage adapters: {len(joltages)}")

num_dict = {}
for i in range(joltages.shape[0]):
    joltage = joltages[i]
    num_dict[joltage] = num_dict.get(joltage, 0)+1

print(f"There are {len(num_dict.keys())} unique joltages")

max_number = 0
for key in num_dict:
    if num_dict[key] > max_number:
        max_number = num_dict[key]

print(f"There are at most {max_number} versions of one joltage adapter.")

max_joltage = joltages.max()

joltages = np.append(joltages, [0, max_joltage+3])
sorted_joltages = np.sort(joltages)

differences = sorted_joltages[1:]-sorted_joltages[:-1]

num_1_diffs = np.where(differences == 1)[0].shape[0]
num_3_diffs = np.where(differences == 3)[0].shape[0]

print(sorted_joltages)

print(f"{num_1_diffs} differences of 1 jolt")
print(f"{num_3_diffs} differences of 3 jolts")
print(f"Day 10 task 1: {num_1_diffs*num_3_diffs}")

print(f"differences:")
print(differences)

unique_differences = {}
for i in range(differences.shape[0]):
    diff = differences[i]
    unique_differences[diff] = unique_differences.get(diff, 0)+1

print(unique_differences)
print(f"max adapter joltage: {max_joltage} max_joltage: {max_joltage+3}, max_joltage/3: {(max_joltage+3)/3}")

# Assumption! At the start, there are only differences of 1 and 3.
# Differences of 3 cannot be 'removed'
# There are likely 'runs' of 1 differences which determine how they can be removed. i.e. if there are 3 1's in a row, 

runs = {}
run_length = 0
for i in range(differences.shape[0]):
    if differences[i] == 1:
        run_length += 1
    else:
        if run_length > 0:
            runs[run_length] = runs.get(run_length, 0)+1
            # Reset run length
            run_length = 0

print("contiguous runs:")
for run_length in sorted(runs.keys()):
    print(f"{run_length}: {runs[run_length]}")

config_answers = {}
hash_cheat_sheet = {}

def count_configurations_imp(config):
    if config.shape[0] <= 1:
        return 1
    config_hash = hash(bytes(config.data))
    if config.shape[0] in config_answers:
        if config_hash in config_answers[config.shape[0]]:
            return config_answers[config.shape[0]][config_hash]
    total = 1
    for i in range(config.shape[0]-1):
        merged_val = config[i]+config[i+1]
        new_config = np.zeros(config.shape[0]-1)
        new_config[:i+1] = config[:i+1]
        new_config[i:] += config[i+1:]
        if new_config[i] == 3:
            # We can split the new config into two parts.
            total += count_configurations_imp(new_config[:i])*count_configurations_imp(new_config[i:])
        else:
            total += count_configurations_imp(new_config)
    # Save result
    if config.shape[0] not in config_answers:
        config_answers[config.shape[0]] = {}
    config_answers[config.shape[0]][config_hash] = total
    hash_cheat_sheet[config_hash] = config
    # Report result
    return total

def count_configurations(run_length):
    init_config = np.ones((run_length,))
    return count_configurations_imp(init_config)

def hash_config(config):
    return hash(bytes(config.data))

def get_configurations_2(config):
    unique_hashes = set()
    conf_hash = hash_config(config)
    unique_hashes.add(conf_hash)
    if config.shape[0] > 1:
        for i in range(config.shape[0]-1):
            if config[i]+config[i+1] <= 3:
                # We can merge them
                new_config = np.zeros(config.shape[0]-1)
                new_config[:i+1] = config[:i+1]
                new_config[i:] += config[i+1:]
                # We can split the new config into two parts.
                unique_hashes = unique_hashes.union(get_configurations_2(new_config))
    return unique_hashes

def count_configurations_2(run_length):
    init_config = np.ones((run_length,))
    return len(get_configurations_2(init_config))

print("configuration counting")
for run_length in runs:
#    print(f"run of length {run_length}: has {count_configurations(run_length)} configurations")
    print(f"run of length {run_length}: has {count_configurations_2(run_length)} configurations")

#print(config_answers)
#print(hash_cheat_sheet)

total_configurations = 1
for run_length in runs:
    total_configurations*=count_configurations_2(run_length)**runs[run_length]

print(f"Total configurations: {total_configurations}")
