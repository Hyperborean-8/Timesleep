import os
from configparser import ConfigParser
from icecream import ic
import customtkinter as ctk


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

        self.checkbox = ctk.CTkCheckBox(self.MainFrame,
                                        text='Не спрашивать подтверждение выхода при запущенном таймере',
                                        checkbox_width=16, checkbox_height=16, command=self.confirm_settings,
                                        variable=self.var)
        self.checkbox.text_label.configure(wraplength=350)
        self.checkbox.grid(row=0, column=0, padx=10, pady=10)

    # Функция, изменяющая настройку подтверждения при таймере
    def confirm_settings(self):
        set('confirmation', 'dont_ask', str(bool(self.checkbox.get())))

    # Функция, переключающая чекбокс в окне Подтверждения
    def change_other_checkbox(self, *_args):
        ic(self.master.ConfirmationWindow)
        if self.master.ConfirmationWindow is not None and self.master.ConfirmationWindow.winfo_exists():
            ic(self.master.ConfirmationWindow.var.set)
            self.master.ConfirmationWindow.var.set(self.var.get())


# Проверка на наличие конфига с настройками
def check_config():
    if os.path.exists('settings.ini'):
        print('[06] Конфиг найден!')
    else:
        print('[06] Конфиг не найден!')
        print('[06] Создаётся стандартный конфиг...')

        parser = ConfigParser()

        parser.add_section('confirmation')
        parser.set('confirmation', 'dont_ask', 'False')

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
    get('confirmation', 'dont_ask')
