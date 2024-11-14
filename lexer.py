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
    KEYWORD = r"\b(HAI|KTHXBYE|WAZZUP|BUHBYE|I HAS A|ITZ|R|AN|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF|BOTH SAEM|DIFFRINT|SMOOSH|MAEK|A|IS NOW A|VISIBLE|GIMMEH|O RLY\?|YA RLY|NO WAI|MEBBE|NO WAI|OIC|WTF\?|OMG|OMGWTF|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|HOW IZ I|IF U SAY SO|GTFO|FOUND YR|I IZ|MKAY)"
    IDENTIFIER = r"\b[a-zA-Z]\w*\b"
    COMMENT = r"(OBTW\s+.*\s+TLDR|BTW [^\n]*)"
    FLOAT = r"\-?\d+\.\d+"
    INTEGER = r"\-?\d+"
    STRING = r"\"[^\n\"]*\""
    BOOL = r"\b(WIN|FAIL)\b"
    NEWLINE = r"(\n|\t|\:\)|\.\.\.)"
    WHITESPACE = r"[ ]+"

    priority = (COMMENT, KEYWORD, WHITESPACE, NEWLINE, IDENTIFIER, FLOAT, INTEGER, STRING, BOOL)
    type = (Token.COMMENT, Token.KEYWORD, Token.WHITESPACE, Token.NEWLINE, Token.IDENTIFIER, Token.FLOAT, Token.INTEGER, Token.STRING, Token.BOOL)

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

        self._tokens = []
        
        print("INTERPRETATION DONE!")
        print("Tokens:", len(self._tokens))

    def get_tokens(self):
        return self._tokens

    def tokenize(self):
        tokens = []
        while self.source_code:
            valid = False
            for pattern, token_type in zip(Pattern.priority, Pattern.type):
                match = re.match(pattern, self.source_code)
                if match:
                    match_str = self.source_code[:match.end()]
                    print(f"{token_type}: {match_str}")
                    tokens.append(Token(match_str, token_type))
                    self.source_code = self.source_code[match.end():]
                    valid = True
                    break
            if valid: continue

            raise ValueError(f"Unexpected character: \"{self.source_code[0]}\"")
        return tokens