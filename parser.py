from lexer import Token, Lexer

grammar = {
    "program": [Token("HAI"), "linebreak", "statement", "linebreak", Token("KTHXBYE")],
    "linebreak": [],
    "print_var": [Token("VISIBLE"), "var"],
    "print_expr": [Token("VISIBLE"), "expr"],
    "print_literal": [Token("VISIBLE"), "literal"],
    "literal": None,
    "statement": None
}

class Node:
    def __init__(self, symbol):
        self.token = None
        self.children = []

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.root = Node("program")

    def start_parse(self):
        self.parse(self.root)
        self.traverse(self.root)

    def parse(self, node):
        # Start at root
        print("Check symbol:", node.symbol, "Token:", type(node.symbol) is Token)
        if not (type(node.symbol) is Token or node.symbol is None):
            for child in grammar[node.symbol]:
                if child is Token:
                    continue
                if child:
                    new_child = Node(child) 
                    node.children.append(new_child)
                    self.parse(new_child)
                else: return
        else: return

    def traverse(self, node):
        print("NODE:", node.symbol)
        for child in node.children:
            self.traverse(child)
        return

tokens = Lexer().get_tokens()
parser = Parser(tokens)
parser.start_parse()
# Traverse the tree in-order