# Стандартные библиотеки
import configparser
import copy
import math
import os
import logging
from logging.handlers import RotatingFileHandler
from datetime import datetime

# Загруженные библиотеки
from PIL import Image
from icecream import ic
import customtkinter as ctk

# Локальные модули
import settings
import timeselect
import timer
import popups
from language import Language

# Базовая настройка customtkinter
ctk.set_appearance_mode("dark")  # Режимы: системный (стандартный), светлый, тёмный
ctk.set_default_color_theme("blue")  # Темы: синяя (стандартная), тёмно-синяя, зелёная
ctk.deactivate_automatic_dpi_awareness()  # Программа больше не реагирует на изменение интерфейса ОС.

# Отладка
debug = True
if not debug: ic.disable()

# Логирование
handler = RotatingFileHandler(f"log.log", maxBytes=1 * 1024 * 1024,
                              backupCount=5)  # Размер каждого лога из пяти не будет превышать 1 МБ

logging.basicConfig(level=logging.DEBUG if debug else logging.INFO, handlers=[handler],
                    format='%(asctime)s | %(levelname)s - %(name)s | %(message)s', datefmt='%D - %H:%M:%S')


def hide_window():
    app.withdraw()


def show_window():
    app.deiconify()


def turn_off_computer():
    if not debug:
        os.system("shutdown /s /t 1")


# Фрейм с кнопками
class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        language = self.master.Language

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

        self.start_button = ctk.CTkButton(self, textvariable=language.vars['buttons']['start_timer'],
                                          state=ctk.DISABLED, command=master.start_timer)
        self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.stop_button = ctk.CTkButton(self, textvariable=language.vars['buttons']['stop_timer'],
                                         command=master.stop_timer)
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

        # Логгер
        self.logger = logging.getLogger(__name__)

        # Настройки
        settings.check_config()
        self.Language = Language()

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
        self.SelectTimeFrame = timeselect.SelectTimeFrame(self)
        self.SelectTimeFrame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="news")
        self.CurrentTimeFrame = timer.CurrentTimeFrame(self)
        self.CurrentTimeFrame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky='news')
        self.CurrentTimeFrame.grid_remove()
        self.ButtonsFrame = ButtonsFrame(self)
        self.ButtonsFrame.grid(row=1, column=0, padx=10, pady=5, sticky='news')

        # Это прикол который нам поможет потом))
        # self.attributes('-topmost', True)

        self.logger.info('The __main__ module has been fully initialized')

    # Ставит время таймера
    def set_timer(self, seconds):

        self.seconds_set = seconds

        if seconds == 0:
            self.ButtonsFrame.start_button.configure(state=ctk.DISABLED)
        else:
            self.ButtonsFrame.start_button.configure(state=ctk.NORMAL)

        self.logger.info(f'The timer time has been set to {seconds} seconds')

    # Запускает таймер с выставленными секундами
    def start_timer(self):

        self.timer_on = True
        self.extra_second = True

        self.seconds = self.seconds_set

        self.SelectTimeFrame.grid_remove()
        self.CurrentTimeFrame.grid()

        self.ButtonsFrame.hide_start()

        self.update_timer()

        self.logger.info(f'The timer was started with {self.seconds_set} seconds.')

    # Останавливает таймер
    def stop_timer(self):
        self.timer_on = False

        self.SelectTimeFrame.grid()
        self.CurrentTimeFrame.grid_remove()

        self.ButtonsFrame.show_start()

        self.after_cancel(self.timer_after)

        self.logger.info('The timer has been stopped')

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
            self.logger.info('The timer reached zero and the computer was shut down.')

            turn_off_computer()

        else:
            pass

    # Функция, вызываемая при нажатии клавиш
    def handle_configure(self, _event):

        # Валидация
        self.SelectTimeFrame.validate_entry()

    def exit_or_confirm(self):

        try:
            if settings.get('confirmation', 'dont_ask'):
                self.destroy()

            elif self.timer_on and (self.ConfirmationWindow is None or not self.ConfirmationWindow.winfo_exists()):

                self.ConfirmationWindow = popups.ConfirmationWindow(self)  # Создать окно, если его нет или уничтожено
                self.after(20, self.ConfirmationWindow.focus)

            elif self.timer_on:
                self.ConfirmationWindow.focus()  # Если окно есть, переключиться на него

            else:
                self.destroy()

        except configparser.NoOptionError as error:
            print(error)
            settings.set('confirmation', 'dont_ask', 'false')
            self.exit_or_confirm()

    def open_settings(self):
        if self.SettingsWindow is None or not self.SettingsWindow.winfo_exists():
            self.SettingsWindow = settings.SettingsWindow(self)  # create window if its None or destroyed
            self.after(10, self.SettingsWindow.focus)

            self.logger.info('The settings window was opened.')

        else:
            self.SettingsWindow.focus()  # if window exists focus it

            self.logger.info('The settings window was focused.')


# Главные цикл
app = App()
app.mainloop()
