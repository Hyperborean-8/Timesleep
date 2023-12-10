import os
from configparser import ConfigParser
import configparser
import language
from icecream import ic
import customtkinter as ctk


# Окно с настройками
class SettingsWindow(ctk.CTkToplevel):

    def __init__(self, StringVars, *args, **kwargs):
        super().__init__(*args, **kwargs)
        ic()
        print('НАСТРОЙКИ РАБОТАЮТ!!')
        self.StringVars = StringVars

        self.title("Настройки")
        self.geometry("400x300")
        self.resizable(False, False)

        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # -- Главный фрейм, хранящий всё
        self.MainFrame = ctk.CTkFrame(self)
        self.MainFrame.grid(row=0, column=0, pady=10, padx=10, sticky='news')
        self.MainFrame.columnconfigure(0, weight=1)

        # --- Выбор языка ---
        self.LanguageFrame = ctk.CTkFrame(self.MainFrame)
        self.LanguageFrame.grid(row=0, column=0, sticky='news')
        self.LanguageFrame.columnconfigure(1, weight=1)

        self.language_label = ctk.CTkLabel(self.LanguageFrame, text='Язык')
        self.language_label.grid(row=0, column=0, sticky='w')
        self.language_box = ctk.CTkOptionMenu(self.LanguageFrame, values=self.StringVars.get_all_names())
        self.language_box.grid(row=0, column=2, sticky='e')

        # --- Чекбокс подтверждения ---
        # Переменная чекбокса
        self.var = ctk.BooleanVar()
        # Привязка сигнала изменения к функции
        self.var.trace('w', self.change_other_checkbox)

        try:
            self.var.set(get('confirmation', 'dont_ask'))
        except configparser.NoOptionError as error:
            print(error)
            set('confirmation', 'dont_ask', 'false')
            self.exit_or_confirm()

        self.confirmation = ctk.CTkCheckBox(self.MainFrame,
                                            text='Не спрашивать подтверждение выхода при запущенном таймере',
                                            checkbox_width=16, checkbox_height=16,
                                            command=self.confirm_settings,
                                            variable=self.var)
        self.confirmation.text_label.configure(wraplength=350)
        self.confirmation.grid(row=1, column=0, padx=10, pady=10)

    # Функция, изменяющая настройку подтверждения при таймере
    def confirm_settings(self):
        set('confirmation', 'dont_ask', str(bool(self.confirmation.get())))

    # Функция, переключающая чекбокс в окне Подтверждения
    def change_other_checkbox(self, *_args):
        ic(self.master.ConfirmationWindow)
        if self.master.ConfirmationWindow is not None and self.master.ConfirmationWindow.winfo_exists():
            ic(self.master.ConfirmationWindow.var.set)
            self.master.ConfirmationWindow.var.set(self.var.get())


# Проверка на наличие конфига с настройками
def check_config():
    parser = ConfigParser()

    default_config = {
        'confirmation': {
            'dont_ask': 'False'
        },
        'language': {
            'current': 'english'
        }
    }

    parser.read_dict(default_config)
    parser.read('settings.ini')

    with open('settings.ini', 'w') as configfile:
        parser.write(configfile)


# Функция, которая возвращает значения переменной
def get(section, option):
    parser = ConfigParser()
    parser.read('settings.ini')
    state = parser.get(section, option)

    # Если значение bool, то перевести из str в bool и вернуть bool
    if state.lower() in ['false', 'true']:
        state = state.lower() == 'true'
        ic(state)
        return state


# Функция, которая записывает значение настройки сразу же
def set(section, option, state):
    ic(section, option, state)
    parser = ConfigParser()
    parser.read('settings.ini')
    parser.set(section, option, state)

    with open('settings.ini', 'w') as configfile:
        parser.write(configfile)


# Точка входа (для отладки)
if __name__ == '__main__':
    app = SettingsWindow()
    app.mainloop()
