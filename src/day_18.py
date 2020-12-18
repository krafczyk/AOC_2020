import argparse
import os
import sys
import string

# Define Argument Parser
parser = argparse.ArgumentParser('Solves Advent of Code Day 18')
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

class Node(object):
    def __init__(self, parent=None):
        self.parent = parent

    def __call__(self):
        pass

    def __str__(self):
        pass

class OperationNode(Node):
    def __init__(self, parent, op1, op2):
        super().__init__(parent)
        self.op1 = op1
        self.op2 = op2

    def __call__(self):
        pass

class AdditionNode(OperationNode):
    def __init__(self, parent, op1, op2):
        super().__init__(parent, op1, op2)

    def __call__(self):
        return self.op1()+self.op2()

    def __str__(self):
        return f"({self.op1} + {self.op2})"

class MultiplicationNode(OperationNode):
    def __init__(self, parent, op1, op2):
        super().__init__(parent, op1, op2)

    def __call__(self):
        return self.op1()*self.op2()

    def __str__(self):
        return f"({self.op1} * {self.op2})"

class NumberNode(Node):
    def __init__(self, parent, num):
        # Initialize parent type
        super().__init__(parent)
        self.number = num

    def __call__(self):
        return self.number

    def __str__(self):
        return f"{self.number}"

# Assumption: All numbers are single digits. This means we don't have to write a tokenizer. Input has already been tokenized.

def parse_line(line):
    the_line = line.strip()
    i = 0
    last_node = None
    while i < len(the_line):
        # Skip empty lines
        if the_line[i] == ' ':
            pass
        # Build new node
        elif the_line[i] in string.digits:
            # We have a number token.
            num = int(the_line[i])
            if last_node is None:
                node = NumberNode(None, num)
                last_node = node
            elif issubclass(type(last_node), OperationNode):
                if last_node.op2 is None:
                    # This is the second number of an operation node.
                    node = NumberNode(last_node, num)
                    last_node.op2 = node
                else:
                    raise RuntimeError("A number can't immediately follow a completed operation.")
            else:
                raise RuntimeError("Number node, unhandled situation")
        elif the_line[i] == '+' or the_line[i] == '*':
            # We have an operation
            if last_node is None:
                raise RuntimeError("The first token can't be an operation!")

            # Initialize node.
            if the_line[i] == '+':
                node = AdditionNode(None, None, None)
            else: 
                node = MultiplicationNode(None, None, None)

            if last_node.parent is not None:
                raise RuntimeError("An operation cannot follow a node with a parent!")
            if issubclass(type(last_node), OperationNode):
                if last_node.op1 is None:
                    raise RuntimeError("Previous operation node not fully specified!")
            node.op1 = last_node
            last_node.parent = node
            last_node = node

            # Skip space
            i += 1
        elif the_line[i] == '(':
            # We have an open parens token.
            # Find the end parens
            j = i+1
            depth = 0
            while (depth > 0) or (the_line[j] != ')'):
                if the_line[j] == '(':
                    depth += 1
                if the_line[j] == ')':
                    depth -= 1
                j += 1
            # Parse subordinate section.
            node = parse_line(the_line[i+1:j])

            if last_node is None:
                last_node = node
            elif type(last_node) is NumberNode:
                raise RuntimeError("A parenthesis can't follow a plain number.")
            elif issubclass(type(last_node), OperationNode):
                if last_node.op1 is None:
                    raise RuntimeError("Previous operation node not fully specified!")
                last_node.op2 = node

            # Skip to end parens.
            i = j
        else:
            raise RuntimeError("Unhandled situation!")

        i += 1
    return last_node

total = 0
for line in lines:
    result = parse_line(line)
    total += result()

print(f"Day 18 task 1: {total}")
