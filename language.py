import customtkinter as ctk
import settings
import os
from configparser import ConfigParser
import configparser
from icecream import ic

def restore_english():
    parser = ConfigParser()

    default_config = {
        'METADATA': {
            'name': 'English',
            'id': 'english'
        },
        'buttons': {
            'start_timer': 'Start',
            'stop_timer': 'Stop'
        }
    }

    parser.read_dict(default_config)

    with open('languages/english.ini', 'w') as configfile:
        parser.write(configfile)


class StringVars:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Восстановление файла с английским языком
        restore_english()

        # Модуль спришвает у Настроек текущий язык
        try:
            self.current_language = settings.get('language', 'current')
        except configparser.NoSectionError as error:
            ic(error)
            self.current_language = 'English'
        except configparser.NoOptionError as error:
            ic(error)
            self.current_language = 'English'

        # Модуль сканирует папку language/ на наличие ini файлов
        self.scan()



    def get_all(self, section, option) -> list:
        names = []
        for configfile in self.language_files:
            ic(configfile)
            try:
                parser = ConfigParser()
                parser.read('languages/' + configfile)
                names.append(parser.get(section, option))
                ic()
            except configparser.NoSectionError as error:
                ic(error)
            except configparser.NoOptionError as error:
                ic(error)

        return names

        ic(names)

    def change_language(self, new_language):
        ic(self, new_language)

    def scan(self):
        self.language_files = [f for f in os.listdir('languages') if f.endswith('.ini')]