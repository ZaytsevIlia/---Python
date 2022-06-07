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

client_log = logging.getLogger('client.log')


def create_presence(account_name='Guest'):
    client_log.debug('Старт функции создания сообщения.')
    out_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    client_log.debug('Сообщение создано.')
    return out_message


def procces_server_message(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            client_log.info('Получен положительный ответ от сервера')
            return 'Всё ОК'
        client_log.warning('Получен отрицательный ответ от сервера')
        return f'Код 400 - {message[ERROR]}'
    client_log.error('Некорректный ответ сервера')
    raise ValueError


def main():
    try:
        server_addres = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 and server_port > 65535:
            client_log.error('Пользователь указал неверный порт')
            raise ValueError
    except IndexError:
        client_log.error('Пользователь не указал порт и адрес')
        server_addres = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
        client_log.debug('Порт и адрес установлены по дефолту')
    except ValueError:
        client_log.error('Пользователь указал неверный порт')
        print('Номер порта должен быть от 1024 до 65535')
        client_log.info('Пользователю направлено информационное сообщение')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    client_log.debug('Создан сокет клиента')
    CLIENT_SOCK.connect((server_addres, server_port))
    message_to_server = create_presence()
    send_message(CLIENT_SOCK, message_to_server)
    client_log.info('Направлено сообщение на сервер')
    try:
        answer = procces_server_message(get_message(CLIENT_SOCK))
        print(answer)
        client_log.info('Получен ответ от сервера')
    except (ValueError, json.JSONDecodeError):
        client_log.error('Не удалось декодировать сообщение сервера')
        print('Не удалось декодировать сообщение сервера')


if __name__ == '__main__':
    main()
