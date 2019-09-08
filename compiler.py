#!/usr/bin/env python3

import re

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return self.value

class Tokenizer:
    token_types = dict(
        definition = r'\bwhatever\b', # whatever keyword
        integer = r'\b[0-9]+\b', # any integer number
        identifier = r'\b\w+\b', # any words characters
        comma = r',', # close paren
        ocurly = r'\{', # open curly bracket
        ccurly = r'\}', # close curly bracket
        oparen = r'\(', # open paren
        cparen = r'\)', # close paren
    )

    def __init__(self, code):
        self.code = code
        print('tokenizer initialized with %s' % code)

    def tokenize(self):
        tokens = []
        while self.code:
            tokens.append(self.tokenize_one_token())
            self.code = self.code.strip()
            # print('tokens: %s' % str(tokens))
            print('remaining : %s' % str(self.code))
        return tokens

    def tokenize_one_token(self):
        for type, regex in Tokenizer.token_types.items():
            pattern = ()
            match = re.compile(regex).match(self.code)
            if match:
                self.code = self.code[match.end():]
                return Token(type, match[0])

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        return self.parse_all_definitions()

    def parse_all_definitions(self):
        all_definitions = []
        while self.peek('definition'):
            all_definitions.append(self.parse_definition())
        return RootNode(all_definitions)

    def parse_definition(self):
        self.consume('definition')
        name = self.consume('identifier')
        arg_names = self.parse_arg_names()
        self.consume('ocurly')
        body = self.parse_expr()
        self.consume('ccurly')
        return DefNode(name, arg_names, body)

    def consume(self, expected_type):
        token = self.tokens.pop(0)
        if token.type is expected_type:
            return token
        else:
            raise RuntimeError("expected %s but got %s" % (expected_type, token.type))

    def peek(self, expected_type, offset = 0):
        return len(self.tokens) > offset and self.tokens[offset].type is expected_type
    
    def parse_arg_names(self):
        arg_names = []
        self.consume('oparen')
        if self.peek('identifier'):
            arg_names.append(self.consume('identifier').value)
            while self.peek('comma'):
                self.consume('comma')
                arg_names.append(self.consume('identifier').value)
        self.consume('cparen')
        return arg_names

    def parse_expr(self):
        if self.peek('integer'):
            return self.parse_integer()
        if self.peek('identifier') and self.peek('oparen', 1):
            return self.parse_call()
        else:
            return self.parse_var_ref()

    def parse_call(self):
        name = self.consume('identifier')
        arg_exprs = self.parse_arg_exprs()
        return CallNode(name, arg_exprs)

    def parse_var_ref(self):
        value = self.consume('identifier').value
        return VarRefNode(value)

    def parse_arg_exprs(self):
        arg_exprs = []
        self.consume('oparen')
        # if it doesn't immediately see a close paren, it must mean there are arg exprs to parse.
        if not self.peek('cparen'):
            arg_exprs.append(self.parse_expr())
            while self.peek('comma'):
                self.consume('comma')
                arg_exprs.append(self.parse_expr())
        self.consume('cparen')
        return arg_exprs

    def parse_integer(self):
        int_value = int(self.consume('integer').value)
        return IntegerNode(int_value)

class RootNode:
    def __init__(self, all_definitions):
        self.all_definitions = all_definitions

    def __str__(self):
        return 'RootNode(%s)' % str(list(map(lambda x: str(x), self.all_definitions)))

class DefNode:
    def __init__(self, name, arg_names, body):
        self.name = name
        self.arg_names = arg_names
        self.body = body

    def __str__(self):
        return 'DefNode(%s, %s, %s)' % (self.name, str(self.arg_names), str(self.body))

class IntegerNode:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'IntegerNode(%s)' % str(self.value)

class CallNode:
    def __init__(self, name, arg_exprs):
        self.name = name
        self.arg_exprs = arg_exprs

    def __str__(self):
        return 'CallNode(%s, %s)' % (self.name, str(list(map(lambda x: str(x), self.arg_exprs))))

class VarRefNode:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'VarRefNode(%s)' % (str(self.value))

class Generator:
    def __init__(self, tree):
        self.tree = tree

    def generate(self, node):
        t = type(node)
        if t == RootNode:
            return '\n'.join([self.generate(definition) for definition in node.all_definitions])
        elif t == DefNode:
            return "function %s(%s) { return %s; }" % (
                node.name,
                ', '.join(node.arg_names),
                self.generate(node.body)
            )
        elif t is CallNode:
            return "%s(%s)" % (
                node.name,
                ', '.join([self.generate(expr) for expr in node.arg_exprs])
            )
        elif t is VarRefNode:
            return node.value
        elif t is IntegerNode:
            return str(node.value)
        else:
            raise RuntimeError("encountered unexpected node of type %s" % t)

tokenizer = Tokenizer(open("test.what").read())
tokens = tokenizer.tokenize()
# print(list(map(lambda x: x.value, tokens)))

parser = Parser(tokens)
tree = parser.parse()
# print(tree)

generator = Generator(tree)
generated = generator.generate(tree)
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

