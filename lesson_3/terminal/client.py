"""
Реализовать простое клиент-серверное взаимодействие по протоколу JIM (JSON instant messaging):
клиент отправляет запрос серверу;
сервер отвечает соответствующим кодом результата.
Клиент и сервер должны быть реализованы в виде отдельных скриптов, содержащих соответствующие функции.

Функции клиента:
сформировать presence-сообщение;
отправить сообщение серверу;
получить ответ сервера;
разобрать сообщение сервера;
параметры командной строки скрипта
client.py <addr> [<port>]: addr — ip-адрес сервера; port — tcp-порт на сервере, по умолчанию 7777.
"""
import time
from socket import socket, AF_INET, SOCK_STREAM
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    RESPONSE, ERROR
import sys
import json
from common.utils import send_message, get_message


def create_presence(account_name='Guest'):
    out_message = {
        ACTION: PRESENCE,
        TIME: time.time(),
        USER: {
            ACCOUNT_NAME: account_name
        }
    }
    return out_message


def procces_server_message(message):
    if RESPONSE in message:
        if message[RESPONSE] == 200:
            return 'Всё ОК'
        return f'Код 400 - {message[ERROR]}'
    raise ValueError


def main():
    try:
        server_addres = sys.argv[1]
        server_port = int(sys.argv[2])
        if server_port < 1024 and server_port > 65535:
            raise ValueError
    except IndexError:
        server_addres = DEFAULT_IP_ADDRESS
        server_port = DEFAULT_PORT
    except ValueError:
        print('Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    CLIENT_SOCK = socket(AF_INET, SOCK_STREAM)
    CLIENT_SOCK.connect((server_addres, server_port))
    message_to_server = create_presence()
    send_message(CLIENT_SOCK, message_to_server)
    try:
        answer = procces_server_message(get_message(CLIENT_SOCK))
        print(answer)
    except (ValueError, json.JSONDecodeError):
        print('Не удалось декодировать сообщение сервера')


if __name__ == '__main__':
    main()
