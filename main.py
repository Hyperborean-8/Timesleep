from PIL import Image
from icecream import ic
import customtkinter as ctk
import copy
import math
import os
import settings

ctk.set_appearance_mode("dark")  # Режимы: системный (стандартный), светлый, тёмный
ctk.set_default_color_theme("blue")  # Темы: синяя (стандартная), тёмно-синяя, зелёная
ctk.deactivate_automatic_dpi_awareness()  # Программа больше не реагирует на изменение интерфейса ОС.

# Отладка
debug = False # Режим отладки. Не позволяет программе выключить компьютер.
ic(debug)
if not debug: ic.disable()


def hide_window():
    app.withdraw()


def show_window():
    app.deiconify()


def turn_off_computer():
    if not debug:
        os.system("shutdown /s /t 1")


# Окно подтверждения о выходе из программы, когда таймер работает
class ConfirmationWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Настройки
        self.title("Timesleep")
        self.geometry("430x180")
        self.resizable(False, False)

        # Центрирование элементов
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=0)
        self.rowconfigure(2, weight=1)

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=0)
        self.columnconfigure(2, weight=1)

        # Фрейм с надписью
        self.LabelFrame = ctk.CTkFrame(self, width=350, fg_color='transparent')
        self.LabelFrame.grid(row=1, column=1)

        self.label = ctk.CTkLabel(self.LabelFrame, text='Вы уверены что хотите выйти? Таймер всё ещё работает.')
        self.label.grid(row=0, column=0)

        # Переменная значения чекбокса
        self.var = ctk.BooleanVar()
        # Привязка сигнала изменения к функции
        self.var.trace('w', self.change_other_checkbox)

        self.checkbox = ctk.CTkCheckBox(self.LabelFrame, text='Больше не спрашивать', font=('Arial', 12),
                                        checkbox_height=16, checkbox_width=16, border_width=2,
                                        command=self.confirm_settings, variable=self.var)
        self.checkbox.grid(row=2, column=0, padx=5, pady=5)

        # Фрейм с кнопками
        self.ButtonsFrame = ctk.CTkFrame(self, height=20, fg_color='transparent')
        self.ButtonsFrame.grid(row=3, column=1, sticky='ews', pady=(0, 15))

        self.quit_button = ctk.CTkButton(self.ButtonsFrame, text='Отмена', command=self.return_back)
        self.quit_button.grid(row=0, column=0)
        self.ButtonsFrame.columnconfigure(1, weight=1)
        self.cancel_button = ctk.CTkButton(self.ButtonsFrame, text='Выйти', fg_color='#c72800', hover_color='#941f01',
                                           command=self.exit)
        self.cancel_button.grid(row=0, column=2)

    # Функция, отвечающая за чекбокс "Не спрашивать больше"
    def confirm_settings(self):
        settings.set('confirmation', 'dont_ask', str(bool(self.checkbox.get())))

    def exit(self):
        self.master.destroy()

    def return_back(self):
        self.master.focus()
        self.destroy()

    # Функция, переключаящая чекбокс в окне Настроек
    def change_other_checkbox(self, *args):
        if self.master.SettingsWindow is not None and self.master.SettingsWindow.winfo_exists():
            self.master.SettingsWindow.var.set(self.var.get())


