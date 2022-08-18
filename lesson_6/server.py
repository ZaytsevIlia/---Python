from socket import socket, AF_INET, SOCK_STREAM, SOL_SOCKET, SO_REUSEADDR
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.utils import send_message, get_message
from common.variables import DEFAULT_PORT, DEFAULT_IP_ADDRESS, MAX_CONNECTIONS, ACTION, \
    TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR
import json
import logging
import logs.server_log_config
from decorate import log

logger = logging.getLogger('server')


@log
def process_client_message(message):
    logger.debug('Запущена функция разбора клиентского сообщения.')
    if ACTION in message and message[ACTION] == PRESENCE and TIME in message and \
            USER in message and message[USER][ACCOUNT_NAME] == 'Guest':
        logger.info('Сообщение клиента корректное.')
        return {RESPONSE: 200}
    logger.warning('Сообщение клиента некорректно.')
    return {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }


@log
def main():
    try:
        if '-p' in sys.argv:
            listen_port = int(sys.argv[sys.argv.index('-p') + 1])
            logger.debug('Получен порт от пользователя.')
        else:
            listen_port = DEFAULT_PORT
            logger.debug('Пользователь не ввёл порт. Порт установлен по дефолту.')
        if listen_port < 1024 or listen_port > 65535:
            logger.error('Пользователь ввёл некорректный порт.')
            raise ValueError
    except IndexError:
        logger.error('Пользователь ввёл некорректный порт.')
        print('После параметра -\'p\' укажите номер порта от 1024 до 65535')
        sys.exit(1)
    except ValueError:
        logger.error('Пользователь ввёл некорректный порт.')
        print('Номер порта должен быть от 1024 до 65535')
        sys.exit(1)

    try:
        if '-a' in sys.argv:
            listen_addres = sys.argv[sys.argv.index('-a') + 1]
            logger.debug('Получен адрес от пользователя.')
        else:
            listen_addres = DEFAULT_IP_ADDRESS
            logger.debug('Пользователь не ввёл адрес. Адрес установлен по дефолту.')

    except IndexError:
        logger.error('Пользователь ввёл некорректный адрес.')
        print('После параметра -\'a\' надо указать ip адрес')
        sys.exit(1)

    SERV_SOCK = socket(AF_INET, SOCK_STREAM)
    logger.debug('Создан сокет сервера')
    SERV_SOCK.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    SERV_SOCK.bind((listen_addres, listen_port))
    SERV_SOCK.listen(MAX_CONNECTIONS)

    while True:
        CLIENT_SOCK, CLIENT_ADDR = SERV_SOCK.accept()
        try:
            message_from_client = get_message(CLIENT_SOCK)
            logger.debug('Получено сообщение от клиента')
            print(message_from_client)
            responce = process_client_message(message_from_client)
            send_message(CLIENT_SOCK, responce)
            logger.info('Направлен ответ клиенту')
            CLIENT_SOCK.close()
        except (ValueError, json.JSONDecodeError):
            logger.error('От клиента получено некорректное сообщение')
            print('Некорректное сообщение от клиента')
            CLIENT_SOCK.close()


if __name__ == '__main__':
    main()
