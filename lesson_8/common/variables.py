DEFAULT_PORT = 7777
ENCODING = 'utf-8'
MAX_PACKAGE_LENGTH = 1024
DEFAULT_IP_ADDRESS = '127.0.0.1'
MAX_CONNECTIONS = 5

ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'sender'
DESTINATION = 'to'

PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
EXIT = 'exit'

RESPONSE_200 = {RESPONSE: 200}
RESPONSE_400 = {
    RESPONSE: 400,
    ERROR: None,
}
