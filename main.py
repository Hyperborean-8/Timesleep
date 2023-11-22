import customtkinter as ctk
import time as t
import copy as copy
import math as math

ctk.set_appearance_mode("dark")  # Режимы: системный (стандартный), светлый, тёмный
ctk.set_default_color_theme("blue")  # Темы: синяя (стандартная), тёмно-синяя, зелёная


# Коробка с выбором времени
class SelectTimeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # --- Слайдер и надписи ---
        self.slider_frame = ctk.CTkFrame(self)
        self.slider_frame.grid(row=0, column=0, sticky='news', padx=(0, 5), pady=(5, 0))

        self.time_options = [('4 часа', 14400, 0),
                             ('2 часа', 7200, 1),
                             ('1 час', 3600, 2),
                             ('30 минут', 1800, 3),
                             ('10 минут', 600, 4)]

        self.time_options_rev = copy.deepcopy(self.time_options)
        self.time_options_rev.reverse()

        self.length: int = len(self.time_options)

        # Слайдер для выбора предустановленного времени
        self.time_slider = ctk.CTkSlider(self.slider_frame, from_=0, to=self.length - 1,
                                         number_of_steps=self.length - 1, orientation='vertical',
                                         command=self.change_by_slider)
        self.time_slider.grid(row=0, column=0, padx=10, pady=20, sticky="news")
        self.time_slider.set(0)

        # Надписи из time_options
        self.label_list: list = []
        self.label_frame = ctk.CTkFrame(self.slider_frame, fg_color="transparent")
        self.label_frame.grid(row=0, column=1, padx=10, pady=10, sticky='news')

        for txt, val, pos in self.time_options:
            label = ctk.CTkLabel(self.label_frame, text=txt)
            label.grid(row=pos, column=1, sticky="news")
            self.label_frame.rowconfigure(pos, weight=1)
            self.label_list.append(label)

        # --- Выбор времени ---
        self.time_frame = ctk.CTkFrame(self)
        self.time_frame.grid(row=0, column=1, sticky="news", pady=(5, 0))

        self.time_inner_frame = ctk.CTkFrame(self.time_frame)
        self.time_inner_frame.grid(row=1, column=1, sticky="news")

        self.time_frame.grid_rowconfigure(0, weight=1)
        self.time_frame.grid_rowconfigure(1, weight=0)
        self.time_frame.grid_rowconfigure(2, weight=1)
        self.time_frame.grid_columnconfigure(0, weight=1)
        self.time_frame.grid_columnconfigure(1, weight=0)
        self.time_frame.grid_columnconfigure(2, weight=1)

        self.font = ctk.CTkFont(size=80)
        self.time_entry = ctk.CTkEntry(self.time_inner_frame, font=self.font, width=105, height=80, border_width=0,
                                       corner_radius=0, fg_color='#101010')
        self.current_input = ''
        self.time_entry.grid(row=0, column=0)
        self.time_type = ctk.CTkSegmentedButton(self.time_inner_frame, values=['Минут', 'Часов'],
                                                command=self.change_by_entry)
        self.time_type.grid(row=1, column=0)
        self.time_type.set('Минут')

    def validate_entry(self):
        new_input = self.time_entry.get()

        # Если entry не пустая и последний символ не является цифрой
        if len(new_input) > 0 and not new_input[len(new_input) - 1].isdigit():
            # Удалить последний символ
            self.time_entry.delete(len(new_input) - 1)

        # Если entry длиннее чем 2
        if len(new_input) > 2:
            # Удалить третий символ
            self.time_entry.delete(2)

        self.change_by_entry()

    def change_by_slider(self, x):  # Todo: убрать хард-код и сделать возможность делать свои времена для слайдера
        time_options = copy.deepcopy(self.time_options)
        time_options.reverse()

        print('[01] Слайдер выбран:', time_options[int(x)][0], 'или', time_options[int(x)][1], 'секунд')

        # Установка entry на значение слайдера
        for y in range(len(self.time_type.get()), -1, -1):
            self.time_entry.delete(y)

        if time_options[int(x)][1] <= 5940:

            self.time_type.set('Минут')
            self.time_entry.insert(string=str(math.ceil(time_options[int(x)][1] / 60)), index=0)

        elif time_options[int(x)][1] > 5940:

            self.time_type.set('Часов')
            self.time_entry.insert(string=str(math.ceil(time_options[int(x)][1] / (60 * 60))), index=0)

    def change_by_entry(self, *_x):  # Todo: Сделать чтобы энтри изменял значение слайдера (сделать после создания кастомных слайдеров)
        time_type = self.time_type.get()
        new_time = self.time_entry.get()

        if new_time == '':
            new_time = 0
        else:
            new_time = int(new_time)

        if time_type == 'Минут':
            seconds = new_time * 60
        elif time_type == 'Часов':
            seconds = new_time * (60 * 60)
        else:
            seconds = 0
            print('[!!!] Тип времени не найден!')

        print('[00] В entry вписано:', new_time, time_type, 'или', seconds, 'секунд')


class CurrentTimeFrame(ctk.CTkFrame):  # Todo: Сделать фрейм с текущем временем

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
        self.StopButton = ctk.CTkButton(self, text='Стоп', state=ctk.DISABLED)
        self.StopButton.grid(row=0, column=1, padx=10, pady=10, sticky="news")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.minimized_rows: bool = False
        self.options_hidden: bool = False
        self.timer_on: bool = False
        self.time_set: int = 0
        self.time: int = 0

        # Прикрепление сигнала изменения к переменной
        self.bind("<Key>", self.handle_configure)

        # Настройка окна
        self.title("Timesleep")
        self.geometry("300x315")
        self.resizable(False, False)
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

        # self.SelectTimeFrame.grid_remove()
        # self.CurrentTimeFrame.grid()

        # Это прикол который нам поможет потом))
        # self.attributes('-topmost', True)

    def set_time(self, time):  # Todo: Сделать систему времени
        print('[03] Время установлено на: ', time)

    def start_time(self, time):
        print('[04] Время запущено с', time, 'секундами.')

        # self.ButtonsFrame.StopButton.configure(state=ctk.NORMAL)

    def restart_time(self, time):
        self.time

    def stop_time(self):
        self.time

    def handle_configure(self, _event):  # Todo: Сделать валидацию
        # print('что-то поменялось ', event)
        self.SelectTimeFrame.validate_entry()


app = App()
app.mainloop()
