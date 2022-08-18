import argparse
import time
from socket import socket, AF_INET, SOCK_STREAM
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
import json
from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    RESPONSE, ERROR, SENDER, MESSAGE, MESSAGE_TEXT
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
def arg_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('addr', default=DEFAULT_IP_ADDRESS, nargs='?')
    parser.add_argument('port', default=DEFAULT_PORT, type=int, nargs='?')
    parser.add_argument('-m', default='send', nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port
    client_mode = namespace.m

    if not 1023 < server_port < 65536:
        logger.error(f'У клиента неверный порт: {server_port}. \n'
                     f'Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    if client_mode not in ('listen', 'send'):
        logger.error(f'Неверный режим работы: {client_mode}')
        sys.exit(1)
    return server_addr, server_port, client_mode


@log
def message_from_server(message):
    if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message:
        print(f'Получено сообщение: \n {message[SENDER]}: {message[MESSAGE_TEXT]}')
        logger.info(f'Получено сообщение. Пользователь: {message[SENDER]}. Сообщение: {message[MESSAGE_TEXT]}')
    else:
        logger.error(f'Получено некорректное сообщение от сервера: {message}')


@log
def create_message(sock, account_name='Guest'):
    message = input('Введите сообщение для отправки или \'exit\' для завершения работы: ')
    if message == 'exit':
        sock.close()
        logger.info('Завершение работы по команде пользователя.')
        print('Спасибо за использование нашего сервиса!')
        sys.exit(0)
    message_dict = {
        ACTION: MESSAGE,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
        MESSAGE_TEXT: message
    }
    logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    return message_dict


@log
def main():
    server_addr, server_port, client_mode = arg_parser()

    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_addr, server_port))
        send_message(transport, create_presence())
        answer = procces_server_message(get_message(transport))
        logger.info(f'Соединение установлено, ответ сервера {answer}')
        print('Соединение с сервером установлено')
    except json.JSONDecodeError:
        logger.error('Ошибка декодирования строки')
        sys.exit(1)
    except ConnectionRefusedError:
        logger.error(f'Неудалось подключиться к серверу: {server_addr}:{server_port}')
        sys.exit(1)
    else:
        if client_mode == 'send':
            print('Режим работы: отправка сообщений')
        else:
            print('Режим работы: приём сообщений')
        while True:
            if client_mode == 'send':
                try:
                    send_message(transport, create_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Соединение с сервером {server_addr}:{server_port} потеряно')
                    sys.exit(1)
            if client_mode == 'listen':
                try:
                    message_from_server(get_message(transport))
                except (ConnectionResetError, ConnectionError, ConnectionAbortedError):
                    logger.error(f'Соединение с сервером {server_addr}:{server_port} потеряно')
                    sys.exit(1)


if __name__ == '__main__':
    main()
