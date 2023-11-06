import tkinter as tk
import customtkinter as ctk

class RadioBtn:
    def __init__(self, root):
        self.v = ctk.IntVar()
        self.v.set(1)

        tk.Label(root, text="Choose your favorite\nprogramming language",
              justify = "left", bg="lightyellow").grid()

        self.languages = [("Python",1),
                    ("Perl",2),
                    ("Java",3),
                    ("C++",4),
                    ("None",5)]

        btn_list=[]
        for txt, val in self.languages:
            rbtn=tk.Radiobutton(root, text=txt, variable=self.v, 
                        command=self.show_choice,
                        value=val)
            rbtn.grid(row=val, column=0)
            btn_list.append(rbtn)

        tk.Button(root, text="Print value", bg="lightblue",
               command=self.print_val).grid(row=9, sticky="nsew")
        tk.Button(root, text="Quit", bg="orange",
               command=root.quit).grid(row=10, sticky="nsew")

    def print_val(self):
        print(self.choice, self.languages[self.choice-1])

    def show_choice(self):
        self.choice=self.v.get()
        print(self.choice, self.languages[self.choice-1])

root = tk.Tk()
rb=RadioBtn(root)
root.mainloop()