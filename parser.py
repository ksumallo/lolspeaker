from lexer import Lexer, Token
from utils import Log
# from syntax_tree import AST, Node

Log.show(True)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.cursor = 0
        # self.ast = AST()  # Root node of the AST
        self.current = self.tokens[self.cursor]

    def next(self):
        """
        Moves to the next token by incrementing the cursor by 1
        """
        self.cursor += 1

        if self.cursor < len(self.tokens):
            self.current = self.tokens[self.cursor]
        else: raise Exception("Token overflow!")
    
    def curr_node(self):
        return self.tokens[self.cursor]

    def expect(self, *token_types, lexeme=None, consume=True, required=True):
        """
        Checks whether the token at the cursor:
        1. has the specified lexeme, or
        2. are specific type/s of tokens

        ### Parameters
        - `lexeme: str` specifies a lexeme to match in the current token
        - `token_types: varargs` - specify any number of Token types to accept as valid
        - `consume: bool` determines whether to move to next token if
                    expectation was satisfied
        - `required: bool` determines whether an error should be raised if
                    expectation was satisfied
        ### Usage
            self.expect(Token.KEYWORD, "HAI") # The current token needs to specifically be a "HAI" keyword
            self.expect(Token.NUMBAR) # The current token has to be a NUMBAR literal
        ### Return
            True if expectations were met, otherwise False
        """
        if self.current.lexeme == "\t": self.next()

        if lexeme != None and self.current.lexeme != lexeme:
            if required:
                raise Exception(f"Expected {self.current.lexeme}, got {lexeme}")
            else: return None

        if self.current.type not in token_types:
            if required:
                raise Exception(f"Expected {token_types}, got {self.current.type}")
            else: return None

        got = self.current.lexeme

        if consume: self.next()

        # self.ast.add_child(self.current)
        return got
    
    # Used for expecting non-terminals
    def accept(self, abstraction, err_msg="Unexpected non-terminal!"):
        _accept = abstraction()
        if _accept == None:
            Log.e(err_msg)
            raise Exception(err_msg)
        
        # self.ast.move(self.current)
        return _accept
    
    '''-----------------------------------------------------------------------------------# 
    In recursive descent, each function represents a non-terminal symbol in the grammar.
    The expansion/s of each non-terminal symbol is handled inside the functions.

    This implementation of recursive descent could be more intuitive 
    when constructing the Abstract Syntax Tree.
    #-----------------------------------------------------------------------------------'''

    def program(self):
        self.expect(Token.KEYWORD, "HAI")
        self.expect(Token.NUMBAR)
        
        # EVERYTHING HAPPENS HERE
        self.statement(depth=1)
        # while not self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
        
        # self.ast.start_traverse()
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
                    operands = []
                    
                    while self.expect(Token.KEYWORD, lexeme="AN",required=False):
                        op = self.accept(self.expr, err_msg="Expected: bool or expression")
                        operands.append(op)

                    if operation == "ALL OF":
                        return all(operands)
                    elif operation == "ANY OF":
                        return any(operands)
                    
                case "SMOOSH":
                    operands = [op1]
                    
                    while self.expect(Token.KEYWORD, lexeme="AN", required=False):
                        value = self.accept(self.expr)
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
             
        if self.expect(Token.NUMBAR, consume=False, required=False):
            got = float(self.current.lexeme)
            self.next()
            return got 
        
        if self.expect(Token.NUMBR, consume=False, required=False):
            got = int(self.current.lexeme)
            self.next()
            return got 
        
        if self.expect(Token.YARN, consume=False, required=False):
            got = str(self.current.lexeme)
            self.next()
            return got
        
        if self.expect(Token.TROOF, consume=False, required=False):
            got = self.current.lexeme 
            self.next()
            return got == "WIN"
        
        return None

    def statement(self, depth=0):
        Log.yell(f"Depth: {depth}")
        
        # Create a branch for every statement ↓↓↓
        if self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
            return None

        if self.expect(Token.KEYWORD, lexeme="I HAS A", required=False):
            pass    
        
        if self.expect(Token.KEYWORD, lexeme="VISIBLE", required=False):
            self.accept(self.print, err_msg="Error occurred while executing VISIBLE")
            
        self.next()
        return self.statement(depth=depth+1)

    def print(self):
        value = self.accept(self.expr, f"Expected literal or <expr>, got {self.current.lexeme}")

        if isinstance(value, bool):
            print("WIN" if value else "FAIL") 
        else: print(value)

        return True
    
# MAIN
tokens = Lexer(open("project-testcases/test_2.lol", "r")).get_tokens()

parser = Parser(tokens)
result = parser.program()

# print("Result:", result)
Log.d("Parsing completed successfully!")