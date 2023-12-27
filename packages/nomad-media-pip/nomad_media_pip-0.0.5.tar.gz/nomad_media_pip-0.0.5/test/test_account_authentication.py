import unittest
from unittest import skip
from unittest.mock import patch, Mock

from src.nomad_sdk import Nomad_SDK

from config.config import CONFIG

class TestAccount(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.NomadSDK = Nomad_SDK(CONFIG)

    def test_login(self):
        self.NomadSDK.login()
        self.assertIsNotNone(self.NomadSDK.token)
        self.assertIsNotNone(self.NomadSDK.refresh_token_val)
        self.assertIsNotNone(self.NomadSDK.expiration_seconds)

    def test_forgot_password(self):
        self.NomadSDK.forgot_password()

    @unittest.skip("requires user interaction")
    def test_reset_password(self):
        self.NomadSDK.resetPassword(CONFIG.username, "given token", "NewStr0ngPassw0rd!!")

if __name__ == '__main__':
    unittest.main()