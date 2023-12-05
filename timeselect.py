import customtkinter as ctk
import copy
import math


# Коробка с выбором времени
class SelectTimeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # Слайдер и надписи
        self.SliderFrame = ctk.CTkFrame(self)
        self.SliderFrame.grid(row=0, column=0, sticky='news', padx=(0, 5))

        self.time_options = [('4 часа', 14400, 0),  # TODO: Потом сделать систему кастомных времён
                             ('2 часа', 7200, 1),
                             ('1 час', 3600, 2),
                             ('30 минут', 1800, 3),
                             ('10 минут', 600, 4)]

        self.time_options_rev = copy.deepcopy(self.time_options)
        self.time_options_rev.reverse()

        self.length: int = len(self.time_options)

        # Слайдер для выбора предустановленного времени
        self.time_slider = ctk.CTkSlider(self.SliderFrame, from_=0, to=self.length - 1,
                                         number_of_steps=self.length - 1, orientation='vertical',
                                         command=self.change_by_slider)
        self.time_slider.grid(row=0, column=0, padx=10, pady=20, sticky="news")
        self.time_slider.set(0)

        # Надписи из time_options
        self.label_list: list = []
        self.LabelFrame = ctk.CTkFrame(self.SliderFrame, fg_color="transparent")
        self.LabelFrame.grid(row=0, column=1, padx=10, pady=10, sticky='news')

        for txt, val, pos in self.time_options:
            label = ctk.CTkLabel(self.LabelFrame, text=txt)
            label.grid(row=pos, column=1, sticky="news")
            self.LabelFrame.rowconfigure(pos, weight=1)
            self.label_list.append(label)

        # Основная коробка
        self.TimeFrame = ctk.CTkFrame(self)
        self.TimeFrame.grid(row=0, column=1, sticky="news")

        # Внутренняя коробка, которая будет оставаться в центре основной
        self.TimeInnerFrame = ctk.CTkFrame(self.TimeFrame)
        self.TimeInnerFrame.grid(row=1, column=1, sticky="news")

        # Центрирование внутренней коробки
        self.TimeFrame.grid_rowconfigure(0, weight=1)
        self.TimeFrame.grid_rowconfigure(1, weight=0)
        self.TimeFrame.grid_rowconfigure(2, weight=1)
        self.TimeFrame.grid_columnconfigure(0, weight=1)
        self.TimeFrame.grid_columnconfigure(1, weight=0)
        self.TimeFrame.grid_columnconfigure(2, weight=1)

        # Энтри для вписывание времени
        self.font = ctk.CTkFont(size=80)  # Шрифт
        self.time_entry = ctk.CTkEntry(self.TimeInnerFrame, font=self.font, width=105, height=80, border_width=0,
                                       corner_radius=0, fg_color='#101010')
        self.time_entry.grid(row=0, column=0)

        # Выбор типа времени
        self.time_type = ctk.CTkSegmentedButton(self.TimeInnerFrame, values=['Минут', 'Часов'],
                                                command=self.change_by_entry)
        self.time_type.grid(row=1, column=0)
        self.time_type.set('Минут')

        # Переменные
        self.current_input = ''

# Валидация вписанного текста (текст должен быть числом, без минуса или букв)
    def validate_entry(self):
        new_input = self.time_entry.get()

        # Если entry не пустая и последний символ не является цифрой
        if len(new_input) > 0 and not new_input[len(new_input) - 1].isdigit():
            # Удалить последний символ
            self.time_entry.delete(len(new_input) - 1)

        # Если пользователь поставил минус перед числом, удалить минус
        if len(new_input) > 0 and new_input[0] == '-':
            self.time_entry.delete(0)

        # Если entry длиннее чем 2
        if len(new_input) > 2:
            # Удалить третий символ
            self.time_entry.delete(2)

        # Не менять значение, если работает таймер
        if not self.master.timer_on:
            self.change_by_entry()

    # Функция, вызываемая при изменении слайдера
    def change_by_slider(self, x):
        time_options = copy.deepcopy(self.time_options)
        time_options.reverse()

        seconds = time_options[int(x)][1]

        print('[01] Слайдер выбран:', time_options[int(x)][0], 'или', seconds, 'секунд')

        # Установка entry на значение слайдера
        for y in range(len(self.time_type.get()), -1, -1):
            self.time_entry.delete(y)

        # Автоматически менять время на часы/минуты, если время слишком большое/маленькое
        if seconds <= 5940:

            self.time_type.set('Минут')
            self.time_entry.insert(string=str(math.ceil(seconds / 60)), index=0)

        elif seconds > 5940:

            self.time_type.set('Часов')
            self.time_entry.insert(string=str(math.ceil(seconds / 3600)), index=0)

        # Установить время в app()
        self.master.set_timer(seconds)

    # Функция, вызываемая если пользователь что-то вписал в энтри
    def change_by_entry(self, *_x):
        # Todo: Сделать чтобы энтри изменял значение слайдера (сделать после создания кастомных слайдеров)
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

        # Установить время в app()
        self.master.set_timer(seconds)
