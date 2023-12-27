import unittest

from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

    def test_clear_server_cache(self):
        try:
            self.nomad_sdk.clear_server_cache()
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("clear_server_cache() raised an exception unexpectedly!")

    def test_get_config(self):
        try:
            CONFIG = self.nomad_sdk.get_config(1)
            
            self.assertIsInstance(CONFIG, dict)
            self.assertIn("assetRootName", CONFIG)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_config() raised an exception unexpectedly!")

    def test_get_server_time(self):
        try:
            SERVER_TIME = self.nomad_sdk.get_server_time()
            
            self.assertIsInstance(SERVER_TIME, dict)
            self.assertIn("serverTimeUtc", SERVER_TIME)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_server_time() raised an exception unexpectedly!")

def main():
    unittest.main()