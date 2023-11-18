import customtkinter as ctk
import time

ctk.set_appearance_mode("dark")  # Modes: system (default), light, dark
ctk.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green


# Коробка с выбором времени
class SelectTimeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)
        # Заранее выбранные опции
        self.time_options = [('4 часа', 14400, 0),
                             ('2 часа', 7200, 1),
                             ('1 час', 3600, 2),
                             ('30 минут', 1800, 3),
                             ('10 минут', 600, 4),
                             ('0 минут', 0, 5)]

        self.SetTimeSlider = ctk.CTkSlider(self, from_=0, to=1, number_of_steps=5, orientation='vertical')
        self.SetTimeSlider.grid(row=0, column=0, padx=10, pady=20, sticky="news")
        self.label_list: list = []

        self.label_frame = ctk.CTkFrame(self)
        self.label_frame.grid(row=0, column=1, padx=10, pady=10, sticky='news')
        for txt, val, pos in self.time_options:
            # Кнопки
            label = ctk.CTkLabel(self.label_frame, text=txt)
            label.grid(row=pos, column=1, sticky="nesw")
            self.label_frame.rowconfigure(pos, weight=1)
            self.label_list.append(label)


class CurrentTimeFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)



class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Кнопки
        self.StartButton = ctk.CTkButton(self, text="Старт", command=lambda: master.start_time(master.time_set))
        self.StartButton.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.RestartButton = ctk.CTkButton(self, text='Перезапустить')
        self.RestartButton.grid(row=0, column=0, padx=10, pady=10, sticky="news")
        self.RestartButton.grid_remove()
        self.StopButton = ctk.CTkButton(self, text='Стоп', state='disabled')
        self.StopButton.grid(row=0, column=1, padx=10, pady=10, sticky="news")


class App(ctk.CTk):
    def __init__(self, bg_color = 'transparent'):
        super().__init__()

        self.minimized_rows: bool = False
        self.options_hidden: bool = False
        self.timer_on: bool = False
        self.time_set: int = 0
        self.time: int = 0

        # # Прикрепление сигнала изменения к переменной
        # self.bind("<Configure>", self.handle_configure)

        # Настройка окна
        self.title("Timesleep")
        self.geometry("300x380")
        # self.minsize(130, 200)

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Frames
        self.SelectTimeFrame = SelectTimeFrame(self)
        self.SelectTimeFrame.grid(row=0, column=0, padx=10, pady=5, sticky="news")
        self.CurrentTimeFrame = CurrentTimeFrame(self)
        self.CurrentTimeFrame.grid(row=0, column=0, padx=10, pady=5, sticky='news')
        self.CurrentTimeFrame.grid_remove()
        self.ButtonsFrame = ButtonsFrame(self)
        self.ButtonsFrame.grid(row=1, column=0, padx=10, pady=5, sticky='news')

        # Это прикол который нам поможет потом))
        # self.attributes('-topmost', True)

    def set_time(self, time):
        print(time)

    def start_time(self, time):
        print(time)

    def restart_time(self, time):
        self.time

    def stop_time(self):
        self.time

app = App()
app.mainloop()
