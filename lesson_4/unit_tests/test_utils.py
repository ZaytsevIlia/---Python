import json
import unittest
import os
import sys

sys.path.insert(0, os.path.join(os.getcwd(), '..'))
from common.variables import ACTION, TIME, USER, ACCOUNT_NAME, PRESENCE, ENCODING, RESPONSE, ERROR
from common.utils import get_message, send_message


class TestSocket:
    def __init__(self, test_dict):
        self.test_dict = test_dict
        self.encoded_msg = None
        self.received_msg = None

    def send(self, msg_to_send):
        json_test_msg = json.dumps(self.test_dict)
        self.encoded_msg = json_test_msg.encode(ENCODING)
        self.received_msg = msg_to_send

    def recv(self, max_length):
        json_test_msg = json.dumps(self.test_dict)
        return json_test_msg.encode(ENCODING)


class TestUtils(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    test_msg_ok = {RESPONSE: 200}
    test_msg_error = {
        RESPONSE: 400,
        ERROR: 'Bad Request'
    }
    test_dict = {
        ACTION: PRESENCE,
        TIME: 1.1,
        USER: {
            ACCOUNT_NAME: 'Guest'
        }
    }

    def test_get_message_ok(self):
        test_socket = TestSocket(self.test_msg_ok)
        self.assertEqual(self.test_msg_ok, get_message(test_socket), 'Ошибка в разборе сообщения')

    def test_get_message_error(self):
        test_socket = TestSocket(self.test_msg_error)
        self.assertEqual(self.test_msg_error, get_message(test_socket), 'Ошибка в разборе сообщения')

    def test_get_message_raise_error(self):
        self.assertRaises(TypeError, get_message, TestSocket('test'))

    def test_send_message_ok(self):
        test_socket = TestSocket(self.test_dict)
        send_message(test_socket, self.test_dict)
        self.assertEqual(test_socket.encoded_msg, test_socket.received_msg)

    def test_send_message_error(self):
        test_socket = TestSocket(self.test_dict)
        send_message(test_socket, self.test_dict)
        self.assertRaises(TypeError, send_message, test_socket, 'test')


if __name__ == '__main__':
    unittest.main()
