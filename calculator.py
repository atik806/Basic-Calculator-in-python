import tkinter as tk
from tkinter import ttk, font
import math

class ScientificCalculator(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("pro calculator")
        self.geometry("400x600")
        self.resizable(False, False)
        self.configure(bg="#2e2e2e")
        
        # Custom font setup
        self.default_font = font.Font(family="Segoe UI", size=12)
        self.display_font = font.Font(family="Segoe UI", size=20)
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=self.default_font, padding=10)
        self.style.map("TButton",
            foreground=[('active', 'white'), ('!disabled', 'black')],
            background=[
                ('active', '#4a4a4a'),
                ('!disabled', '#f0f0f0'),
                ('pressed', '#3a3a3a')
            ]
        )
        
        self.create_widgets()
        self.bind_keys()
        
    def create_widgets(self):
        # Display frame
        self.display_var = tk.StringVar()
        display_frame = ttk.Frame(self)
        display_frame.pack(pady=20, padx=20, fill=tk.X)
        
        self.display = ttk.Entry(
            display_frame,
            textvariable=self.display_var,
            font=self.display_font,
            justify="right",
            state="readonly"
        )
        self.display.pack(fill=tk.X, ipady=10)
        
        # Button grid
        button_frame = ttk.Frame(self)
        button_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        
        buttons = [
            ('sin', 'cos', 'tan', '√'),
            ('7', '8', '9', '/'),
            ('4', '5', '6', '*'),
            ('1', '2', '3', '-'),
            ('0', '.', '=', '+'),
            ('π', 'e', 'log', '^'),
            ('(', ')', 'C', '⌫')
        ]
        
        for row_idx, row in enumerate(buttons):
            for col_idx, text in enumerate(row):
                btn = ttk.Button(
                    button_frame,
                    text=text,
                    command=lambda t=text: self.on_button_click(t)
                )
                btn.grid(
                    row=row_idx,
                    column=col_idx,
                    sticky="nsew",
                    padx=2,
                    pady=2
                )
                button_frame.grid_columnconfigure(col_idx, weight=1)
            button_frame.grid_rowconfigure(row_idx, weight=1)
        
    def bind_keys(self):
        self.bind("<Return>", lambda e: self.calculate())
        self.bind("<BackSpace>", lambda e: self.delete_last())
        self.bind("<Escape>", lambda e: self.clear_display())
        
        for char in "0123456789+-*/.()":
            self.bind(char, lambda e, c=char: self.add_to_display(c))
            
    def on_button_click(self, text):
        if text == "=":
            self.calculate()
        elif text == "C":
            self.clear_display()
        elif text == "⌫":
            self.delete_last()
        else:
            self.add_to_display(text)
            
    def add_to_display(self, text):
        current = self.display_var.get()
        special_chars = {
            '√': 'sqrt(',
            '^': '**',
            'π': str(math.pi),
            'e': str(math.e),
            'sin': 'math.sin(',
            'cos': 'math.cos(',
            'tan': 'math.tan(',
            'log': 'math.log10('
        }
        self.display_var.set(current + special_chars.get(text, text))
    
    def clear_display(self):
        self.display_var.set('')
    
    def delete_last(self):
        current = self.display_var.get()
        self.display_var.set(current[:-1])
    
    def calculate(self):
        try:
            expression = self.display_var.get()
            result = eval(expression, {"__builtins__": None}, {"math": math})
            self.display_var.set(str(round(result, 10)))
        except Exception as e:
            self.display_var.set("Error")
            self.after(1000, self.clear_display)
    
if __name__ == "__main__":
    app = ScientificCalculator()
    app.mainloop() 