#!/usr/bin/env python3

import sys

from compiler.generator import Generator
from compiler.nodes import *
from compiler.parser import Parser
from compiler.tokenizer import Tokenizer

if len(sys.argv) < 2:
    sys.exit()

debug_enabled = False
files = sys.argv[1:]

if sys.argv[1] == '--debug':
    debug_enabled = True
    files = files[1:]

generated = ""
for filename in files:
    tokenizer = Tokenizer(open(filename).read())
    tokens = tokenizer.tokenize()
    if debug_enabled:
        print('>>> parsed tokens:\n%s\n' % list(map(lambda x: x.value, tokens)))

    parser = Parser(tokens)
    tree = parser.parse()
    if debug_enabled:
        print('>>> parse tree:\n%s\n' % tree)

    generator = Generator(tree)
    generated = generated + '\n' + generator.generate(tree)

if debug_enabled:
    print('>>> generated code:\n%s' % generated)
    exit()

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

