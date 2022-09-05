import logging
import datetime
from display import start_gui
from go import start_cli

if __name__ == '__main__':
    # logging.basicConfig(filename=f'{datetime.datetime.now().strftime("%Y%m%d %H%M%S")}.log', level=logging.DEBUG)
    logging.basicConfig(level=logging.DEBUG)

    print('gui/cli (gui):', end='')
    interface = input()
    if interface == 'gui' or interface == '':
        start_gui()
    elif interface == 'cli':
        start_cli()
    else:
        print('Неизвестная команда, запускаю gui')
        start_gui()

