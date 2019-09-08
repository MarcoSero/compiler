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
        integer    = r'\b[0-9]+\b',   # any integer number
        identifier = r'\b\w+\b',      # any words characters
        comma      = r',',            # close paren
        ocurly     = r'\{',           # open curly bracket
        ccurly     = r'\}',           # close curly bracket
        oparen     = r'\(',           # open paren
        cparen     = r'\)',           # close paren
    )

    def __init__(self, code):
        self.code = code

    def tokenize(self):
        tokens = []
        while self.code:
            tokens.append(self._tokenize_one_token())
            self.code = self.code.strip()
        return tokens

    def _tokenize_one_token(self):
        for type, regex in Tokenizer.token_types.items():
            pattern = ()
            match = re.compile(regex).match(self.code)
            if match:
                self.code = self.code[match.end():]
                return Token(type, match[0])
