import logging
import datetime
import os
import json

from game.display import start_gui
import game.cli


class Config:
    def __init__(self, open_gui_default: bool, enable_logging: bool):
        self.open_gui_default = open_gui_default
        self.enable_logging = enable_logging


PATH_TO_SAVE_LOGS = './logs'
if __name__ == '__main__':
    # Load config
    with open('config.json', 'r') as f:
        config_dict = json.loads(f.read())
        config = Config(**config_dict)

    if config.enable_logging:
        if not os.path.exists(PATH_TO_SAVE_LOGS):
            os.makedirs(PATH_TO_SAVE_LOGS)
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%d %b %Y %H:%M:%S',
                            filename=f'logs/{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}.log', filemode='w')

    if config.open_gui_default:
        start_gui()
        exit(1)

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
