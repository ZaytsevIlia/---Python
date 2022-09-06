import argparse
import time
from socket import socket, AF_INET, SOCK_STREAM
import os
import sys
import threading

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
import json
from common.utils import send_message, get_message
from common.variables import ACTION, PRESENCE, TIME, USER, ACCOUNT_NAME, DEFAULT_PORT, DEFAULT_IP_ADDRESS, \
    RESPONSE, ERROR, SENDER, MESSAGE, MESSAGE_TEXT, DESTINATION, EXIT
import logging
import logs.client_log_config
from decorate import log

logger = logging.getLogger('client')


@log
def create_presence(account_name):
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
    parser.add_argument('-n', '--name', default=None, nargs='?')
    namespace = parser.parse_args(sys.argv[1:])
    server_addr = namespace.addr
    server_port = namespace.port
    client_name = namespace.name

    if not 1023 < server_port < 65536:
        logger.error(f'У клиента неверный порт: {server_port}. \n'
                     f'Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    return server_addr, server_port, client_name


@log
def message_from_server(sock, username):
    while True:
        try:
            message = get_message(sock)
            if ACTION in message and message[ACTION] == MESSAGE and SENDER in message and MESSAGE_TEXT in message\
                    and DESTINATION in message and message[DESTINATION] == username:
                print(f'Получено сообщение: \n {message[SENDER]}: {message[MESSAGE_TEXT]}')
                logger.info(f'Получено сообщение. Пользователь: {message[SENDER]}. '
                            f'Сообщение: {message[MESSAGE_TEXT]}')
            else:
                logger.error(f'Получено некорректное сообщение от сервера: {message}')
        except (OSError, ConnectionError, ConnectionAbortedError, ConnectionResetError,
                json.JSONDecodeError):
            logger.error(f'Потеряно соединение с сервером.')
            break


@log
def create_message(sock, account_name='Guest'):
    to_user = input('Введите получателя сообщения: ')
    message = input('Введите сообщение для отправки: ')
    message_dict = {
        ACTION: MESSAGE,
        SENDER: account_name,
        DESTINATION: to_user,
        TIME: time.time(),
        MESSAGE_TEXT: message,
    }
    logger.debug(f'Сформирован словарь сообщения: {message_dict}')
    try:
        send_message(sock, message_dict)
        logger.debug(f'Пользователю {to_user} отправлено сообщение')
    except Exception as err:
        print(err)
        logger.error('Потеряно соединение с сервером')
        sys.exit(1)


@log
def create_exit_message(account_name):
    return {
        ACTION: EXIT,
        TIME: time.time(),
        ACCOUNT_NAME: account_name,
    }


def print_help():
    print('Поддерживаемые команды:')
    print('message - отправить сообщение. Кому и текст будет запрошены отдельно.')
    print('help - вывести подсказки по командам')
    print('exit - выход из программы')

@log
def user_interactive(sock, username):
    print_help()
    while True:
        command = input('Введите команду: ')
        if command == 'message':
            create_message(sock, username)
        elif command == 'help':
            print_help()
        elif command == 'exit':
            send_message(sock, create_exit_message(username))
            print('Завершение соединения')
            logger.info('Работа завершена по команде пользователя.')
            time.sleep(0.5)
            break
        else:
            print('Неизвестная команда. Попробуйте снова или введите \'help\'.')


@log
def main():
    server_addr, server_port, client_name = arg_parser()

    if not client_name:
        client_name = input('Введите имя пользователя: ')

    print(f'Консольный месседжер запущен. Имя пользователя: {client_name}')

    try:
        transport = socket(AF_INET, SOCK_STREAM)
        transport.connect((server_addr, server_port))
        send_message(transport, create_presence(client_name))
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
        receiver = threading.Thread(target=message_from_server, args=(transport, client_name))
        receiver.daemon = True
        receiver.start()

        user_interface = threading.Thread(target=user_interactive, args=(transport, client_name))
        user_interface.daemon = True
        user_interface.start()
        logger.info('Запущены потоки')

        while True:
            time.sleep(1)
            if receiver.is_alive() and user_interface.is_alive():
                continue
            break


if __name__ == '__main__':
    main()
