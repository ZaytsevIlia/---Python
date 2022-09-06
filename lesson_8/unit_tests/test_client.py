import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR
from client import create_presence, procces_server_message


class TestClient(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_create_presence(self):
        msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        test_msg = create_presence()
        test_msg[TIME] = 1.1
        self.assertEqual(msg, test_msg, 'Неверное создание сообщения')

    def test_procces_server_message_ok(self):
        test_msg_ok = {RESPONSE: 200}
        self.assertEqual('Всё ОК', procces_server_message(test_msg_ok), 'Неверный приём сообщения от сервера')

    def test_procces_server_message_error(self):
        msg_error = {
            RESPONSE: 400,
            ERROR: 'Bad Request'
        }
        test_msg_error = f'Код 400 - {msg_error[ERROR]}'
        self.assertEqual(test_msg_error, procces_server_message(msg_error), 'Неверный приём сообщения от сервера')

    def test_procces_server_message_value_error(self):
        test_msg_value_error = {}
        self.assertRaises(ValueError, procces_server_message, test_msg_value_error)


if __name__ == '__main__':
    unittest.main()
