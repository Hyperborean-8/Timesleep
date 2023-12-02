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

        config = ConfigParser()

        config.add_section('confirmation')
        config.set('confirmation', 'confirm_when_timer_on', 'True')

        with open('settings.ini', 'w') as configfile:
            config.write(configfile)


# Функция, которая возвращает значения переменной
def get(section, option):
    config = ConfigParser()
    config.read('settings.ini')
    state = config.get(section, option)

    # Если значение bool, то перевести из str в bool и вернуть bool
    if state.lower() in ['false', 'true']:
        state = state.lower() == 'true'
        ic(state)
        return state


# Точка входа
if __name__ == '__main__':
    get('confirmation', 'confirm_when_timer_on')
