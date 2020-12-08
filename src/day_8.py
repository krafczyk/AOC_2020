import argparse
import os
import sys

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 8')
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

class Computer(object):
    @staticmethod
    def read_program_by_lines(lines):
        program = []
        for line in lines:
            parts = line.split()
            program.append((parts[0], int(parts[1])))
        return program

    def __init__(self, program):
        self.initialize_mem()
        self.program = program

    def initialize_mem(self):
        self.accumulator = 0
        self.cur_inst = 0

    def nop(self, arg):
        self.cur_inst += 1

    def acc(self, arg):
        self.accumulator += arg
        self.cur_inst += 1

    def jmp(self, arg):
        self.cur_inst += arg

    def run_instruction(self, inst):
        if inst[0] == 'nop':
            self.nop(inst[1])
        elif inst[0] == 'acc':
            self.acc(inst[1])
        elif inst[0] == 'jmp':
            self.jmp(inst[1])
        else:
            raise RuntimeError(f"Unrecognized instruction {inst[0]}")

    def run_cur_instruction(self):
        inst = self.program[self.cur_inst]
        self.run_instruction(inst)

computer = Computer(Computer.read_program_by_lines(lines))

instruction_count = {}

while True:
    if instruction_count.get(computer.cur_inst, 0) == 1:
        print(f"Day 8 task 1: {computer.accumulator}")
        break
    else:
        instruction_count[computer.cur_inst] = instruction_count.get(computer.cur_inst, 0)+1
        computer.run_cur_instruction()
