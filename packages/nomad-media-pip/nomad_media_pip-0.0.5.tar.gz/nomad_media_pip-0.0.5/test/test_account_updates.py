import unittest
from unittest import skip
from unittest.mock import patch, Mock

from src.nomad_sdk import Nomad_SDK

from config.config import CONFIG

class TestAccountUpdate(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

    def test_get_user_info(self):
        try:
            user_info = self.nomad_sdk.get_user()
            self.assertIsInstance(user_info, dict)
            self.assertIn('id', user_info)
            self.assertIn('firstName', user_info)
            self.assertIn('lastName', user_info)
            self.assertIn('email', user_info)

        except Exception as error:
            if self.nomad_sdk.config['apiType'] != 'portal':
                self.assertEqual(str(error.args[0]), 'This function is only available for portal API type.')
            else:
                print(error.args[0])
                self.fail("get_user() raised an exception unexpectedly!")

    @skip
    def test_change_user_email(self):
        try:
            new_email = "newEmail@newEmail.com"
            self.nomad_sdk.change_email(new_email, self.nomad_sdk.config['password'])

            user_info = self.nomad_sdk.get_user()

            self.assertIn('email', user_info)
            self.assertEqual(user_info['email'], new_email)

        except Exception as error:
            if self.nomad_sdk.config['apiType'] != 'portal':
                self.assertEqual(str(error.args[0]), 'This function is only available for portal API type.')
            else:
                print(error.args[0])
                self.fail("change_email() raised an exception unexpectedly!")
    
    @skip
    def test_change_user_password(self):
        try:
            new_password = "newPassword123"
            self.nomad_sdk.change_password(self.nomad_sdk.config['password'], new_password)

            user_info = self.nomad_sdk.get_user()

            self.assertIn('email', user_info)
            self.assertEqual(user_info['email'], self.nomad_sdk.config['email'])

        except Exception as error:
            if self.nomad_sdk.config['apiType'] != 'portal':
                self.assertEqual(str(error.args[0]), 'This function is only available for portal API type.')
            else:
                print(error.args[0])
                self.fail("change_password() raised an exception unexpectedly!")
   
    def test_update_user_info(self):
        try:
            new_first_name = "NewFirstName"
            new_last_name = "NewLastName"
            self.nomad_sdk.update_user(None, None, None, new_first_name, new_last_name, None, 
                                       None, None, None, None, None)
            
            user_info = self.nomad_sdk.get_user()
            self.assertIn('firstName', user_info)
            self.assertIn('lastName', user_info)
            self.assertEqual(user_info['firstName'], new_first_name)
            self.assertEqual(user_info['lastName'], new_last_name)
            
        except Exception as error:
            if self.nomad_sdk.config['apiType'] != 'portal':
                self.assertEqual(str(error.args[0]), 'This function is only available for portal API type.')
            else:
                print(error.args[0])
                self.fail("update_user() raised an exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
