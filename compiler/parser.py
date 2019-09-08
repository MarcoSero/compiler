#!/usr/bin/env python3

from .nodes import *
from .tokenizer import *

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens

    def parse(self):
        return self._parse_all_definitions()

    def _parse_all_definitions(self):
        all_definitions = []
        while self._peek('definition'):
            all_definitions.append(self._parse_definition())
        return RootNode(all_definitions)

    def _parse_definition(self):
        self._consume('definition')
        name = self._consume('identifier')
        arg_names = self._parse_arg_names()
        self._consume('ocurly')
        body = self._parse_expr()
        self._consume('ccurly')
        return DefNode(name, arg_names, body)

    def _consume(self, expected_type):
        token = self.tokens.pop(0)
        if token.type is expected_type:
            return token
        else:
            raise RuntimeError("expected %s but got %s" % (expected_type, token.type))

    def _peek(self, expected_type, offset = 0):
        return len(self.tokens) > offset and self.tokens[offset].type is expected_type
    
    def _parse_arg_names(self):
        arg_names = []
        self._consume('oparen')
        if self._peek('identifier'):
            arg_names.append(self._consume('identifier').value)
            while self._peek('comma'):
                self._consume('comma')
                arg_names.append(self._consume('identifier').value)
        self._consume('cparen')
        return arg_names

    def _parse_expr(self):
        if self._peek('integer'):
            return self._parse_integer()
        if self._peek('identifier') and self._peek('oparen', 1):
            return self._parse_call()
        else:
            return self._parse_var_ref()

    def _parse_call(self):
        name = self._consume('identifier')
        arg_exprs = self._parse_arg_exprs()
        return CallNode(name, arg_exprs)

    def _parse_var_ref(self):
        value = self._consume('identifier').value
        return VarRefNode(value)

    def _parse_arg_exprs(self):
        arg_exprs = []
        self._consume('oparen')
        # if it doesn't immediately see a close paren, it must mean there are arg exprs to parse.
        if not self._peek('cparen'):
            arg_exprs.append(self._parse_expr())
            while self._peek('comma'):
                self._consume('comma')
                arg_exprs.append(self._parse_expr())
        self._consume('cparen')
        return arg_exprs

    def _parse_integer(self):
        int_value = int(self._consume('integer').value)
        return IntegerNode(int_value)
