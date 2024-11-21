from lexer import Lexer
from utils import Log

Log.show(True)

class Node:
    def __init__(self, symbol=None, parent=None, children=[]):
        self.symbol = symbol
        self.parent = parent
        self.children = children
        
    def add_child(self, node):
        self.children.append(node)

class Token:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBR = "NUMBR"
    NUMBAR = "NUMBAR"
    YARN = "YARN"
    TROOF = "TROOF"
    OPERATOR = "OPERATOR"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"
    COMMENT_SINGLE = "COMMENT_SINGLE"
    COMMENT_MULTI = "COMMENT_MULTI"

    def __init__(self, lexeme, type=None, description="None"):
        self.lexeme = lexeme
        self.type = type
        self.description = description

    def __str__(self):
        return f"{self.type}: {self.lexeme}"

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0
        self.root = Node()  # Root node of the AST
        self.current = self.tokens[self.cursor]

    # Move to the next token
    # - increments the cursor by 1
    def next(self):
        self.cursor += 1

        if self.cursor < len(self.tokens):
            self.current = self.tokens[self.cursor]
        else: raise Exception("Token overflow!")

    # def current(self):
    #     return self.tokens[self.cursor]
    
    def curr_node(self):
        return self.tokens[self.cursor]
    
    # def accept(self, *token_types, lexeme=None):
    #     if self.current.type not in token_types:
    #         return False
        
    #     return not lexeme or self.current.lexeme == lexeme

    '''-------------------------------------------------------------------------= 
    Checks whether the token at the cursor:
      - has the specified lexeme
      - are specific type/s of tokens
    @ Parameters
      - *token_types [str] = specify "any number" of Token types to expect
      - lexeme [str] = specify a specific lexeme to expect in the current token
      - consume [bool] = determines whether to move to next token if
                expectation was satisfied
      - required [bool] = determines whether an error should be raised if
                expectation was satisfied
    @ Usage
        self.expect(Token.KEYWORD, "HAI") → The current token needs to specifically be a "HAI" keyword
        self.expect(Token.NUMBAR) → The current token has to be a NUMBAR literal
    @ Return
        True if expectation was met, otherwise False
    =---------------------------------------------------------------------------'''
    def expect(self, *token_types, lexeme=None, consume=True, required=True):
        if self.current.type not in token_types:
            if required:
                raise Exception(f"Expected {token_types}, got {self.current.type}")
            else: return None
        
        if lexeme and self.current.lexeme != lexeme:
            if required:
                raise Exception(f"Expected {self.current.lexeme}, got {lexeme}")
            else: return None
        
        if consume: 
            self.next()

        return lexeme if lexeme else True
    
    '''----------------------------# 
    In recursive descent, each function represents a non-terminal symbol in the grammar.
    The expansion/s of each non-terminal symbol is handled inside the functions.

    This implementation of recursive descent could be more intuitive 
    when constructing the Abstract Syntax Tree.
    #----------------------------'''

    def program(self):
        self.expect(Token.KEYWORD, "HAI")
        self.expect(Token.NUMBAR)
        
        # EVERYTHING HAPPENS HERE
        while not self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
            self.statement()
            self.next()

        return True

    def expr(self):
        operation = self.current.lexeme
        if self.expect(Token.KEYWORD, required=False, consume=True):

            op1 = self.expr()
            if not op1:
                raise Exception("Expected: <expression>")
            Log.i(op1)

            if operation == "NOT":
                return not bool(op1)
            
            self.expect(Token.KEYWORD, lexeme="AN")

            op2 = self.expr()
            if not op2:
                raise Exception("Expected: <expression>")
            Log.i(op2)
            
            match operation:
                # Arithmetic
                case "SUM OF":
                    return op1 + op2
                case "DIFF OF":
                    return op1 - op2
                case "PRODUKT OF":
                    return op1 * op2
                case "QUOSHUNT OF":
                    return op1 / op2
                case "MOD OF":
                    return op1 % op2
                case "BIGGR OF":
                    return max(op1, op2)
                case "SMALLR OF":
                    return min(op1, op2)
                
                # Conditional
                case "BOTH SAEM":
                    return op1 == op2
                case "DIFFRINT":
                    return op1 != op2
                case _:
                    raise Exception(f"Operation {operation} not recognized")
             
        if self.expect(Token.NUMBAR, consume=False, required=False):
            got = float(self.current.lexeme)
            self.next()
            return got 
        
        if self.expect(Token.NUMBR, consume=False, required=False):
            got = int(self.current.lexeme)
            self.next()
            return got 
        
        if self.expect(Token.TROOF, consume=False, required=False):
            Log.i(f"Got boolean: {self.current.lexeme}")
            self.next()
            return self.current.lexeme == "WIN"
        
        raise Exception("Encountered invalid symbol in expression")

    def statement(self):
        if self.expect(Token.KEYWORD, lexeme="I HAS A", required=False):
            Log.i("Assign!")
                
            # if not self.assign():
            #     raise Exception("Error occurred during declaration")
            var_name = self.current.lexeme
            Log.i(f"Variable name: {var_name}")
            self.next()
            if self.expect(Token.KEYWORD, lexeme="ITZ"):
                Log.d(self.current)
                if self.current.type == "KEYWORD": val = self.expr()
                else: val = self.current.lexeme
                Log.i(f"Assigning value: {val} to {var_name}")

            # code for var_name = val


        if self.expect(Token.KEYWORD, lexeme="VISIBLE", required=False):
            if not self.print():
                raise Exception("Error occurred while executing VISIBLE")
            
        # Create a branch for every statement ↓↓↓
        if self.expect(Token.COMMENT_SINGLE, required=False, consume=False):
            comm = str(self.current.lexeme).split()
            comm = " ".join(comm[1:])
            Log.d(f"Single-line Comment: {comm}")


        if self.expect(Token.COMMENT_MULTI, required=False, consume=False):
            comm = str(self.current.lexeme).split()
            comm = " ".join(comm[1:-1])
            Log.d(f"Multi-line Comment: {comm}")

        if self.expect(Token.IDENTIFIER, lexeme="OBTW", required=False):
            comm = ""
            while not self.expect(Token.IDENTIFIER, lexeme="TLDR", consume=False, required=False):
                comm += (self.current.lexeme) + " "
                self.next()
            Log.d(f"Multi-line Comment: {comm}")


        return True

    def print(self):
        if not self.expect(Token.YARN, Token.KEYWORD, Token.NUMBAR, Token.NUMBR, Token.TROOF, consume=False):
            raise Exception(f"Expected literal or <expr>, got {self.current.lexeme}")
        
        Log.d(f"To print: {self.current.type}")
        value = self.current.lexeme if self.current.type == Token.YARN else self.expr()

        if isinstance(value, bool):
            print("WIN" if value else "FAIL") 
        else: print(value)
        Log.d(f"Printed {value}")

        return True
    
# MAIN
tokens = Lexer(open("sample.lol", "r")).get_tokens()

for token in tokens:
    print(f"Token type: {token.type}, Lexeme: {token.lexeme}")

parser = Parser(tokens)
result = parser.program()


# print("Result:", result)
Log.d("Parsing completed successfully!")