import tkinter as tk
import json
import os
import pygments
from tkinter import messagebox, simpledialog, filedialog
from commands import CommandHandler
from syntax_highlighter import SyntaxHighlighter

class TextEditor:
    def __init__(self, master):
        self.master = master
        self.master.title("agpte")
        
        self.text_area = tk.Text(master, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill='both')

        self.load_config()
        self.syntax_highlighter = SyntaxHighlighter(self)
        self.command_handler = CommandHandler(self)

        self.language_label = tk.Label(master, text='Language: None', anchor=tk.W)
        self.language_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.format_label = tk.Label(master, text='Formatting: None', anchor=tk.W)
        self.format_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.line_count_label = tk.Label(master, text='Lines: 0', anchor=tk.W)
        self.line_count_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.configure_editor()
        self.create_menu()
        self.bind_key_events()

    def load_config(self):
        with open('config.json', 'r') as file:
            self.config = json.load(file)

        with open('languages.json', 'r') as file:
            self.language_mapping = json.load(file)['languages']

    def configure_editor(self):
        self.text_area.config(font=(self.config["font"], self.config["font_size"]),
                              bg=self.config["bg_color"], fg=self.config["font_color"])

    def create_menu(self):
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        file_menu = tk.Menu(menu)
        menu.add_cascade(label='File', menu=file_menu)
        file_menu.add_command(label='Open', command=self.command_handler.open_file)
        file_menu.add_command(label='Save', command=self.command_handler.save_file)
        file_menu.add_separator()
        file_menu.add_command(label='Exit', command=self.master.quit)

        edit_menu = tk.Menu(menu)
        menu.add_cascade(label='Edit', menu=edit_menu)
        edit_menu.add_command(label='Find', command=self.command_handler.find_text)
        edit_menu.add_command(label='Replace', command=self.command_handler.replace_text)

        keybinds_text = (
            f"Keybinds: "
            f"{self.config['keybinds']['save']}  Save, "
            f"{self.config['keybinds']['open']}  Open, "
            f"{self.config['keybinds']['exit']}  Exit, "
            f"{self.config['keybinds']['find']}  Find, "
            f"{self.config['keybinds']['replace']}  Replace"
        )
        self.status_bar = tk.Label(self.master, text=keybinds_text, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def bind_key_events(self):
        self.master.bind('<Control-s>', lambda event: self.command_handler.save_file())
        self.master.bind('<Control-o>', lambda event: self.command_handler.open_file())
        self.master.bind('<Control-q>', lambda event: self.master.quit())
        self.master.bind('<Control-f>', lambda event: self.command_handler.find_text())
        self.master.bind('<Control-r>', lambda event: self.command_handler.replace_text())
        self.master.bind('<Return>', self.auto_indent)

    def display_language_info(self, language):
        self.language_label.config(text=f'Language: {language}')
        self.update_line_count()

    def update_line_count(self):
        line_count = int(self.text_area.index('end-1c').split('.')[0])
        self.line_count_label.config(text=f'Lines: {line_count}')

    def auto_indent(self, event):
        current_index = self.text_area.index(tk.INSERT)
        current_line = self.text_area.get(f"{current_index.split('.')[0]}.0", current_index).strip()
        if current_line.endswith(':'):
            self.text_area.insert(current_index, '    ')  # Insert four spaces
        return "break"

if __name__ == "__main__":
    root = tk.Tk()
    editor = TextEditor(root)
    root.mainloop()
