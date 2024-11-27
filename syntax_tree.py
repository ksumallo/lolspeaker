class AST:
    def __init__(self):
        self.root = Node()
        self.current = self.root

    def goto_parent(self):
        if self.current.parent != None:
            self.current = self.current.parent
        else: raise("Current node has no parent.")

    def add_child(self, node):
        self.current.children.append(node)

class Node:
    def __init__(self, symbol=None, parent=None, children=[]):
        self.symbol = symbol
        self.parent = parent
        self.children = children