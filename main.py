import logging
import datetime
from game.display import start_gui
from game.go import start_cli

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%d %b %Y %H:%M:%S',
                        filename=f'logs/{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}.log', filemode='w')

    print('gui/cli (gui):', end='')
    interface = input()
    if interface == 'gui' or interface == '':
        start_gui()
    elif interface == 'cli':
        start_cli()
    else:
        print('Неизвестная команда, запускаю gui')
        start_gui()

