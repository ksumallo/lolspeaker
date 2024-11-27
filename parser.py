from lexer import Lexer, Token
from utils import Log

Log.show(True)

class Node:
    def __init__(self, symbol=None, parent=None, children=[]):
        self.symbol = symbol
        self.parent = parent
        self.children = children
        
    def add_child(self, node):
        self.children.append(node)

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
        else: Log.e("Token overflow!")

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
        if lexeme != None and self.current.lexeme != lexeme:
            if required:
                raise Exception(f"Expected {self.current.lexeme}, got {lexeme}")
            else: return None

        if self.current.type not in token_types:
            if required:
                raise Exception(f"Expected {token_types}, got {self.current.type}")
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

        return True

    def expr(self):
        if self.expect(Token.OPERATOR, required=False, consume=False):
            operation = self.current.lexeme

            self.next()
            op1 = self.expr()
            if op1 == None:
                raise Exception(f"Expected: <expression>, got {self.current.lexeme}")
        
            match (operation):
                case "NOT":
                    return not bool(op1)
                case "ANY OF" | "ALL OF":
                    operands = [op1]
                    
                    while self.expect(Token.KEYWORD, lexeme="AN", required=False):
                        op = self.expr()

                        if op == None:
                            raise Exception("Expected: bool or expression")
                        operands.append(op)

                    result = all(operands) if operation == "ALL OF" else any(operands)
                    return result
                
                case "SMOOSH":
                    operands = []
                    
                    if op1 != None:
                        operands.append(op1)
                    else: raise Exception("Expected: literal or <expr>")
                    
                    while self.expect(Token.KEYWORD, lexeme="AN", consume=True, required=False):
                        value = self.expr()

                        if value == None: break
                        # Log.d(f"To concat: {self.current.type}") # DEBUG
                        operands.append(value)

                    return "".join(operands)
            
            self.expect(Token.KEYWORD, lexeme="AN")

            op2 = self.expr()
            if not op2:
                raise Exception("Expected: <expression>")
            
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
        
        if self.expect(Token.YARN, consume=False, required=False):
            got = self.current.lexeme[1:-1]
            self.next()
            return got 
        
        if self.expect(Token.TROOF, consume=False, required=False):
            got = self.current.lexeme
            self.next()
            return got == "WIN"
        
        raise Exception(f"Encountered invalid symbol in expression: {self.current.lexeme}")

    def statement(self):
        if self.expect(Token.KEYWORD, lexeme="I HAS A", required=False):
            Log.i("Assign!")
            # if not self.assign():
            #     raise Exception("Error occurred during declaration")
        
        if self.expect(Token.KEYWORD, lexeme="VISIBLE", required=False):
            if not self.print():
                raise Exception("Error occurred while executing VISIBLE")
            
        # Create a branch for every statement ↓↓↓

        return True

    def print(self):
        value = self.expr()
        if value == None:
            raise Exception(f"Expected literal or <expr>, got {self.current.lexeme}")
        
        # Log.d(f"To print: {value} ({self.current.type})") # DEBUG

        if isinstance(value, bool):
            print("WIN" if value else "FAIL") 
        else: 
            print(value)

        return True
    
# MAIN
tokens = Lexer(open("project-testcases/test_2.lol", "r")).get_tokens()

parser = Parser(tokens)
result = parser.program()

# print("Result:", result)
Log.d("Parsing completed successfully!")