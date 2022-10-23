import logging
import datetime
import os
import json

from game.display import start_gui
import game.cli

PATH_TO_LOGS = './logs'
PATH_TO_CONFIG = './config.json'


def create_config_file():
    if os.path.isfile(PATH_TO_CONFIG):
        return

    with open(PATH_TO_CONFIG, 'w') as config_file:
        default_config = Config()
        config_file.write(default_config.to_json())
        config_file.close()


class Config:
    def __init__(self, open_gui_default: bool = False, enable_logging: bool = True):
        self.open_gui_default = open_gui_default
        self.enable_logging = enable_logging

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


if __name__ == '__main__':
    # Load config
    create_config_file()
    with open(PATH_TO_CONFIG, 'r') as file:
        config_dict = json.loads(file.read())
        config = Config(**config_dict)

    if config.enable_logging:
        if not os.path.exists(PATH_TO_LOGS):
            os.makedirs(PATH_TO_LOGS)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%d %b %Y %H:%M:%S',
                            filename=f'logs/{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}.log', filemode='w')

    if config.open_gui_default:
        start_gui()
        exit(0)

    print('? Какую версию запустить?')
    print('[графическая — 0 (default); консольная — 1]')
    print('Ввод:', end=' ')
    interface = input()
    if interface == '0' or interface == '':
        print('i Запуск графической версии...', end='\n\n')
        start_gui()
    elif interface == '1':
        print('i Запуск консольной версии...', end='\n\n')
        game.cli.start_cli()
    else:
        raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')
