import tkinter as tk


def hide_window():
    top_level.withdraw()  # hide the top level window


root = tk.Tk()
root.title("Main Window")

# create top level window
top_level = tk.Toplevel(root)
top_level.title("Top Level Window")

# add a button to the main window
button = tk.Button(root, text="Hide Window", command=hide_window)
button.pack(pady=20)

root.mainloop()