from io import TextIOWrapper
import re

class Token:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    NUMBR = "NUMBR"
    NUMBAR = "NUMBAR"
    YARN = "YARN"
    TROOF = "TROOF"
    OPERATOR = "OPERATOR"
    COMMENT = "COMMENT"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"

    def __init__(self, lexeme, type=None):
        self.lexeme = lexeme
        self.type = type

    def get_lexeme(self):
        return self.lexeme
    
    def get_type(self):
        return self.type

# Dictionary for LOLCODE keyword descriptions
keyword_descriptions = {
    "NUMBR Literal": "Integer literal",
    "NUMBAR Literal": "Floating-point literal",
    "YARN Literal": "String literal",
    "TROOF Literal": "Boolean literal (WIN/FAIL)",
    "TYPE Literal": "Type identifier",
    "<identifier>": "Variable or function name",
    "HAI": "Start of program",
    "KTHXBYE": "End of program",
    "WAZZUP": "Alternative start of program",
    "BUHBYE": "Alternative end of program",
    "BTW": "Single-line comment",
    "OBTW": "Start of multi-line comment",
    "TLDR": "End of multi-line comment",
    "I HAS A": "Variable declaration",
    "ITZ": "Initial value assignment",
    "R": "Assignment operator",
    "SUM OF": "Addition operator",
    "DIFF OF": "Subtraction operator",
    "PRODUKT OF": "Multiplication operator",
    "QUOSHUNT OF": "Division operator",
    "MOD OF": "Modulo operator",
    "BIGGR OF": "Maximum of two values",
    "SMALLR OF": "Minimum of two values",
    "BOTH OF": "Logical AND",
    "EITHER OF": "Logical OR",
    "WON OF": "Logical XOR",
    "NOT": "Logical NOT",
    "ANY OF": "Any operand is true",
    "ALL OF": "All operands are true",
    "BOTH SAEM": "Equality check",
    "DIFFRINT": "Inequality check",
    "SMOOSH": "String concatenation",
    "MAEK": "Type casting",
    "A": "Type specifier in casting",
    "IS NOW A": "Dynamic type change",
    "VISIBLE": "Output statement",
    "GIMMEH": "Input statement",
    "O RLY?": "Start of conditional block",
    "YA RLY": "True branch of conditional",
    "MEBBE": "Else-if branch",
    "NO WAI": "False branch of conditional",
    "OIC": "End of conditional block",
    "WTF?": "Start of switch-case block",
    "OMG": "Case in switch block",
    "OMGWTF": "Default case in switch block",
    "IM IN YR": "Start of loop block",
    "UPPIN": "Increment loop variable",
    "NERFIN": "Decrement loop variable",
    "YR": "Loop variable specifier",
    "TIL": "Loop until condition",
    "WILE": "Loop while condition",
    "IM OUTTA YR": "End of loop block",
    "HOW IZ I": "Function definition",
    "IF U SAY SO": "End of function definition",
    "GTFO": "Exit loop or function",
    "FOUND YR": "Return value from function",
    "I IZ": "Function call",
    "MKAY": "End of function call arguments",
}

class Pattern:
    KEYWORD = r"\b(HAI|KTHXBYE|WAZZUP|BUHBYE|I HAS A|ITZ|R|AN|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF|BOTH SAEM|DIFFRINT|SMOOSH|MAEK|A|IS NOW A|VISIBLE|GIMMEH|O RLY|MEBBE|NO WAI|OIC|WTF|OMG|OMGWTF|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|HOW IZ I|IF U SAY SO|GTFO|FOUND YR|I IZ|MKAY)\b"
    IDENTIFIER = r"\b[a-zA-Z]\w*\b"
    COMMENT = r"(OBTW\s+.*\s+TLDR|BTW [^\n]*)"
    NUMBAR = r"\-?\d+\.\d+"
    NUMBR = r"\-?\d+"
    YARN = r"\"[^\n\"]*\""
    TROOF = r"\b(WIN|FAIL)\b"
    NEWLINE = r"(\n|\t|\:\)|\.\.\.)"
    WHITESPACE = r" "
    YARN_DELIMITER = r" "

    priority = (COMMENT, WHITESPACE, NEWLINE, KEYWORD, IDENTIFIER, NUMBAR, NUMBR, YARN, TROOF)
    type = (Token.COMMENT, Token.WHITESPACE, Token.NEWLINE, Token.KEYWORD, Token.IDENTIFIER, Token.NUMBAR, Token.NUMBR, Token.YARN, Token.TROOF)

