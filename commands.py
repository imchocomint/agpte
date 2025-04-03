import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import os

class CommandHandler:
    def __init__(self, editor):
        self.editor = editor

    def open_file(self):
        file_path = filedialog.askopenfilename(defaultextension=".txt")
        if file_path:
            extension = os.path.splitext(file_path)[1]
            language = self.get_language_by_extension(extension)
            
            with open(file_path, 'r') as file:
                content = file.read()
                self.editor.text_area.delete(1.0, tk.END)
                self.editor.text_area.insert(tk.END, content)

            self.editor.syntax_highlighter.load_language_config(language)
            self.editor.display_language_info(language)
            self.editor.update_line_count()

    def get_language_by_extension(self, extension):
        for lang, exts in self.editor.language_mapping.items():
            if extension in exts:
                return lang
        return "Plain Text"

    def save_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt")
        if file_path:
            with open(file_path, 'w') as file:
                file.write(self.editor.text_area.get(1.0, tk.END))
            messagebox.showinfo("Info", "File saved successfully!")

    def find_text(self):
        self.find_window = tk.Toplevel(self.editor.master)
        self.find_window.title("Find Text")

        tk.Label(self.find_window, text="Find:").grid(row=0, column=0)
        self.find_entry = tk.Entry(self.find_window)
        self.find_entry.grid(row=0, column=1)

        tk.Button(self.find_window, text="Find", command=self.perform_find).grid(row=1, column=0, columnspan=2)

    def perform_find(self):
        search_text = self.find_entry.get()
        start_pos = self.editor.text_area.search(search_text, "1.0", tk.END)
        if start_pos:
            self.editor.text_area.tag_remove("highlight", "1.0", tk.END)
            end_pos = f"{start_pos}+{len(search_text)}c"
            self.editor.text_area.tag_add("highlight", start_pos, end_pos)
            self.editor.text_area.tag_config("highlight", background="yellow")

    def replace_text(self):
        search_text = simpledialog.askstring("Replace Text", "Find:")
        replace_text = simpledialog.askstring("Replace Text", "Replace with:")
        content = self.editor.text_area.get(1.0, tk.END)

        if search_text and replace_text is not None:
            new_content = content.replace(search_text, replace_text)
            self.editor.text_area.delete(1.0, tk.END)
            self.editor.text_area.insert(tk.END, new_content)
            self.editor.syntax_highlighter.highlight_syntax()
