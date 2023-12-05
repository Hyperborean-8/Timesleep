import customtkinter as ctk


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
    def change_other_checkbox(self, *_args):
        if self.master.SettingsWindow is not None and self.master.SettingsWindow.winfo_exists():
            self.master.SettingsWindow.var.set(self.var.get())
