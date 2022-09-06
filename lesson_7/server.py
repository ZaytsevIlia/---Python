import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER
import json
import logging
import logs.server_log_config
from decorate import log
import argparse
import select

logger = logging.getLogger('server')


@log
def process_client_message(message, message_list, client):
    logger.debug('Запущена функция разбора клиентского сообщения.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        logger.info('Сообщение клиента корректное.')
        send_message(client, {RESPONSE: 200})
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message:
        message_list.append((message[ACCOUNT_NAME], message[MESSAGE_TEXT]))
        return
    else:
        logger.warning('Сообщение клиента некорректно.')
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-a', default='', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    listen_addr = namespace.a
    listen_port = namespace.p

    if not 1023 < listen_port < 65536:
        logger.error(f'Некорректный порт: {listen_port}. \n'
                     f'Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    return listen_addr, listen_port


@log
def main():
    listen_addr, listen_port = arg_parser()

    logger.info(f'Сервер запущен.\nАдрес, с которого принимаются подключения {listen_addr}\n'
                f'Порт для подключения {listen_port} ')

    transport = socket(AF_INET, SOCK_STREAM)
    transport.bind((listen_addr, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []

    transport.listen(MAX_CONNECTIONS)

    while True:
        try:
            client, client_addr = transport.accept()
        except OSError as err:
            print(err.errno)
            pass
        else:
            logger.info(f'Установлено соединение с пользователем {client_addr}')
            clients.append(client)

        recv_data_list = []
        send_data_list = []
        err_list = []

        try:
            if clients:
                recv_data_list, send_data_list, err_list = select.select(clients, clients, [], 0)
        except OSError:
            pass

        if recv_data_list:
            for client_with_message in recv_data_list:
                try:
                    process_client_message(get_message(client_with_message), messages, client_with_message)
                except:
                    logger.info(f'Пользователь {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        if messages and send_data_list:
            message = {
                ACTION: MESSAGE,
                SENDER: messages[0][0],
                TIME: time.time(),
                MESSAGE_TEXT: messages[0][1],
            }
            del messages[0]
            for waiting_client in send_data_list:
                try:
                    send_message(waiting_client, message)
                except:
                    logger.info(f'Пользователь {waiting_client.getpeername()} отключился от сервера.')
                    waiting_client.close()
                    clients.remove(waiting_client)


if __name__ == '__main__':
    main()
