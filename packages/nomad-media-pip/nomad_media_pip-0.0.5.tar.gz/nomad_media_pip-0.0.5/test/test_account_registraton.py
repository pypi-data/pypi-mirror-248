import unittest
from unittest import skip
from unittest.mock import patch, Mock

from src.nomad_sdk import Nomad_SDK

from config.config import CONFIG

class TestAccountRegistration(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)
        print("Test")

    def test_register_user(self):
        user_info = self.nomad_sdk.register("email@email.com", "First", "Last", "Str0ngPassword!!")
        self.assertIsInstance(user_info, dict)
        self.assertIn('id', user_info)
        self.assertIn('firstName', user_info)
        self.assertIn('lastName', user_info)
        self.assertIn('email', user_info)

    def test_resend_code(self):
        self.nomad_sdk.resend_code()

    def test_verify_user(self):
        user_info = self.nomad_sdk.verify("000000")
        self.assertIsInstance(user_info, dict)
        self.assertIn('loginStatus', user_info)


if __name__ == '__main__':
    unittest.main()