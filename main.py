import customtkinter
import tkinter

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        var = customtkinter.BooleanVar()
        var.set(False)
        
        self.title("my app")
        self.geometry("400x150")
        self.grid_columnconfigure((0, 1), weight=1)

        self.radiobutton_1 = customtkinter.CTkRadioButton(self, text="Выключить через 30 минут", variable=var)
        self.radiobutton_1.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.radiobutton_2 = customtkinter.CTkRadioButton(self, text="Выключить через 1 час", variable=var)
        self.radiobutton_2.grid(row=1, column=0, padx=10, pady=(10, 0), sticky="w")
        
    def button_callback(self):
        print("button pressed")

app = App()
app.mainloop()