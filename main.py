import customtkinter as ctk
import copy as copy
import math as math
from PIL import Image
from icecream import ic
import os

ctk.set_appearance_mode("dark")  # Режимы: системный (стандартный), светлый, тёмный
ctk.set_default_color_theme("blue")  # Темы: синяя (стандартная), тёмно-синяя, зелёная
ctk.deactivate_automatic_dpi_awareness()
debug = True
# ic.disable()

def hide_window():
    app.withdraw()


def show_window():
    app.deiconify()


def turn_off_computer():

    if not debug:
        os.system("shutdown /s /t 1")

# Коробка с выбором времени
class SelectTimeFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        # --- Слайдер и надписи ---
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

        # --- Выбор времени ---
        self.TimeFrame = ctk.CTkFrame(self)
        self.TimeFrame.grid(row=0, column=1, sticky="news")

        self.TimeInnerFrame = ctk.CTkFrame(self.TimeFrame)
        self.TimeInnerFrame.grid(row=1, column=1, sticky="news")

        self.TimeFrame.grid_rowconfigure(0, weight=1)
        self.TimeFrame.grid_rowconfigure(1, weight=0)
        self.TimeFrame.grid_rowconfigure(2, weight=1)
        self.TimeFrame.grid_columnconfigure(0, weight=1)
        self.TimeFrame.grid_columnconfigure(1, weight=0)
        self.TimeFrame.grid_columnconfigure(2, weight=1)

        self.font = ctk.CTkFont(size=80)
        self.time_entry = ctk.CTkEntry(self.TimeInnerFrame, font=self.font, width=105, height=80, border_width=0,
                                       corner_radius=0, fg_color='#101010')
        self.current_input = ''
        self.time_entry.grid(row=0, column=0)
        self.time_type = ctk.CTkSegmentedButton(self.TimeInnerFrame, values=['Минут', 'Часов'],
                                                command=self.change_by_entry)
        self.time_type.grid(row=1, column=0)
        self.time_type.set('Минут')

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

    def change_by_slider(self, x):
        time_options = copy.deepcopy(self.time_options)
        time_options.reverse()

        seconds = time_options[int(x)][1]

        print('[01] Слайдер выбран:', time_options[int(x)][0], 'или', seconds, 'секунд')

        # Установка entry на значение слайдера
        for y in range(len(self.time_type.get()), -1, -1):
            self.time_entry.delete(y)

        if seconds <= 5940:

            self.time_type.set('Минут')
            self.time_entry.insert(string=str(math.ceil(seconds / 60)), index=0)

        elif seconds > 5940:

            self.time_type.set('Часов')
            self.time_entry.insert(string=str(math.ceil(seconds / 3600)), index=0)

        self.master.set_timer(seconds)

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

        self.master.set_timer(seconds)


class CurrentTimeFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

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

        def tr(text):
            text = str(text)
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
            label_text = 'Something went wrong'

        self.time_label.configure(text=label_text)


class ButtonsFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "icons")
        ic(image_path)
        self.icon_settings_light = ctk.CTkImage(Image.open(os.path.join(image_path, "icon-settings-light.png")), size=(20, 20))
        self.icon_minimize_light = ctk.CTkImage(Image.open(os.path.join(image_path, "icon-minimize-light.png")),
                                                size=(20, 20))



        # Кнопки
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        self.start_button = ctk.CTkButton(self, text="Старт", state=ctk.DISABLED, command=master.start_timer)
        self.start_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.stop_button = ctk.CTkButton(self, text='Стоп', command=master.stop_timer)
        self.stop_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')
        self.stop_button.grid_remove()

        self.ExtraButtonFrame = ctk.CTkFrame(self, height=30, width=150)
        self.ExtraButtonFrame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)

        self.ExtraButtonFrame.columnconfigure(0, weight=0)
        self.ExtraButtonFrame.columnconfigure(1, weight=1)

        self.settings_button = ctk.CTkButton(self.ExtraButtonFrame, text='', image=self.icon_settings_light, width=20, height=20)
        self.settings_button.grid(row=0, column=0)
        self.minimize = ctk.CTkButton(self.ExtraButtonFrame, text='', image=self.icon_minimize_light, width=20, height=20)
        self.minimize.grid(row=0, column=2)

    def hide_start(self):
        self.start_button.grid_remove()
        self.stop_button.grid()

    def show_start(self):
        self.start_button.grid()
        self.stop_button.grid_remove()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.timer_after = None
        self.minimized_rows: bool = False
        self.options_hidden: bool = False
        self.timer_on: bool = False
        self.extra_second = False
        self.seconds_set: int = 0
        self.seconds: int = 0

        # Прикрепление сигнала изменения к переменной
        self.bind("<Key>", self.handle_configure)

        # Настройка окна
        self.title("Timesleep")
        self.geometry("300x315")
        self.resizable(False, False)

        # Настройка сетки
        self.grid_columnconfigure(0, weight=1)

        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        # Frames
        self.SelectTimeFrame = SelectTimeFrame(self)
        self.SelectTimeFrame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky="news")
        self.CurrentTimeFrame = CurrentTimeFrame(self)
        self.CurrentTimeFrame.grid(row=0, column=0, padx=10, pady=(15, 0), sticky='news')
        self.CurrentTimeFrame.grid_remove()
        self.ButtonsFrame = ButtonsFrame(self)
        self.ButtonsFrame.grid(row=1, column=0, padx=10, pady=5, sticky='news')

        # self.SelectTimeFrame.grid_remove()
        # self.CurrentTimeFrame.grid() # TODO: -----------------------------------------------------------------

        # Это прикол который нам поможет потом))
        # self.attributes('-topmost', True)

    def set_timer(self, seconds):
        print('[03] Время установлено на: ', seconds)

        self.seconds_set = seconds

        if seconds == 0:
            self.ButtonsFrame.start_button.configure(state=ctk.DISABLED)
        else:
            self.ButtonsFrame.start_button.configure(state=ctk.NORMAL)

    def start_timer(self):
        print('[04] Время запущено с', self.seconds_set, 'секундами.')

        self.timer_on = True
        self.extra_second = True

        self.seconds = self.seconds_set

        self.SelectTimeFrame.grid_remove()
        self.CurrentTimeFrame.grid()

        self.ButtonsFrame.hide_start()

        self.update_timer()

    def stop_timer(self):
        self.timer_on = False

        self.SelectTimeFrame.grid()
        self.CurrentTimeFrame.grid_remove()

        self.ButtonsFrame.show_start()

        self.after_cancel(self.timer_after)

    def handle_configure(self, _event):

        self.SelectTimeFrame.validate_entry()

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


app = App()
app.mainloop()
