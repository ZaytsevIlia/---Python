import logging
import os

client_log = logging.getLogger('client')

PATH = os.path.dirname(__file__)
PATH = os.path.join(PATH, 'client.log')
file_handler = logging.FileHandler(PATH, encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(module)s - %(message)s')

file_handler.setFormatter(formatter)

client_log.addHandler(file_handler)
client_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    client_log.debug('Дебаг')
    client_log.info('Инфо')
    client_log.warning('Внимание!')
    client_log.error('Ошибка')
    client_log.critical('Критическая ошибка')
