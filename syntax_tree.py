class AST:
    def __init__(self):
        self.root = Node()
        self.current = self.root

    def goto_parent(self):
        if self.current.parent != None:
            self.current = self.current.parent
        else: raise("Current node has no parent.")

    def add_child(self, token):
        self.current.children.append(Node(token, self.current))

    def move(self, token):
        new_node = Node(token, self.current)
        self.current.children.append(new_node)

        self.current = new_node

    def start_traverse(self):
        self.traverse(self.root)

    def traverse(self, node):
        if len(node.children) == 0:
            print("L:", node.token.lexeme)
            return
        
        print("A:", node.token.lexeme)
        for child in node.children:
            self.traverse(child)
 
class Node:
    def __init__(self, token=None, parent=None, children=[]):
        self.token = token
        self.parent = parent
        self.children = children