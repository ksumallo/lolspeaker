class Error(Exception):
    _gui = None

    def __init__(self, message):
        super().__init__(message)
        if Error._gui != None:
            Error._gui.cout(message)

    @staticmethod
    def set_cout(cout):
        Error._gui = cout

class SyntaxError(Error):
    def __init__(self, current, expected):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tSyntaxError: Expected '{expected}', but got {repr(current.lexeme)}"
        super().__init__(self.message)

class VariableError(Error):
    def __init__(self, current, var):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tVariableError: Accessing undeclared variable '{var}'"
        super().__init__(self.message)

class FunctionUndefinedError(Error):
    def __init__(self, current, identifier):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tFunctionUndefinedError: Accessing undeclared variable '{identifier}'"
        super().__init__(self.message)        

class LoopLabelError(Error):
    def __init__(self, current, label):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tVariableError: Loop with label '{label}' not found"
        super().__init__(self.message)

class LoopUnclosedError(Error):
    def __init__(self, current, label):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\LoopUnclosedError: Loop '{label}' has no matching IM OUTTA YR"
        super().__init__(self.message)

class ArgumentMismatchError(Error):
    def __init__(self, current, expected):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tArgumentMismatchError: Mismatched number of arguments, expected {expected}, got {curr.lexeme}"
        super().__init__(self.message)

class ExpressionError(Error):
    def __init__(self, current):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\ExpressionError: Encountered error while parsing expression"
        super().__init__(self.message)

class UnknownError(Error):
    def __init__(self, current):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tUnknownError: Couldn't identify error"
        super().__init__(self.message)

class CastError(Error):
    def __init__(self, current, _from, _to, val='?'):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\CastError: Cannot cast {_from} to {_to} (Value: {val})"
        super().__init__(self.message)

class CastToUnknownTypeError(Error):
    def __init__(self, current, _from, _to, val='?'):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\CastToUknownTypeError: Trying to cast {_from} to unknown type {_to} (Value: {val})"
        super().__init__(self.message)

class IllegalDeclareError(Error):
    def __init__(self, current):
        self.line = current.line
        self.col = current.col
        self.message = f"At line {self.line}, col {self.col}:\n\tIllegalDeclareError: Variable declaration not allowed here"
        super().__init__(self.message)