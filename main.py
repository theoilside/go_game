import logging
import datetime
import os

from game.display import start_gui
from game.cli import start_cli

PATH_TO_SAVE_LOGS = './logs'
if __name__ == '__main__':
    if not os.path.exists(PATH_TO_SAVE_LOGS):
        os.makedirs(PATH_TO_SAVE_LOGS)
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename=f'logs/{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}.log', filemode='w')
    print('Какую версию запустить?')
    print('[графическая — 0 (default); консольная — 1]')
    print('Ввод:', end=' ')
    interface = input()
    if interface == '0' or interface == '':
        print('...Запуск графической версии...', end='\n\n')
        start_gui()
    elif interface == '1':
        print('...Запуск консольной версии...', end='\n\n')
        start_cli()
    else:
        raise NameError(f'Неверный ввод. Получено: {interface}. Допустимо: 0, 1')

