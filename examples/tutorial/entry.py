from tkinter import ttk
import tkinter as tk

def validate_entry(text):
    return text.isdecimal()

root = tk.Tk()
root.config(width=300, height=200)
root.title("My App")
entry = ttk.Entry(
    validate="key",
    validatecommand=(root.register(validate_entry), "%S")
)
entry.place(x=50, y=50, width=150)
root.mainloop()
