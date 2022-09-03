import time
from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR, MESSAGE, MESSAGE_TEXT, SENDER, DESTINATION, EXIT, \
    RESPONSE_200, RESPONSE_400
import json
import logging
import logs.server_log_config
from decorate import log
import argparse
import select

logger = logging.getLogger('server')


@log
def process_client_message(message, message_list, client, clients, names):
    logger.debug('Запущена функция разбора клиентского сообщения.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message:
        if message[USER][ACCOUNT_NAME] not in names.keys():
            names[message[USER][ACCOUNT_NAME]] = client
            send_message(client, RESPONSE_200)
        else:
            response = RESPONSE_400
            response[ERROR] = 'Имя пользователя уже используется.'
            send_message(client, response)
            clients.remove(client)
            client.close()
        return
    elif ACTION in message and message[ACTION] == MESSAGE and TIME in message and MESSAGE_TEXT in message \
            and DESTINATION in message and SENDER in message:
        message_list.append(message)
        return
    elif ACTION in message and message[ACTION] == EXIT and ACCOUNT_NAME in message:
        clients.remove(names[message[ACCOUNT_NAME]])
        names[message[ACCOUNT_NAME]].close()
        del names[message[ACCOUNT_NAME]]
        return
    else:
        send_message(client, {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        })
        return


@log
def process_message(message, names, listen_socks):
    """ Отправка определённому клиенту (DESTINATION = 'to') """
    if message[DESTINATION] in names and names[message[DESTINATION]] in listen_socks:
        send_message(names[message[DESTINATION]], message)
        logger.info(f'Отправлено сообщение пользователю {message[DESTINATION]} от пользователя {message[SENDER]}')
    elif message[DESTINATION] in names and names[message[DESTINATION]] not in listen_socks:
        raise ConnectionError
    else:
        logger.error(f'Пользователь {message[DESTINATION]} не зарегистрирован на сервере')


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
    transport.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    transport.bind((listen_addr, listen_port))
    transport.settimeout(0.5)

    clients = []
    messages = []
    names = dict()  # {client_name: client_socket}

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
                    process_client_message(get_message(client_with_message), messages,
                                           client_with_message, clients, names)
                except:
                    logger.info(f'Пользователь {client_with_message.getpeername()} отключился от сервера.')
                    clients.remove(client_with_message)

        for i in messages:
            try:
                process_message(i, names, send_data_list)
            except Exception:
                logger.error(f'Связь с клиентом {i[DESTINATION]} была потеряна.')
                clients.remove(names[i[DESTINATION]])
                del names[i[DESTINATION]]
        messages.clear()


if __name__ == '__main__':
    main()
