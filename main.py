import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class RadioboxFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        
        self.v = ctk.IntVar()
        self.v.set(1)

        self.time_options = [('Выключить через 10 минут', 600, 1),
                             ('Выключить через 30 минут', 1800, 2),
                             ('Выключить через 1 час', 3600, 3)]
        
        radiobutton_list=[]
        
        for txt, val, pos in self.time_options:
            radiobutton = ctk.CTkRadioButton(self, text=txt, variable=self.v, value=val)
            radiobutton.grid(row=pos, column=0, padx=10, pady=(10, 10), sticky="w")
            radiobutton_list.append(radiobutton)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("my app")
        self.geometry("400x300")
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.RadioboxFrame = RadioboxFrame(self)
        self.RadioboxFrame.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")
        
        self.button = ctk.CTkButton(self, text="my button", command=self.button_callback)
        self.button.grid(row=1, column=0, padx=10, pady=10, sticky="ew")

    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()