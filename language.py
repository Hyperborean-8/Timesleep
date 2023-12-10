import customtkinter as ctk
import settings
import os
from configparser import ConfigParser
import configparser
from icecream import ic

def get_all_languages():
    return [f for f in os.listdir('languages') if f.endswith('.ini')]

def restore_english():
    parser = ConfigParser()

    default_config = {
        'METADATA': {
          'language_name': 'English'
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

        restore_english()
        self.languages = get_all_languages()

        ic(self.languages)

        self.get_all_names()

    def get_all_names(self) -> list:
        names = []
        for configfile in self.languages:
            ic(configfile)
            try:
                parser = ConfigParser()
                parser.read('languages/' + configfile)
                names.append(parser.get('METADATA', 'language_name'))
                ic()
            except configparser.NoSectionError as error:
                ic(error)
                names.append(configfile)
            except configparser.NoOptionError as error:
                ic(error)
                names.append(configfile)

        return names


        ic(names)





