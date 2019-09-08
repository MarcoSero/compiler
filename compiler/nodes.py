#!/usr/bin/env python3

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

