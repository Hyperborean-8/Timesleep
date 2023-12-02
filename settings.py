import os
from configparser import ConfigParser
from icecream import ic


# Проверка на наличие конфига с настройками
def check_config():
    if os.path.exists('settings.ini'):
        print('[06] Конфиг найден!')
    else:
        print('[06] Конфиг не найден!')
        print('[06] Создаётся стандартный конфиг...')

        parser = ConfigParser()

        parser.add_section('confirmation')
        parser.set('confirmation', 'confirm_when_timer_on', 'True')

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
    get('confirmation', 'confirm_when_timer_on')
