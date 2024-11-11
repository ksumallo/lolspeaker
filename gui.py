import tkinter as Tk
from tkinter import Frame, Button, Label, Text, Entry, filedialog, StringVar, END
from tkinter.ttk import Treeview

from pathlib import Path
from os.path import abspath
from ctypes import windll

import re

windll.shcore.SetProcessDpiAwareness(1)

class Token:
    KEYWORD = "KEYWORD"
    IDENTIFIER = "IDENTIFIER"
    LITERAL = "LITERAL"

    def __init__(self, lexeme, type):
        self.lexeme = lexeme
        self.type = type

class Pattern:
    KEYWORD = "^(HAI|KTHXBYE|WAZZUP|BUHBYE|BTW|OBTW|TLDR|I HAS A|ITZ|R|SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF|BOTH OF|EITHER OF|WON OF|NOT|ANY OF|ALL OF|BOTH SAEM|DIFFRINT|SMOOSH|MAEK|A|IS NOW A|VISIBLE|GIMMEH|O RLY?|MEBBE|NO WAI|OIC|WTF?|OMG|OMGWTF|IM IN YR|UPPIN|NERFIN|YR|TIL|WILE|IM OUTTA YR|HOW IZ I|IF U SAY SO|GTFO|FOUND YR|I IZ|MKAY)$"
    IDENTIFIER = "^[_a-zA-Z][_a-zA-Z0-9]{0,}$"
    LITERAL = "^[_a-zA-Z][_a-zA-Z0-9]{0,}$"

class LOLCodeInterpreter:
    def __init__(self):
        pane_pad = 8

        self.root = Tk.Tk()
        self.root.title("LOLSPEAKER")

        self.frame = Frame(self.root)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.columnconfigure(2, weight=1)
        self.frame.rowconfigure(0, weight=1)
        self.frame.rowconfigure(2, weight=1)
        self.frame.pack()

        # SOURCE PANE
        self.pane_source = Frame(self.frame)
        self.pane_source.grid(row=0, column=0, padx=pane_pad, pady=pane_pad)

        self.file_picker_row = Frame(self.pane_source)
        self.file_picker_row.pack(side="top", fill="x", expand=True)

        self.file_picker_path = StringVar(value="")
        self.file_picker_text = Entry(self.file_picker_row, textvariable=self.file_picker_path, state="disabled")
        self.file_picker_text.pack(side="left", fill="both", expand=True)

        self.import_btn = Button(self.file_picker_row, text="Import", command=self.import_file)
        self.import_btn.pack(side="right")
        
        self.editor = Text(self.pane_source, wrap="char")
        self.editor.pack(side="bottom")

        # LEXEME TABLE PANE
        self.pane_lexemes = Frame(self.frame)
        self.pane_lexemes.grid(row=0, column=1, sticky="ns", padx=pane_pad, pady=pane_pad)

        self.label_lexemes = Label(self.pane_lexemes, text="Lexemes")
        self.label_lexemes.pack(side="top")

        self.lexeme_table = Treeview(self.pane_lexemes, columns=("frequency"))
        self.lexeme_table.heading("#0", text="Lexeme")
        self.lexeme_table.heading("frequency", text="Classification")
        self.lexeme_table.pack(fill="y", expand=True)

        # SYMBOL TABLE PANE
        self.pane_symbols = Frame(self.frame)
        self.pane_symbols.grid(row=0, column=2, sticky="ns", padx=pane_pad, pady=pane_pad)

        self.label_symbols = Label(self.pane_symbols, text="Symbols")
        self.label_symbols.pack(side="top")

        self.symbol_table = Treeview(self.pane_symbols, columns=("value"))
        self.symbol_table.heading("#0", text="Identifier")
        self.symbol_table.heading("value", text="Value")
        self.symbol_table.pack(fill="both", expand=True)

        # EXECUTION
        self.execute_btn = Button(self.frame, text="Execute")
        self.execute_btn.grid(row=1, column=0, columnspan=3, sticky="ew", pady=pane_pad, padx=pane_pad)

        self.console = Text(self.frame, wrap="char", bg="#000000", fg="#ffffff")
        self.console.grid(row=2, column=0, columnspan=3, sticky="ews", padx=pane_pad, pady=pane_pad)
        
    def start(self):
        self.root.mainloop()

    def import_file(self):
        # Accept only .lol or .lols files
        file = filedialog.askopenfile(filetypes=[("LOLCODE File", "*.lol"), ("LOLCODE File", "*.lols")])

        # Display the absolute file of the selected file
        self.file_picker_path.set(str(abspath(file.name)))

        data = file.read()
        self.editor.insert(Tk.END, data)

    def lexer(self, code):
        tokens = []
        while code != "":
            _identifier = re.match(Pattern.IDENTIFIER)

interpreter = LOLCodeInterpreter()
interpreter.start()

