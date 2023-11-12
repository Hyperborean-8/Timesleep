import customtkinter as ctk
import tkinter as tk

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


class Topbar(ctk.CTkFrame):
    master = None

    def __init__(self, master):
        super().__init__(master)

        self.button = ctk.CTkButton(self, text="Старт")
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="news")


# Коробка с выбором времени
class RadioboxFrame(ctk.CTkFrame):
    radiobutton_list: list = []
    radiobutton_list2: list = []

    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Переменная которая позволяет выбрать только одну опцию
        self.v = ctk.IntVar()
        self.v.set(1)

        # Заранее выбранные опции
        self.time_options = [('Выключить через 10 минут', '10 минут', 600, 1),
                             ('Выключить через 30 минут', '30 минут', 1800, 2),
                             ('Выключить через 1 час', '1 час', 3600, 3),
                             ('Выключить через 2 часа', '2 часа', 7200, 4),
                             ('Выключить через 4 часа', '4 часа', 14400, 5)]

        for txt, small_txt, val, pos in self.time_options:
            # Кнопки
            radiobutton = ctk.CTkRadioButton(self, text=txt, variable=self.v, value=val)
            radiobutton.grid(row=pos, column=0, padx=10, pady=(5, 5), sticky="w")
            self.radiobutton_list.append(radiobutton)
            # Кнопки при уменьшении окна
            radiobutton = ctk.CTkRadioButton(self, text=small_txt, variable=self.v, value=val)
            radiobutton.grid(row=pos, column=0, padx=10, pady=(5, 5), sticky="w")
            radiobutton.grid_remove()
            self.radiobutton_list2.append(radiobutton)

        # Своё время
        radiobutton = ctk.CTkRadioButton(self, text='Своё время', variable=self.v, value=-1)
        radiobutton.grid(row=(len(self.time_options) + 1), column=0, padx=10, pady=(5, 5), sticky="w")
        self.radiobutton_list.append(radiobutton)
        # Своё время при уменьшении окна
        radiobutton = ctk.CTkRadioButton(self, text='Своё', variable=self.v, value=-1)
        radiobutton.grid(row=(len(self.time_options) + 1), column=0, padx=10, pady=(5, 5), sticky="w")
        self.radiobutton_list2.append(radiobutton)

class CurrentTimeFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.label = ctk.CTkLabel(self, text='Компьютер выключится через: ')
        self.label.grid(row=1, column=0, padx=10, pady=(0, 10), stick='news')

        self.timeleft = ctk.CTkLabel(self, text='30 минут')
        self.timeleft.grid(row=2, column=0, padx=10, pady=(0, 10), stick='news')

        self.timebar = ctk.CTkProgressBar(self)
        self.timebar.grid(row=3, column=0, padx=10, pady=10, stick='news')
        self.grid_columnconfigure(0, weight=1)


class ButtonsFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # Кнопки
        self.button = ctk.CTkButton(self, text="Старт")
        self.button.grid(row=0, column=0, padx=10, pady=10, sticky="news")


class App(ctk.CTk):
    minimized_rows: bool = False
    options_hidden: bool = False

    def __init__(self):
        super().__init__()

        # Прикрепление сигнала изменения к переменной
        self.bind("<Configure>", self.handle_configure)

        # Настройка окна
        self.title("Timesleep")
        self.geometry("300x500")
        # self.minsize(130, 200)

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=0)

        # Frames
        self.RadioboxFrame = RadioboxFrame(self)
        self.RadioboxFrame.master = self
        self.RadioboxFrame.grid(row=0, column=0, padx=10, pady=5, sticky="news")

        self.CurrentTimeFrame = CurrentTimeFrame(self)
        self.CurrentTimeFrame.grid(row=1, column=0, padx=10, pady=5, sticky='news')

        self.ButtonsFrame = ButtonsFrame(self)
        self.ButtonsFrame.grid(row=2, column=0, padx=0, pady=0, sticky="wes")

        # Это прикол который нам поможет потом))
        # self.attributes('-topmost', True)

    def handle_configure(self, _event):
        if not self.minimized_rows and self.winfo_width() <= 250:
            self.minimize_rows()
        elif self.minimized_rows and self.winfo_width() > 250:
            self.maximize_rows()

        if not self.options_hidden and self.winfo_height() <= 300:
            self.hide_options()
        elif self.options_hidden and self.winfo_height() > 300:
            self.show_options()

    def minimize_rows(self):
        for radiobox in self.RadioboxFrame.radiobutton_list:
            radiobox.grid_remove()
        for radiobox in self.RadioboxFrame.radiobutton_list2:
            radiobox.grid()

        print('[00] Свернуть')
        self.minimized_rows = True

    def maximize_rows(self):
        for radiobox in self.RadioboxFrame.radiobutton_list:
            radiobox.grid()
        for radiobox in self.RadioboxFrame.radiobutton_list2:
            radiobox.grid_remove()

        print('[00] Развернуть')
        self.minimized_rows = False

    def hide_options(self):
        self.RadioboxFrame.grid_remove()

        print('[01] Скрыть опции')
        self.options_hidden = True

    def show_options(self):
        self.RadioboxFrame.grid()

        self.options_hidden = False
        print('[01] Показать опции')


app = App()
app.mainloop()