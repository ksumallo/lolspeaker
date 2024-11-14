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

class Pattern:
    KEYWORD = r"\b(HAI|KTHXBYE|WAZZUP|BUHBYE|I HAS A|ITZ|R|AN|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF|BOTH SAEM|DIFFRINT|SMOOSH|MAEK|A|IS NOW A|VISIBLE|GIMMEH|O RLY|MEBBE|NO WAI|OIC|WTF|OMG|OMGWTF|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|HOW IZ I|IF U SAY SO|GTFO|FOUND YR|I IZ|MKAY)\b"
    IDENTIFIER = r"\b[a-zA-Z]\w*\b"
    COMMENT = r"(OBTW\s+.*\s+TLDR|BTW [^\n]*)"
    FLOAT = r"\-?\d+\.\d+"
    INTEGER = r"\-?\d+"
    STRING = r"\"[^\n\"]*\""
    BOOL = r"\b(WIN|FAIL)\b"
    NEWLINE = r"(\n|\t|\:\)|\.\.\.)"
    WHITESPACE = r" "

    priority = (COMMENT, WHITESPACE, NEWLINE, KEYWORD, IDENTIFIER, FLOAT, INTEGER, STRING, BOOL)
    type = (Token.COMMENT, Token.WHITESPACE, Token.NEWLINE, Token.KEYWORD, Token.IDENTIFIER, Token.FLOAT, Token.INTEGER, Token.STRING, Token.BOOL)
     
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

    def get_tokens(self):  #Use get_item to return value
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
                    tokens.append([token_formal.get_lexeme(), token_formal.get_type()])
                    self.source_code = self.source_code[match.end():]
                    valid = True
                    break
            if valid: continue

            raise ValueError(f"Unexpected character: \"{self.source_code[0]}\"")
        print("INTERPRETATION DONE!") # Relocated at the bottom for console readability
        print("Tokens:", len(tokens))
        print(tokens)
        for token in tokens:
            print(f"{token[1]}: {token[0]}")
        return tokens
