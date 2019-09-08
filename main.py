#!/usr/bin/env python3

import sys

from compiler.generator import Generator
from compiler.nodes import *
from compiler.parser import Parser
from compiler.tokenizer import Tokenizer

if len(sys.argv) < 2:
    sys.exit()

generated = ""
for filename in sys.argv[1:]:
    tokenizer = Tokenizer(open(filename).read())
    tokens = tokenizer.tokenize()
    # print(list(map(lambda x: x.value, tokens)))

    parser = Parser(tokens)
    tree = parser.parse()
    # print(tree)

    generator = Generator(tree)
    generated = generated + '\n' + generator.generate(tree)

# print(generated)

RUNTIME = """
function add(x, y) { return x + y; }
function subtract(x, y) { return x - y; }
function multiply(x, y) { return x * y; }
function divide(x, y) { return x / y; }
"""
TEST = """
console.log(f(1, 2));
"""
OUTPUT = '\n'.join([RUNTIME, generated, TEST])
print(OUTPUT)

