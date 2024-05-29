import tkinter as tk
from tkinter import filedialog, messagebox
from transformers import MarianMTModel, MarianTokenizer
import torch

# Base class for GUI
class BaseGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Language Translation App")
        self.geometry("600x400")
        self.create_widgets()

    def create_widgets(self):
        raise NotImplementedError("Subclass must implement abstract method")

# Mixin class for file handling (demonstrating multiple inheritance)
class FileHandlerMixin:
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename()
        return file_path

    def read_file(self, file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return text

# Main application class using multiple inheritance
class TranslationApp(BaseGUI, FileHandlerMixin):
    def __init__(self, model, tokenizer, src_lang, tgt_lang):
        self.model = model  # Encapsulation: storing model within the class
        self.tokenizer = tokenizer
        self.src_lang = src_lang
        self.tgt_lang = tgt_lang
        super().__init__()

    def create_widgets(self):
        self.label = tk.Label(self, text="Select a text file to translate", font=("Arial", 16))
        self.label.pack(pady=20)
        
        self.select_button = tk.Button(self, text="Select Text File", command=self.select_file)
        self.select_button.pack(pady=10)
        
        self.input_text = tk.Text(self, height=10, width=50)
        self.input_text.pack(pady=10)
        
        self.translate_button = tk.Button(self, text="Translate", command=self.translate_text)
        self.translate_button.pack(pady=10)
        
        self.output_text = tk.Text(self, height=10, width=50)
        self.output_text.pack(pady=10)

    def select_file(self):
        file_path = self.open_file_dialog()
        if file_path:
            text = self.read_file(file_path)
            self.input_text.delete(1.0, tk.END)
            self.input_text.insert(tk.END, text)

    def translate_text(self):
        input_text = self.input_text.get(1.0, tk.END).strip()
        if input_text:
            translation = self.translate(input_text)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, translation)

    def translate(self, text):
        tokens = self.tokenizer.prepare_seq2seq_batch(src_texts=[text], return_tensors='pt')
        translation_tokens = self.model.generate(**tokens)
        translated_text = self.tokenizer.batch_decode(translation_tokens, skip_special_tokens=True)[0]
        return translated_text

# Custom decorator to confirm before closing the app (demonstrating decorators)
def confirm_close(func):
    def wrapper(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            func(self)
    return wrapper

# Subclass to demonstrate method overriding and use of decorator
class ConfirmCloseTranslationApp(TranslationApp):
    def __init__(self, model, tokenizer, src_lang, tgt_lang):
        super().__init__(model, tokenizer, src_lang, tgt_lang)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    @confirm_close
    def on_closing(self):
        self.destroy()

# Polymorphism: We could have multiple models and they would work similarly in this interface
model_name = "Helsinki-NLP/opus-mt-en-de"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

# Running the application
if __name__ == "__main__":
    app = ConfirmCloseTranslationApp(model, tokenizer, "en", "de")
    app.mainloop()