# Окно с настройками
class SettingsWindow(ctk.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Настройки")
        self.geometry("400x300")
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.MainFrame = ctk.CTkFrame(self)
        self.MainFrame.grid(row=0, column=0, pady=10, padx=10, sticky='news')

        # Переменная чекбокса TODO: Переименовать
        self.var = ctk.BooleanVar()
        # Привязка сигнала изменения к функции
        self.var.trace('w', self.change_other_checkbox)

        self.checkbox = ctk.CTkCheckBox(self.MainFrame, text='Не спрашивать подтверждение выхода при запущенном таймере',
                                        checkbox_width=16, checkbox_height=16, command=self.confirm_settings, variable=self.var)
        self.checkbox._text_label.configure(wraplength=350)
        self.checkbox.grid(row=0, column=0, padx=10, pady=10)

    # Функция, изменяющая настройку подтверждения при таймере
    def confirm_settings(self):
        settings.set('confirmation', 'dont_ask', str(bool(self.checkbox.get())))

    # Функция, переключаящая чекбокс в окне Подтверждения
    def change_other_checkbox(self, *args):
        ic(self.master.ConfirmationWindow)
        if self.master.ConfirmationWindow is not None and self.master.ConfirmationWindow.winfo_exists():
            ic(self.master.ConfirmationWindow.var.set)
            self.master.ConfirmationWindow.var.set(self.var.get())

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


# Фрейм с кнопками
class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")

        self.icon_settings_light = ctk.CTkImage(Image.open(os.path.join(image_path, "icon-settings-light.png")),
                                                size=(20, 20))
        self.icon_minimize_light = ctk.CTkImage(Image.open(os.path.join(image_path, "icon-minimize-light.png")),
                                                size=(20, 20))

        # Кнопки "Старт" и "Стоп"
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.start_button = ctk.CTkButton(self, text="Старт", state=ctk.DISABLED, command=master.start_timer)
        self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.stop_button = ctk.CTkButton(self, text='Стоп', command=master.stop_timer)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.stop_button.grid_remove()

        # Дополнительные кнопки
        self.ExtraButtonFrame = ctk.CTkFrame(self, height=30, width=150, fg_color='transparent')
        self.ExtraButtonFrame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        self.ExtraButtonFrame.columnconfigure(0, weight=0)
        self.ExtraButtonFrame.columnconfigure(1, weight=1)

        self.settings_button = ctk.CTkButton(self.ExtraButtonFrame, text='', image=self.icon_settings_light,
                                             width=20, height=20, command=self.master.open_settings)
        self.settings_button.grid(row=0, column=0)

        self.minimize = ctk.CTkButton(self.ExtraButtonFrame, text='', image=self.icon_minimize_light,
                                      width=20, height=20)
        self.minimize.grid(row=0, column=2)

    def hide_start(self):
        self.start_button.grid_remove()
        self.stop_button.grid()

    def show_start(self):
        self.start_button.grid()
        self.stop_button.grid_remove()


# Основной класс для программы
class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Настройки
        settings.check_config()

        # Переменные для таймера
        self.timer_after = None
        self.minimized_rows: bool = False
        self.options_hidden: bool = False
        self.timer_on: bool = False
        self.extra_second: bool = False
        self.seconds_set: int = 0
        self.seconds: int = 0

        # Переменные для окон
        self.SettingsWindow = None
        self.ConfirmationWindow = None

        # Прикрепление сигналов к функциям
        self.bind("<Key>", self.handle_configure)
        self.protocol('WM_DELETE_WINDOW', self.exit_or_confirm)

        # Настройка окна
        self.title("Timesleep")
        self.geometry("300x315")
        self.resizable(False, False)

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Коробки
        self.SelectTimeFrame = SelectTimeFrame(self)
        self.SelectTimeFrame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="news")
        self.CurrentTimeFrame = CurrentTimeFrame(self)
        self.CurrentTimeFrame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky='news')
        self.CurrentTimeFrame.grid_remove()
        self.ButtonsFrame = ButtonsFrame(self)
        self.ButtonsFrame.grid(row=1, column=0, padx=10, pady=5, sticky='news')

        # Это прикол который нам поможет потом))
        # self.attributes('-topmost', True)

    # Ставит время таймера
    def set_timer(self, seconds):
        print('[03] Время установлено на: ', seconds)

        self.seconds_set = seconds

        if seconds == 0:
            self.ButtonsFrame.start_button.configure(state=ctk.DISABLED)
        else:
            self.ButtonsFrame.start_button.configure(state=ctk.NORMAL)

    # Запускает таймер с выставленными секундами
    def start_timer(self):
        print('[04] Время запущено с', self.seconds_set, 'секундами.')

        self.timer_on = True
        self.extra_second = True

        self.seconds = self.seconds_set

        self.SelectTimeFrame.grid_remove()
        self.CurrentTimeFrame.grid()

        self.ButtonsFrame.hide_start()

        self.update_timer()

    # Останавливает таймер
    def stop_timer(self):
        self.timer_on = False

        self.SelectTimeFrame.grid()
        self.CurrentTimeFrame.grid_remove()

        self.ButtonsFrame.show_start()

        self.after_cancel(self.timer_after)

    # Функция, которая вызывает саму себя и обновляет время каждую секунду
    def update_timer(self):

        if self.extra_second:
            self.seconds += 1
            self.extra_second = False

        if self.seconds > 0 and self.timer_on:
            self.seconds -= 1

            self.CurrentTimeFrame.update_all()

            self.timer_after = self.after(1000, self.update_timer)
        elif self.seconds == 0 and self.timer_on:
            print('[05] Таймер сработал!')

            turn_off_computer()

        else:
            pass

    # Функция, вызываемая при нажатии клавиш
    def handle_configure(self, _event):

        # Валидация
        self.SelectTimeFrame.validate_entry()

    def exit_or_confirm(self):

        if settings.get('confirmation', 'dont_ask'):
            self.destroy()

        elif self.timer_on and (self.ConfirmationWindow is None or not self.ConfirmationWindow.winfo_exists()):

            self.ConfirmationWindow = ConfirmationWindow(self)  # Создать окно, если его нет или уничтожено
            self.after(20, self.ConfirmationWindow.focus)

        elif self.timer_on:
            self.ConfirmationWindow.focus()  # Если окно есть, переключиться на него

        else:
            self.destroy()

    def open_settings(self):
        if self.SettingsWindow is None or not self.SettingsWindow.winfo_exists():
            self.SettingsWindow = SettingsWindow(self)  # create window if its None or destroyed
            self.after(10, self.SettingsWindow.focus)
        else:
            self.SettingsWindow.focus()  # if window exists focus it


# Главные цикл
app = App()
app.mainloop()
