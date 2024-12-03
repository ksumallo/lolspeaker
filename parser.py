from lexer import Lexer, Token
from utils import Log
from time import sleep
# from syntax_tree import AST, Node

Log.show(True)

class Parser:
    def __init__(self, gui):
        self.gui = gui
        self.tokens = []
        self.cursor = 0
        self.current = None # self.tokens[self.cursor]

        self.flags = {
            'brk': False
        }

        # Runtime 
        self.vars = {}
        self.var_types = {}

    def set_tokens(self, _tokens):
        self.tokens = _tokens
        self.current = self.tokens[self.cursor]

    def set_gui(self, _tk_gui):
        self.gui = _tk_gui

    def next(self):
        """
        Moves to the next token by incrementing the cursor by 1
        """
        self.cursor += 1

        if self.cursor < len(self.tokens):
            self.current = self.tokens[self.cursor]
        else: raise Exception("Token overflow!")

    def seek(self, pos):
        """
        Moves to the cursor to `pos`, then updates the current token
        """
        self.cursor = pos

        if self.cursor < len(self.tokens):
            self.current = self.tokens[self.cursor ]
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
        if lexeme != None and self.current.lexeme != lexeme:
            if required:
                raise Exception(f"{self.current.pos()} Expected {lexeme}, got {self.current.lexeme}")
            else: return None

        if self.current.type not in token_types:
            if required:
                raise Exception(f"{self.current.pos()} Expected {token_types}, got {self.current.type} ({self.current.lexeme})")
            else: return None

        got = self.current.lexeme

        if consume: self.next()

        return got
    
    # Used for expecting non-terminals
    def accept(self, abstraction, err_msg="Unexpected non-terminal!"):
        _accept = abstraction()
        if _accept == None:
            Log.e(err_msg)
            raise Exception(f"{self.current.pos()} {err_msg} : {self.current.lexeme}")
        
        return _accept
    
    '''-----------------------------------------------------------------------------------# 
    In recursive descent, each function represents a non-terminal symbol in the grammar.
    The expansion/s of each non-terminal symbol is handled inside the functions.

    This implementation of recursive descent could be more intuitive 
    when constructing the Abstract Syntax Tree.
    #-----------------------------------------------------------------------------------'''

    def start(self):
        self._set("it", 0)
        self.program()

    def program(self):
        self.expect(Token.KEYWORD, "HAI")
        self.expect(Token.NUMBAR, required=False)

        # Variable Declarations
        self.expect(Token.KEYWORD, lexeme="WAZZUP")
        while not self.expect(Token.KEYWORD, lexeme="BUHBYE", required=False):
            self.expect(Token.KEYWORD, "I HAS A")
            self.accept(self.declare, err_msg="Expected assignment statement")
        
        # Program Body
        while not self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
            self.accept(self.statement, err_msg="Statement not recognized")
        
        return True

    def expr(self): 
        Log.d(f"EXPRESSION: {self.current}")
        if operation := self.expect(Token.OPERATOR, required=False):
            Log.yell("First Operand")
            op1 = self.accept(self.expr, err_msg=f"Expected: <expr>, got {self.current.lexeme}")
            
            match (operation):
                case "NOT":
                    op1 = self.cast(op1, "TROOF")
                    return not bool(op1)
                
                case "MAEK":
                    op1 = self.cast(op1, "TROOF")
                    target = self.expect(Token.KEYWORD)
                    result = self.cast()
                    self._set("it", )
                    return not bool(op1)
                
                case "ANY OF" | "ALL OF":
                    operands = []
                    
                    while self.expect(Token.KEYWORD, lexeme="AN",required=False):
                        op = self.accept(self.expr, err_msg="Expected: bool or expression")
                        # op = self.cast(op, "TROOF")
                        operands.append(op)

                    if operation == "ALL OF":
                        return all(operands)
                    elif operation == "ANY OF":
                        return any(operands)
                    
                case "SMOOSH":
                    operands = [op1]
                    
                    while self.expect(Token.KEYWORD, lexeme="AN", required=False):
                        value = self.accept(self.expr)
                        value = self.cast(op, "YARN")
                        operands.append(value)
                        
                    return "".join(operands)
            
            self.expect(Token.KEYWORD, lexeme="AN")

            Log.yell("Second Operand")
            op2 = self.accept(self.expr, err_msg=f"Expected: <expr>, got {self.current.lexeme}")

            op1, op2 = float(op1), float(op2)
            
            # Arithmetic Operations
            match operation:
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
                
            op1, op2 = bool(op1), bool(op2)
            
            # Boolean Operations
            match operation:
                case "BOTH SAEM":
                    return op1 == op2
                case "DIFFRINT":
                    return op1 != op2
                case "BOTH OF":
                    return op1 & op2
                case "EITHER OF":
                    return op1 | op2
                case "WON OF":
                    return op1 ^ op2
                
                
             
        if got := self.expect(Token.NUMBAR, required=False):
            return float(got) 
        
        if got := self.expect(Token.NUMBR, required=False):
            return int(got) 
        
        if got := self.expect(Token.YARN, required=False):
            return str(got)
        
        if got := self.expect(Token.TROOF, required=False):
            return got == "WIN"
        
        if got := self.expect(Token.IDENTIFIER, required=False):
            _val = self._get(got)
            if _val == None:
                return "(NOOB)"
            else: return _val
        
        return None

    def statement(self):
        # Create a branch for every statement ↓↓↓
        Log.i(f"Got statement: {self.current.lexeme}")
        if self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
            return None

        if self.expect(Token.KEYWORD, lexeme="I HAS A", required=False):
            raise Exception(f"{self.current.pos()} Variable declaration not allowed here")
        
        # user input: GIMMEH
        if self.expect(Token.KEYWORD, lexeme="GIMMEH", required=False):
            var = self.expect(Token.IDENTIFIER)  # Expect an identifier for the variable to store the input
            
            # after 'GIMMEH', we expect user input
            user_input = self.accept(self.input, err_msg="Error occurred while in GIMMEH")
            
            # Set the input value to the variable
            self._set(var, user_input)
            
            # we've stored the value, set IT to the value of the input
            self._set("it", user_input)
            
            return True

        # switch-case block
        if self.expect(Token.KEYWORD, lexeme="WTF?", required=False):
            self.switch_case()

        # <operator> <x> AN <y> | <operator> <x1> AN <x2> ... <xn> | NOT <x>
        if self.expect(Token.OPERATOR, consume=False, required=False):
            Log.i(f"Got operation: {self.current.lexeme}")
            it = self.accept(self.expr, err_msg=f"Error evaluating expression")
            self._set("it", it)

        # <varident> R <expr>
        if self.expect(Token.IDENTIFIER, consume=False, required=False):
            self.accept(self.assign, err_msg=f"Error assigning value to variable")
        
        if self.expect(Token.KEYWORD, lexeme="VISIBLE", required=False):
            self.accept(self.print, err_msg="Error occurred while in VISIBLE")

        if self.expect(Token.KEYWORD, lexeme="O RLY?", required=False):
            self.accept(self.cond, err_msg="Error occurred while in IM IN YR")

        if self.expect(Token.KEYWORD, lexeme="IM IN YR", required=False):
            self.accept(self.loop, err_msg="Error occurred while in IM IN YR")

        if self.expect(Token.KEYWORD, lexeme="MAEK", required=False):
            self.accept(self.cast, err_msg="Error occurred while in IM IN YR")
            
        if self.expect(Token.KEYWORD, lexeme="GTFO", required=False):
            self.flags["brk"] = True
            
        return True

    def print(self):
        first = self.accept(self.expr, f"Expected literal or <expr>, got {self.current.lexeme}")
        operands = [self.cast(first, "YARN")]
                    
        while self.expect(Token.CONCAT, lexeme="+", required=False):
            op = self.accept(self.expr, err_msg="Expected: <expr>")
            operands.append(self.cast(op, "YARN"))

        buffer = "".join(operands) + '\n'
        self.gui.cout(buffer)
        print(buffer, end='')
            
        return True
    
    # Not an abstraction
    def cast(self, val, target):
        match target:
            case "TROOF":
                return bool(val)
            case "NUMBR":
                try:
                    i = int(val)
                    return i
                except:
                    return float(val)
            case "NUMBAR":
                return float(val)
            case "YARN":
                if val == None:
                    return "(nil)"
                elif isinstance(val, bool):
                    return "WIN" if val else "FAIL"
                elif isinstance(val, float):
                    return "%.2f" % val
                elif isinstance(val, int):
                    return str(val)
                else: 
                    return str(val)
            case _:
                return "WAHHH"
    
    # def cast(self, val=None, target=None):
    #     if val != None and target != None:
    #         var = self.expect(Token.IDENTIFIER)
    #         self.expect(Token.KEYWORD, lexeme="A", required=False)
    #         target = self.expect(Token.KEYWORD, required=False)

    #         if target not in ("NUMBR", "NUMBAR", "YARN", "TROOF", "NOOB"):
    #             raise Exception(f"Expected: <TYPE>, got {self.current.lexeme}")

    #     match target:
    #         case "TROOF":
    #             return bool(val)
    #         case "NUMBR":
    #             try:
    #                 i = int(val)
    #                 return i
    #             except:
    #                 return float(val)
    #         case "NUMBAR":
    #             return float(val)
    #         case "YARN":
    #             if val == None:
    #                 return "(nil)"
    #             elif isinstance(val, bool):
    #                 return "WIN" if val else "FAIL"
    #             elif isinstance(val, float):
    #                 return "%.2f" % val
    #             elif isinstance(val, int):
    #                 return str(val)
    #             else: 
    #                 return str(val)
    #         case _:
    #             return "WAHHH"
        
    # def recast(self): # , val=None, target=None
    #     var = self.expect(Token.IDENTIFIER)
    #     match self.typeof()
    #     match target:
    #         case "TROOF":
    #             return bool(val)
    #         case "NUMBR":
    #             return int(val)
    #         case "NUMBAR":
    #             try:
    #                 i = int(val)
    #                 return i
    #             except:
    #                 return float(val)
    #         case "YARN":
    #             if val == None:
    #                 return "(nil)"
    #             elif isinstance(val, bool):
    #                 return "WIN" if val else "FAIL"
    #             elif isinstance(val, float):
    #                 return "%.2f" % val
    #             elif isinstance(val, int):
    #                 return str(val)
    #             else: 
    #                 return str(val)
    #         case _:
    #             return "WAHHH"

    def _set(self, var, val):
        type = self.typeof(val)

        self.vars[var] = val
        self.var_types[var] = type
        self.gui.add_symbol(var, self.cast(val, "YARN"))
        # Log.i(f"SET: {var} = {val}")

    def _get(self, var):
        if var not in self.vars:
            raise Exception(f"Accessing undeclared variable: {var}")
        
        # Log.i(f"GET: {var} => {self.vars[var]}")
        return self.vars[var]
    
    def assign(self):
        var = self.expect(Token.IDENTIFIER)
        self.expect(Token.KEYWORD, lexeme="R")
        
        value = self.accept(self.expr, err_msg="Expected: <expr>")
        
        self._set(var, value)
        
        return True
    
    def declare(self):
        var = self.expect(Token.IDENTIFIER)

        value = None
        if self.expect(Token.KEYWORD, lexeme="ITZ", required=False):
            value = self.accept(self.expr)

        self._set(var, value)

        return True
    
    def typeof(self, value):
        if value == None:
            return "NOOB"
        elif isinstance(value, str):
            return "YARN"
        elif isinstance(value, int):
            return "NUMBR"
        elif isinstance(value, float):
            return "NUMBAR"
        elif isinstance(value, bool):
            return "TROOF"
        
    # MAEK <var> [A] <type>
    # <var> IS NOW A <type> (?)
        
    def input(self):
        var = self.expect(Token.IDENTIFIER)
        _input = self.gui.cin()
        self._set(var, _input)

        return True

    # O RLY?
    
    def loop(self):
        label = self.expect(Token.IDENTIFIER)
        operation = self.expect(Token.KEYWORD, required=False)

        if operation not in ("UPPIN", "NERFIN"): 
            raise Exception(f"Expected UPPIN or NERFIN, got {cond}")

        self.expect(Token.KEYWORD, "YR")

        var = self.expect(Token.IDENTIFIER)
        cond = self.expect(Token.KEYWORD, required=False)

        if cond not in ("TIL", "WILE"):
            raise Exception(f"Expected TIL or WILE, got {cond}")
        
        # Jump to the conditional
        self.vars[label] = int(self.cursor)
        end = None

        # Find the index of the IM OUTTA YR token
        for i in range(self.vars[label], len(self.tokens)):
            if self.tokens[i].lexeme == "IM OUTTA YR":
                if self.tokens[i+1].lexeme == label:
                    end = i+2
                    break

        if end == None: raise Exception(f"Loop \"{label}\" has no matching IM OUTTA YR")

        # Execute loop
        while True:
            # Evaluate condition
            cond_result = self.accept(self.expr)

            if cond == "TIL" and cond_result:
                self.seek(end)
                break
            if cond == "WILE" and not cond_result:
                self.seek(end)
                break

            # Execute loop body
            while not self.expect(Token.KEYWORD, lexeme="IM OUTTA YR", consume=False, required=False):
                self.statement()

                # Handle GTFO
                if self.flags["brk"]:
                    self.flags["brk"] = False
                    break
            
            # Modifier application
            Log.d(f"{operation} {label}")
            if operation == "UPPIN":
                self.vars[var] += 1
            elif operation == "NERFIN":
                self.vars[var] -= 1

            # Reset cursor to loop start
            self.seek(self.vars[label])

        Log.yell("Finished looping!")
        if self._get(label):
            del self.vars[label]

        return True
    
    def switch_case(self):
        # Get the value of the implicit IT variable
        it_value = self._get("it")
        case_matched = False  # Flag to track if a case is matched

        Log.d(f"Starting switch-case. IT value: {it_value}")

        while True:
            # If we encounter OMG, we are now in a case block
            if self.expect(Token.KEYWORD, lexeme="OMG", required=False):
                case_value = self.accept(self.expr, err_msg="Expected case value")

                Log.d(f"Case value: {case_value}, IT value: {it_value}")

                if case_value == it_value:
                    Log.d(f"Case matched: {case_value} == {it_value}")
                    # If case matched, execute the statements inside the case block
                    while True:
                        Log.d("Inside case block")
                        Log.d(f"Current token: {self.current.lexeme}")

                        # Handle GIMMEH input inside the case
                        if self.expect(Token.KEYWORD, lexeme="GIMMEH", required=False):
                            Log.d(f"current token: {self.current.lexeme}")
                            Log.d(f"current token type: {self.current.type}")

                            # Directly process user input without expecting an identifier
                            user_input = self.accept(self.input, err_msg="Error occurred while inside case GIMMEH")

                            # Store the user input in the variable and in IT
                            var = "input_var"  # Default variable name for GIMMEH input
                            self._set(var, user_input)
                            self._set("it", user_input)

                            # Move on to the next statement after GIMMEH
                            continue  # Skip to the next iteration of the case block

                        # Execute other statements inside the case block
                        self.statement()  # Run the general statement handling here

                        # Check if the 'GTFO' is encountered and break out of the loop
                        if self.expect(Token.KEYWORD, lexeme="GTFO", required=False):
                            Log.d("GTFO encountered, exiting case.")
                            break  # Exit the loop when 'GTFO' is encountered

                        # If a break flag is set, exit the loop
                        if self.flags["brk"]:
                            self.flags["brk"] = False
                            break

                    case_matched = True
                    break  # Exit the loop after finding a matching case

            # If no cases matched, check for the default case: OMGWTF
            if self.expect(Token.KEYWORD, lexeme="OMGWTF", required=False):
                Log.d("Default case (OMGWTF) executed.")
                while True:
                    self.statement()  # Execute statements in the default block
                    # Exit if we reach OIC after processing the default block
                    if self.expect(Token.KEYWORD, lexeme="OIC", required=False):
                        Log.d("OIC encountered, exiting default case.")
                        break
                break  # Exit the loop after executing the default case

            # If we've reached the OIC keyword, exit the loop
            elif self.expect(Token.KEYWORD, lexeme="OIC", required=False):
                Log.d("Switch-case ended with OIC.")
                break  # Exit the loop if we encounter OIC


# MAIN
# tokens = Lexer(open("project-testcases/test_1.lol", "r")).get_tokens()

# parser = Parser(tokens)
# success = parser.program()

# # print("Result:", result)
# Log.d("Parsing completed successfully!")