class Classification:
    DELIMITER = r"\b(HAI|KTHXBYE)\b"

    LITERAL = r"\b\.+\b"

class Lexer:
    def __init__(self, input):
        # Check if it is an opened file
        # Otherwise, [input] is a plain string
        if isinstance(input, TextIOWrapper):
            _file = open("example.lol")
            self.source_code = _file.read()
        elif isinstance(input, str):
            self.source_code = input
        else: raise TypeError(f"Cannot accept {type(input)}. Input a string or a File.")
        
        self.tokens = self.tokenize() # Tokenize becomes part of __init__

    def get_tokens(self):  # Use get_item to return value
        return self.tokens

    def tokenize(self):
        tokens = []
        while self.source_code:
            valid = False
            for pattern, token_type in zip(Pattern.priority, Pattern.type):
                match = re.match(pattern, self.source_code)
                if match:
                    match_str = self.source_code[:match.end()]
                    token_formal = Token(match_str, token_type)
                    tokens.append([token_formal.get_lexeme(), token_formal.get_type(), keyword_descriptions.get(token_formal.get_lexeme(), "Unknown")])  # Added description
                    self.source_code = self.source_code[match.end():]
                    valid = True
                    break
            if valid: continue

            raise ValueError(f"Unexpected character: \"{self.source_code[0]}\"")
        print("INTERPRETATION DONE!") # Relocated at the bottom for console readability
        print("Tokens:", len(tokens))
        print(tokens)
        for token in tokens:
            print(f"{token[1]}: {token[0]} - {token[2]}") 
        return tokens
=======
from io import TextIOWrapper
import re

class Token:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    INTEGER = "INTEGER"
    FLOAT = "FLOAT"
    STRING = "STRING"
    BOOL = "BOOL"
    OPERATOR = "OPERATOR"
    COMMENT = "COMMENT"
    NEWLINE = "NEWLINE"
    WHITESPACE = "WHITESPACE"

    def __init__(self, lexeme, type=None):
        self.lexeme = lexeme
        self.type = type

    def get_lexeme(self):
        return self.lexeme
    
    def get_type(self):
        return self.type

# Dictionary for LOLCODE keyword descriptions
keyword_descriptions = {
    "NUMBR Literal": "Integer literal",
    "NUMBAR Literal": "Floating-point literal",
    "YARN Literal": "String literal",
    "TROOF Literal": "Boolean literal (WIN/FAIL)",
    "TYPE Literal": "Type identifier",
    "<identifier>": "Variable or function name",
    "HAI": "Start of program",
    "KTHXBYE": "End of program",
    "WAZZUP": "Alternative start of program",
    "BUHBYE": "Alternative end of program",
    "BTW": "Single-line comment",
    "OBTW": "Start of multi-line comment",
    "TLDR": "End of multi-line comment",
    "I HAS A": "Variable declaration",
    "ITZ": "Initial value assignment",
    "R": "Assignment operator",
    "SUM OF": "Addition operator",
    "DIFF OF": "Subtraction operator",
    "PRODUKT OF": "Multiplication operator",
    "QUOSHUNT OF": "Division operator",
    "MOD OF": "Modulus operator",
    "BIGGR OF": "Maximum of two values",
    "SMALLR OF": "Minimum of two values",
    "BOTH OF": "Logical AND",
    "EITHER OF": "Logical OR",
    "WON OF": "Logical XOR",
    "NOT": "Logical NOT",
    "ANY OF": "Any operand is true",
    "ALL OF": "All operands are true",
    "BOTH SAEM": "Equality check",
    "DIFFRINT": "Inequality check",
    "SMOOSH": "String concatenation",
    "MAEK": "Type casting",
    "A": "Type specifier in casting",
    "IS NOW A": "Dynamic type change",
    "VISIBLE": "Output statement",
    "GIMMEH": "Input statement",
    "O RLY?": "Start of conditional block",
    "YA RLY": "True branch of conditional",
    "MEBBE": "Else-if branch",
    "NO WAI": "False branch of conditional",
    "OIC": "End of conditional block",
    "WTF?": "Start of switch-case block",
    "OMG": "Case in switch block",
    "OMGWTF": "Default case in switch block",
    "IM IN YR": "Start of loop block",
    "UPPIN": "Increment loop variable",
    "NERFIN": "Decrement loop variable",
    "YR": "Loop variable specifier",
    "TIL": "Loop until condition",
    "WILE": "Loop while condition",
    "IM OUTTA YR": "End of loop block",
    "HOW IZ I": "Function definition",
    "IF U SAY SO": "End of function definition",
    "GTFO": "Exit loop or function",
    "FOUND YR": "Return value from function",
    "I IZ": "Function call",
    "MKAY": "End of function call arguments",
    " ": "Whitespace",
    "\t": "Whitespace",
    "\n": "Newline",
    "troof": "literal",

}

