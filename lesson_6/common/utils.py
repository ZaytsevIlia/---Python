import sys
import json
from common.variables import MAX_PACKAGE_LENGTH, ENCODING
from decorate import log


@log
def get_message(client):
    """Функция получения и разбора сообщения"""

    encoded_response = client.recv(MAX_PACKAGE_LENGTH)
    if isinstance(encoded_response, bytes):
        json_response = encoded_response.decode(ENCODING)
        if isinstance(json_response, str):
            response = json.loads(json_response)
            if isinstance(response, dict):
                return response
            raise TypeError
        raise TypeError
    raise TypeError


@log
def send_message(sock, message):
    """Функция отправки сообщения"""

    if not isinstance(message, dict):
        raise TypeError
    json_message = json.dumps(message)
    encoded_message = json_message.encode(ENCODING)
    sock.send(encoded_message)
