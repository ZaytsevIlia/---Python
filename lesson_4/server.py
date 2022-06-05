"""
Функции сервера:
принимает сообщение клиента;
формирует ответ клиенту;
отправляет ответ клиенту;
имеет параметры командной строки:
-p <port> — TCP-порт для работы (по умолчанию использует 7777);
-a <addr> — IP-адрес для прослушивания (по умолчанию слушает все доступные адреса).
"""

from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import os
import sys
sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR
import json


def process_client_message(message):
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        return {RESPONSE: 200}
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
        else:
            listen_port = DEFAULT_PORT
        if listen_port < 1024 or listen_port > 65535:
            raise ValueError
    except IndexError:
        print('После параметра -\'p\' укажите номер порта от 1024 до 65535')
        sys.exit(1)
    except ValueError:
        print('Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_addres = sys.argv[sys.argv.index('-a') + 1]
        else:
            listen_addres = DEFAULT_IP_ADDRESS

    except IndexError:
        print('После параметра -\'a\' надо указать ip адрес')
        sys.exit(1)

    SERV_SOCK = socket(AF_INET, SOCK_STREAM)
    SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SERV_SOCK.bind((listen_addres, listen_port))
    SERV_SOCK.listen(MAX_CONNECTIONS)

    while True:
        CLIENT_SOCK, CLIENT_ADDR = SERV_SOCK.accept()
        try:
            message_from_client = get_message(CLIENT_SOCK)
            print(message_from_client)
            responce = process_client_message(message_from_client)
            send_message(CLIENT_SOCK, responce)
            CLIENT_SOCK.close()
        except (ValueError, json.JSONDecodeError):
            print('Некорректное сообщение от клиента')
            CLIENT_SOCK.close()


if __name__ == '__main__':
    main()