class Pattern:
    KEYWORD = r"\b(HAI|KTHXBYE|WAZZUP|BUHBYE|I HAS A|ITZ\b|R|AN|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF|BOTH SAEM|DIFFRINT|SMOOSH|MAEK|A|IS NOW A|VISIBLE|GIMMEH|O RLY\?|YA RLY|NO WAI|MEBBE|NO WAI|OIC|WTF\?|OMG|OMGWTF|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|HOW IZ I|IF U SAY SO|GTFO|FOUND YR|I IZ|MKAY)"
    IDENTIFIER = r"\b[a-zA-Z]\w*\b"
    COMMENT = r"(OBTW\s+.*\s+TLDR|BTW [^\n]*)"
    FLOAT = r"\-?\d+\.\d+"
    INTEGER = r"\-?\d+"
    STRING = r"\"[^\n\"]*\""
    BOOL = r"\b(WIN|FAIL)\b"
    NEWLINE = r"(\n|\:\)|\.\.\.)"
    WHITESPACE = r" |\t"

    priority = (COMMENT, WHITESPACE, NEWLINE, BOOL, KEYWORD, IDENTIFIER, FLOAT, INTEGER, STRING)
    type = (Token.COMMENT, Token.WHITESPACE, Token.NEWLINE, Token.BOOL, Token.KEYWORD, Token.IDENTIFIER, Token.FLOAT, Token.INTEGER, Token.STRING)

class Lexer:
    def __init__(self, input):
        # Check if it is an opened file
        # Otherwise, [input] is a plain string
        if isinstance(input, TextIOWrapper):
            _file = open("example.lol")
            self.source_code = _file.read()
        elif isinstance(input, str):
            self.source_code = input
        else: raise TypeError(f"Cannot accept {type(input)}. Input a string or a File.")
        
        self.tokens = self.tokenize() # Tokenize becomes part of __init__

    def get_tokens(self):  # Use get_item to return value
        return self.tokens

    def tokenize(self):
        tokens = []
        while self.source_code:
            valid = False
            for pattern, token_type in zip(Pattern.priority, Pattern.type):
                match = re.match(pattern, self.source_code)
                if match:
                    match_str = self.source_code[:match.end()]
                    token_formal = Token(match_str, token_type)
                    tokens.append([token_formal.get_lexeme(), token_formal.get_type(), keyword_descriptions.get(token_formal.get_lexeme(), "Unknown")])  # Added description
                    self.source_code = self.source_code[match.end():]
                    valid = True
                    break
            if valid: continue

            raise ValueError(f"Unexpected character: \"{self.source_code[0]}\"")
        print("INTERPRETATION DONE!") # Relocated at the bottom for console readability
        print("Tokens:", len(tokens))
        print(tokens)
        for token in tokens:
            print(f"{token[1]}: {token[0]} - {token[2]}") 
        return tokens
