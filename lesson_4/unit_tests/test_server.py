import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, PRESENCE, RESPONSE, ERROR
from server import process_client_message


class TestServer(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    msg_to_return_error = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }

    def test_process_client_message_200(self):
        test_msg = {
            ACTION: PRESENCE,
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        msg_to_return = {RESPONSE: 200}
        self.assertEqual(msg_to_return, process_client_message(test_msg), 'Неверная проверка клиентского сообщения')

    def test_procces_client_message_400(self):
        test_msg = {}
        self.assertEqual(self.msg_to_return_error, process_client_message(test_msg),
                         'Неверная проверка клиентского сообщения')

    def test_procces_client_message_no_action(self):
        test_msg = {
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        self.assertEqual(self.msg_to_return_error, process_client_message(test_msg),
                         'Неверная проверка клиентского сообщения')

    def test_procces_client_message_wrong_action(self):
        test_msg = {
            ACTION: 'test',
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        self.assertEqual(self.msg_to_return_error, process_client_message(test_msg),
                         'Неверная проверка клиентского сообщения')

    def test_procces_client_message_no_time(self):
        test_msg = {
            ACTION: 'test',
            USER: {
                ACCOUNT_NAME: 'Guest'
            }
        }
        self.assertEqual(self.msg_to_return_error, process_client_message(test_msg),
                         'Неверная проверка клиентского сообщения')

    def test_procces_client_message_no_user(self):
        test_msg = {
            ACTION: 'test',
            TIME: 1.1,
        }
        self.assertEqual(self.msg_to_return_error, process_client_message(test_msg),
                         'Неверная проверка клиентского сообщения')

    def test_procces_client_message_wrong_user(self):
        test_msg = {
            ACTION: 'test',
            TIME: 1.1,
            USER: 'test',
        }
        self.assertEqual(self.msg_to_return_error, process_client_message(test_msg),
                         'Неверная проверка клиентского сообщения')

    def test_procces_client_message_wrong_account_name(self):
        test_msg = {
            ACTION: 'test',
            TIME: 1.1,
            USER: {
                ACCOUNT_NAME: 'test'
            }
        }
        self.assertEqual(self.msg_to_return_error, process_client_message(test_msg),
                         'Неверная проверка клиентского сообщения')


if __name__ == '__main__':
    unittest.main()
