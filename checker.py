class Error(Exception):
    _gui = None

    def __init__(self, message):
        super().__init__(self.message)
        if Error._gui:
            Error._gui.cout(self.message)

    @staticmethod
    def set_cout(cout):
        Error._gui = cout

class SyntaxError(Exception):
    def __init__(self, current, expected):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tSyntaxError: Expected {expected}, but got {current.lexeme}"
        super().__init__(self.message)

class VariableError(Exception):
    def __init__(self, current, var):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tVariableError: Accessing undeclared variable '{var}'"
        super().__init__(self.message)

class FunctionUndefinedError(Exception):
    def __init__(self, current, identifier):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tFunctionUndefinedError: Accessing undeclared variable '{identifier}'"
        super().__init__(self.message)        

class LoopLabelError(Exception):
    def __init__(self, current, label):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tVariableError: Loop with label '{label}' not found"
        super().__init__(self.message)

class LoopUnclosedError(Exception):
    def __init__(self, current, label):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\LoopUnclosedError: Loop '{label}' has no matching IM OUTTA YR"
        super().__init__(self.message)

class ArgumentMismatchError(Exception):
    def __init__(self, current, expected):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tArgumentMismatchError: Mismatched number of arguments, expected {expected}, got {curr.lexeme}"
        super().__init__(self.message)

class ExpressionError(Exception):
    def __init__(self, current):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\ExpressionError: Encountered error while parsing expression"
        super().__init__(self.message)

class UnknownError(Exception):
    def __init__(self, current):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tUnknownError: Couldn't identify error"
        super().__init__(self.message)

class IllegalDeclareError(Exception):
    def __init__(self, current):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tIllegalDeclareError: Variable declaration not allowed here"
        super().__init__(self.message)