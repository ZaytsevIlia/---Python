import time
from socket import socket, AF_INET, SOCK_STREAM
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
import json
from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    RESPONSE, ERROR
import logging
import logs.client_log_config
from decorate import log

logger = logging.getLogger('client')


@log
def create_presence(account_name='Guest'):
    logger.debug('Старт функции создания сообщения.')
    out_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    logger.debug('Сообщение создано.')
    return out_message


@log
def procces_server_message(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            logger.info('Получен положительный ответ от сервера')
            return 'Всё ОК'
        logger.warning('Получен отрицательный ответ от сервера')
        return f'Код 400 - {message[ERROR]}'
    logger.error('Некорректный ответ сервера')
    raise ValueError


@log
def main():
    try:
        server_addres = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 and server_port > 65535:
            logger.error('Пользователь указал неверный порт')
            raise ValueError
    except IndexError:
        logger.error('Пользователь не указал порт и адрес')
        server_addres = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        logger.debug('Порт и адрес установлены по дефолту')
    except ValueError:
        logger.error('Пользователь указал неверный порт')
        print('Номер порта должен быть от 1024 до 65535')
        logger.info('Пользователю направлено информационное сообщение')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    logger.debug('Создан сокет клиента')
    CLIENT_SOCK.connect((server_addres, server_port))
    message_to_server = create_presence()
    send_message(CLIENT_SOCK, message_to_server)
    logger.info('Направлено сообщение на сервер')
    try:
        answer = procces_server_message(get_message(CLIENT_SOCK))
        print(answer)
        logger.info('Получен ответ от сервера')
    except (ValueError, json.JSONDecodeError):
        logger.error('Не удалось декодировать сообщение сервера')
        print('Не удалось декодировать сообщение сервера')


if __name__ == '__main__':
    main()
