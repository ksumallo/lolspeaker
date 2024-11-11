import tkinter as Tk
from tkinter import Frame, Button, Label, Text, Entry, filedialog, StringVar
from tkinter.ttk import Treeview

from os.path import abspath
from ctypes import windll

import re

windll.shcore.SetProcessDpiAwareness(1)

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
    KEYWORD = r"\b(HAI|KTHXBYE|WAZZUP|BUHBYE|I HAS A|ITZ|R|AN|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF|BOTH SAEM|DIFFRINT|SMOOSH|MAEK|A|IS NOW A|VISIBLE|GIMMEH|O RLY?|MEBBE|NO WAI|OIC|WTF?|OMG|OMGWTF|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|HOW IZ I|IF U SAY SO|GTFO|FOUND YR|I IZ|MKAY)\b"
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

class Lexer:
    def __init__(self):
        file = open("example.lol")

        source_code = file.read()
        self._tokens = []
        self._tokens.extend(self.lexer(source_code))
        
        print("INTERPRETATION DONE!")
        print("Tokens:", len(self._tokens))

    def get_tokens(self):
        return self._tokens

    def lexer(self, code):
        tokens = []
        while code:
            valid = False
            for pattern, token_type in zip(Pattern.priority, Pattern.type):
                match = re.match(pattern, code)
                if match:
                    print(f"{token_type}: {match}")
                    tokens.append(Token(match, token_type))
                    code = code[match.end():]
                    valid = True
                    break
            if valid: continue

            raise ValueError(f"Unexpected character: \"{code[0]}\"")
        return tokens

Lexer()