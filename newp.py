from lexer import Lexer, Token
from utils import Log
from time import sleep
# from syntax_tree import AST, Node

Log.show(False)

class Parser:
    def __init__(self, gui):
        self.gui = gui
        self.tokens = []
        self.cursor = 0
        self.current = None # self.tokens[self.cursor]

        self.flags = {
            'JMPOUT': False
        }

        # Runtime 
        self.vars = {}
        self.var_types = {}
        self.loops = {}
        self.funcs = {}

        _global_scope = {
            "vars": {},
            "var_types": {},
            "loops": {},
            "funcs": {},
        }

        self.stack = [_global_scope]

    def _push(self, layer):
        self.stack.append(layer)

    def _pop(self):
        if len(self.stack) == 1:
            raise Exception(f"{self.current.pos()} Tried popping an empty stack")
        else: self.stack.pop()

    def _top_of_stack(self):
        return self.stack[-1]

    def set_tokens(self, _tokens):
        self.tokens = _tokens
        self.current = self.tokens[self.cursor]

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
    def accept(self, abstraction, err_msg=f"Unexpected non-terminal!"):
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

    def parse(self):
        self._set("IT", 0)
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
        sleep(0.05)
        if operation := self.expect(Token.OPERATOR, required=False):
            op1 = self.accept(self.expr, err_msg=f"Expected: <expr>, got {self.current.lexeme}")
            
            match operation:
                case "NOT":
                    op1 = self.cast(op1, "TROOF")
                    return not bool(op1)
                
                case "MAEK":
                    pass
                    # # TODO Implement this
                    # op1 = self.cast(op1, "TROOF")
                    # target = self.expect(Token.KEYWORD)
                    # result = self.cast()
                    # self._set("IT", 0)
                    # return not bool(op1)
                
                case "ANY OF" | "ALL OF":
                    operands = []
                    
                    while not self.expect(Token.KEYWORD, lexeme="MKAY", required=False):
                        self.expect(Token.KEYWORD, lexeme="AN")
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
        # Create a branch for everyn statement ↓↓↓
        Log.i(f"Got statement: {self.current}")
        if self.expect(Token.KEYWORD, lexeme="KTHXBYE", consume=False, required=False):
            return None

        if self.expect(Token.KEYWORD, lexeme="I HAS A", required=False):
            raise Exception(f"{self.current.pos()} Variable declaration not allowed here")
        
        # <operator> <x> AN <y> | <operator> <x1> AN <x2> ... <xn> | NOT <x>
        if self.expect(Token.OPERATOR, consume=False, required=False):
            Log.i(f"Got operation: {self.current.lexeme}")
            it = self.accept(self.expr, err_msg=f"Error evaluating expression")
            self._set("IT", it)

        # <varident> R <expr>
        if self.expect(Token.IDENTIFIER, consume=False, required=False):
            self.accept(self.assign, err_msg=f"Error assigning value to variable")
        
        if self.expect(Token.KEYWORD, lexeme="VISIBLE", required=False):
            self.accept(self.print, err_msg="Error occurred while in VISIBLE")

        if self.expect(Token.KEYWORD, lexeme="GIMMEH", required=False):
            self.accept(self.input, err_msg="Error occurred while in GIMMEH")

        if self.expect(Token.KEYWORD, lexeme="O RLY?", required=False):
            self.accept(self.cond, err_msg="Error occurred while in IM IN YR")

        if self.expect(Token.KEYWORD, lexeme="IM IN YR", required=False):
            self.accept(self.loop, err_msg="Error occurred while in IM IN YR")

        if self.expect(Token.KEYWORD, lexeme="MAEK", required=False):
            self.accept(self.cast, err_msg="Error occurred while in IM IN YR")
            
        if self.expect(Token.KEYWORD, lexeme="GTFO", required=False):
            self.flags["JMPOUT"] = True

        if self.expect(Token.KEYWORD, lexeme="HOW IZ I", required=False):
            self.accept(self.def_func, err_msg="Error occured while in I IZ")

        if self.expect(Token.KEYWORD, lexeme="I IZ", required=False):
            self.accept(self.call, err_msg="Error occured while in declaring function")

        if self.expect(Token.KEYWORD, lexeme="FOUND YR", required=False):
            self.accept(self.ret, err_msg="Error occured while in FOUND YR")
            
        return True

    def print(self):
        first = self.accept(self.expr, f"Expected literal or <expr>, got {self.current.lexeme}")
        operands = [self.cast(first, "YARN")]
                    
        while self.expect(Token.CONCAT, lexeme="+", required=False) and not self.expect(Token.KEYWORD, lexeme="MKAY", required=False):
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
        _type = self.typeof(val)

        if var == "IT":
            self.stack[0]["vars"][var] = val
            self.stack[0]["var_types"][var] = _type
            self.gui.add_symbol(var, self.cast(val, "YARN"))
            return
        else:
            self._top_of_stack()["vars"][var] = val
            self._top_of_stack()["var_types"][var] = _type
            self.gui.add_symbol(var, self.cast(val, "YARN"))

        # self.vars[var] = val
        # self.var_types[var] = _type
        Log.i(f"SET: {var} = {val}")

    def _get(self, var):
        if var == "IT":
            Log.i(f"GET: {var} => {self.stack[0]["vars"][var]}")
            return self.stack[0]["vars"][var]
        
        if var not in self._top_of_stack()["vars"]:
            raise Exception(f"{self.current.pos()} Accessing undeclared variable: {var}")
        
        Log.i(f"GET: {var} => {self._top_of_stack()["vars"][var]}")
        return self._top_of_stack()["vars"][var]
        
    
    def _get_loop(self, var):
        if var not in self._top_of_stack()["loops"]:
            raise Exception(f"Loop label not found: {var}")
        
        # Log.i(f"GET: {var} => {self.loops[var]}")
        return self._top_of_stack()["loops"][var]
    
    def _get_func(self, fun):
        if fun not in self.funcs:
            raise Exception(f"{self.current.pos()} Function undefined: {fun}")
        
        # Log.i(f"GET: {var} => {self.funcs[var]}")
        return self.funcs[fun]
    
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
        operation = self.expect(Token.KEYWORD)

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
                self.accept(self.statement)

                # Handle GTFO
                if self.flags["BRK"]:
                    self.flags["BRK"] = False
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
    
    def call(self):
        funcident = self.expect(Token.IDENTIFIER)
        arg_count = 0
        jmp, params = self._get_func(funcident)

        scope = {
            "name": funcident,
            "jmp": -1,
            "vars": {},
            "var_types": {},
            "loop": {},
            "ret": -1
        }

        for p in range(len(params)):
            self.expect(Token.KEYWORD, lexeme="YR")

            arg = self.accept(self.expr, err_msg="Error in accepting arguments")

            param = params[p]
            scope["vars"][param] = arg
            arg_count += 1

            if not self.expect(Token.KEYWORD, lexeme="AN", required=False):
                break

        if arg_count != len(params):
            raise Exception(f"Mismatched number of arguments, expected {len(params)}, got {arg_count}")
        
        # Position where the cursor will jump to after returning from function
        ret = int(self.cursor)
        
        scope["jmp"] = jmp
        scope["ret"] = ret

        # Go back to the position where the function was called
        self._push(scope)
        self.seek(self._top_of_stack()["jmp"])

        # Run function body
        while not self.expect(Token.KEYWORD, lexeme="IF U SAY SO", consume=False, required=False):
            self.accept(self.statement, err_msg=f"Error encountered in {self.current.pos()} {funcident}()")
            if self.flags["JMPOUT"]: 
                self.flags["JMPOUT"] = False
                break
        
        # Go back to the position where the function was called
        # Then pop the function scope from the stack
        self.seek(self._top_of_stack()["ret"])
        self._pop()

        return True
    
    def def_func(self):
        funcident = self.expect(Token.IDENTIFIER)

        params = []
        while self.expect(Token.KEYWORD, lexeme="YR", required=False):
            param = self.expect(Token.IDENTIFIER)
            params.append(param)
            if not self.expect(Token.KEYWORD, lexeme="AN", required=False):
                break
        jmp = int(self.cursor)
        
        self.funcs[funcident] = (jmp, params)

        while not self.expect(Token.KEYWORD, lexeme="IF U SAY SO", required=False):
            self.next()

        return True

    def ret(self):
        # Assign return value to [IT]
        ret_val = self.accept(self.expr, err_msg=f"{self.current.pos()} Invalid return value")
        self._set("IT", ret_val)

        # Set JMP flag
        self.flags["JMPOUT"] = True

        return True

# MAIN
# tokens = Lexer(open("project-testcases/05_bool.lol", "r")).get_tokens()

# parser = Parser()
# success = parser.parse()

# # print("Result:", result)
# Log.d("Parsing completed successfully!")