from .nodes import *

class Generator:
    def __init__(self, tree):
        self.tree = tree

    def generate(self, node):
        t = type(node)
        if t == RootNode:
            return '\n'.join([self.generate(definition) for definition in node.all_definitions])
        elif t == DefNode:
            return "function %s(%s) {\n %s\n}" % (
                node.name,
                ', '.join(node.arg_names),
                self.generate(node.body)
            )
        elif t is BodyNode:
            all_but_last = ";\n ".join([self.generate(expr) for expr in node.expressions[:-1]])
            return all_but_last + ("\n return %s;" % self.generate(node.expressions[-1]))
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
