import customtkinter as ctk
import settings
import os
from configparser import ConfigParser
import configparser
from icecream import ic
import logging


class Language:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Переменная с названиями файлов, именами и id файлов с языком
        self.language_files: dict = {}

        # Логгер
        self.logger = logging.getLogger(__name__)

        # Стандартный английский
        # Все переменные генерируются относительно этого словаря
        self.default_config = {
            'METADATA': {
                'name': 'English',
                'id': 'english'
            },
            'buttons': {
                'start_timer': 'Start',
                'stop_timer': 'Stop'
            },
            'settings': {
                'current_language': 'Current language',
                'confirmation': 'Do not ask for exit confirmation when the timer is on',
                'title': 'Settings'
            },
            'popups': {
                'confirmation_label': 'Are you sure you want to exit? The timer is still running.',
                'confirmation_setting': "Don't ask again"
            }
        }

        # Переменная хранящая все StringVar
        self.vars = {}

        # Копирование self.default_config и превращение всех переменных в StringVar
        for key, value in self.default_config.items():
            # Пропускает строки из METADATA
            if key == 'METADATA':
                continue
            if isinstance(value, dict):
                self.vars[key] = {k: ctk.StringVar(value=v) for k, v in value.items()}
            else:
                self.vars[key] = value

        # Восстановление файла с английским языком
        self.restore_english()

        # Модуль сканирует папку language/ на наличие ini файлов
        self.scan()

        # Модуль спрашивает у Настроек текущий язык
        try:
            self.current_language = settings.get('language', 'current')
        except configparser.NoSectionError as error:
            self.current_language = 'English'
        except configparser.NoOptionError as error:
            self.current_language = 'English'

        # Поменять язык на текущий
        self.change_language(self.current_language)

        self.logger.info('The Language module is fully initialized.')

    # Функция, которая восстанавливает английский язык, если он отсутствует или повреждён (но не изменён)
    def restore_english(self):
        parser = ConfigParser()

        parser.read_dict(self.default_config)
        parser.read('languages/english.ini')

        with open('languages/english.ini', 'w') as configfile:
            parser.write(configfile)

    # Возвращает значение секции из всех языков, которые доступны
    def get_all(self, section, option) -> list:
        strings = []
        for configfile in self.language_files:
            try:
                parser = ConfigParser()
                parser.read('languages/' + configfile)
                strings.append(parser.get(section, option))
            except configparser.NoSectionError as error:
                self.logger.warning(f'No {section} section was found in {configfile}. {error}')
                pass
            except configparser.NoOptionError as error:
                self.logger.warning(f'No {option} option was found in {configfile}. {error}')
                pass

        return strings

    def change_language(self, new_language):

        self.scan()

        if new_language not in self.get_all('METADATA', 'name'):
            raise self.NoLanguageFileFound(self)

        for key, val in self.language_files.items():
            ic(key, val, new_language)
            if val[0] == new_language:
                parser = ConfigParser()
                parser.read_dict(self.default_config)
                parser.read('languages/' + key, encoding='windows-1251')
                with open('languages/' + key, 'w', encoding='windows-1251') as configfile:
                    parser.write(configfile)

                for section_key, section_val in self.vars.items():
                    for option_key, option_val in section_val.items():
                        ic(section_key, section_val, option_key, option_val)
                        ic(parser.get(section_key, option_key))

                        option_val.set(parser.get(section_key, option_key))

        self.logger.info(f'The language has been changed to {new_language}')

    # Сканирует папку language и записывает названия всех ini файлов, а также их name и id
    def scan(self):
        self.language_files = {f: f for f in os.listdir('languages') if f.endswith('.ini')}

        self.logger.info(f'{len(self.language_files)} languages were found: {self.language_files}')

        parser = ConfigParser()
        for key in self.language_files:

            parser.read('languages/' + key)

            try:
                self.language_files[key] = [parser.get('METADATA', 'Name'), parser.get('METADATA', 'id')]
            except configparser.NoSectionError as error:
                ic(error)
                del self.language_files[key]
            except configparser.NoOptionError as error:
                print(f'Появилась ошибка! {error}')
                del self.language_files[key]

    class NoLanguageFileFound(Exception):
        def __init__(self, language_class, message='Язык не обнаружен!'):
            super().__init__(message)

            self.message = message
            language_class.current_language = 'English'
