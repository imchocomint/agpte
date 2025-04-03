import json
import os
import tkinter as tk
import pygments
from pygments import lexers, formatters

class SyntaxHighlighter:
    def __init__(self, editor):
        self.editor = editor
        self.language_config = {}

    def load_language_config(self, language):
        lang_config_file = f"{language}.json" if os.path.exists(f"{language}.json") else None
        
        if lang_config_file:
            with open(lang_config_file, 'r') as config_file:
                self.language_config = json.load(config_file)
                self.editor.display_language_info(language)

        self.highlight_syntax()

    def highlight_syntax(self):
        self.editor.text_area.tag_remove("highlight", "1.0", "end")

        code = self.editor.text_area.get(1.0, tk.END)
        # Basic highlighting for keywords
        for keyword, color in self.language_config.get('keywords', {}).items():
            start_index = "1.0"
            while True:
                start_index = self.editor.text_area.search(keyword, start_index, tk.END)
                if not start_index:
                    break
                end_index = f"{start_index}+{len(keyword)}c"
                self.editor.text_area.tag_add("highlight", start_index, end_index)
                self.editor.text_area.tag_config("highlight", foreground=color)
                start_index = end_index

        # You can implement similar logic for strings and comments if needed.
