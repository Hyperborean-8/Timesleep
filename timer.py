import customtkinter as ctk
import copy


# Коробка, показывающая таймер
class CurrentTimeFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        # Центрирование
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=0)
        self.grid_rowconfigure(3, weight=0)
        self.grid_rowconfigure(4, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=1)

        self.label = ctk.CTkLabel(self, text='Компьютер выключится через')
        self.label.grid(row=1, column=1, pady=10)

        self.font = ctk.CTkFont(size=60)

        self.time_label = ctk.CTkLabel(self, text='00:00:00', font=self.font)
        self.time_label.grid(row=2, column=1, pady=(0, 10))

        self.time_bar = ctk.CTkProgressBar(self, height=15, width=250, corner_radius=0)
        self.time_bar.grid(row=3, column=1, pady=(0, 10))

    def update_all(self):
        self.update_timebar()
        self.update_text()

    def update_timebar(self):
        # Todo: Сделать фрейм с циркулярной полоской прогресса "circular progress bar.py"
        self.time_bar.set(self.master.seconds / self.master.seconds_set)

    def update_text(self):

        seconds = copy.deepcopy(self.master.seconds)

        hours = seconds // 3600
        seconds = seconds % 3600

        minutes = seconds // 60
        seconds = seconds % 60

        # Добавляет 0 перед числом, чтобы таймер выглядит как 01:02:50, а не как 1:2:50
        # Не используется, когда остаются только секунды
        def tr(text):
            text = str(text)

            if len(text) < 2:
                text = '0' + text
            return text

        if hours > 0:
            label_text = f'{tr(hours)}:{tr(minutes)}:{tr(seconds)}'
        elif hours == 0 and minutes > 0:
            label_text = f'{tr(minutes)}:{tr(seconds)}'
        elif hours == 0 and minutes == 0:
            label_text = f'{seconds}'
        else:
            label_text = 'Что-то пошло не так'

        # Меняет текст на полученный
        self.time_label.configure(text=label_text)
