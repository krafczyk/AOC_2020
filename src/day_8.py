import argparse
import os
import sys
import copy

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
            program.append([parts[0], int(parts[1])])
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

    def run_program(self):
        instruction_count = {}
        while True:
            if self.cur_inst == len(self.program):
                return
            elif self.cur_inst > len(self.program):
                raise RuntimeError("Program Overflow!")
            elif instruction_count.get(self.cur_inst, 0) == 1:
                return
            else:
                instruction_count[self.cur_inst] = instruction_count.get(self.cur_inst, 0)+1
                self.run_cur_instruction()

program = Computer.read_program_by_lines(lines)

computer = Computer(program)
computer.run_program()
print(f"Day 8 task 1: {computer.accumulator}")

for i in range(len(program)):
    program_copy = copy.deepcopy(program)
    if program_copy[i][0] == 'nop':
        program_copy[i][0] = 'jmp'
    elif program_copy[i][0] == 'jmp':
        program_copy[i][0] = 'nop'
    else:
        continue
    computer = Computer(program_copy)
    computer.run_program()
    if computer.cur_inst == len(program_copy):
        print(f"Day 8 task 2: {computer.accumulator}")
        break
