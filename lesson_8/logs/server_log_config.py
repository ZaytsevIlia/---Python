import logging
import os
import logging.handlers

server_log = logging.getLogger('server')

formatter = logging.Formatter('%(asctime)s - %(levelname)-8s - %(module)s - %(message)s')

PATH = os.path.dirname(__file__)
PATH = os.path.join(PATH, 'server.log')
time_rotation_handler = logging.handlers.TimedRotatingFileHandler(PATH, when='D', interval=1, encoding='utf-8')
time_rotation_handler.setFormatter(formatter)
time_rotation_handler.setLevel(logging.DEBUG)

server_log.addHandler(time_rotation_handler)
server_log.setLevel(logging.DEBUG)

if __name__ == '__main__':
    server_log.debug('Дебаг')
    server_log.info('Инфо')
    server_log.warning('Внимание!')
    server_log.error('Ошибка')
    server_log.critical('Критическая ошибка')
