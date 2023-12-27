import unittest
from helpers.slugify import _slugify

from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG

CONTENT_DEFINITION_ID = "33cec5ca-6170-4237-842b-78bf1ef17932";

class TestContent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

        CONTENT = cls.nomad_sdk.create_content(CONTENT_DEFINITION_ID, None)
        cls.contentId = CONTENT["contentId"]

    @classmethod
    def tearDownClass(cls):
        cls.nomad_sdk.delete_content(cls.contentId, CONTENT_DEFINITION_ID)

    def test_create_content(self):
        try:
            CONTENT = self.nomad_sdk.create_content(CONTENT_DEFINITION_ID, None)
            
            self.assertIsInstance(CONTENT, dict)
            self.assertIn("contentId", CONTENT)

            self.nomad_sdk.delete_content(CONTENT["contentId"], CONTENT_DEFINITION_ID)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("create_content() raised an exception unexpectedly!")

    def test_update_content(self):
        try:
            self.nomad_sdk.update_content(self.contentId, CONTENT_DEFINITION_ID,
                {
                    "name": "New Performer",
                    "slug": _slugify("New Performer"),
                    "performerType": {
                        "id": "3cf90a81-2f98-456e-ade6-d3968f3f59c6",
                        "description": "Actor"
                    }
                }, None)
            
            CONTENT_INFO = self.nomad_sdk.get_content(self.contentId, CONTENT_DEFINITION_ID, None)

            self.assertEqual(CONTENT_INFO["properties"]["name"], "New Performer")
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("update_content() raised an exception unexpectedly!")

    def test_get_content(self):
        try:
            CONTENT_INFO = self.nomad_sdk.get_content(self.contentId, CONTENT_DEFINITION_ID, None)
            
            self.assertIsInstance(CONTENT_INFO, dict)
            self.assertIn("contentId", CONTENT_INFO)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_content() raised an exception unexpectedly!")

    def test_delete_content(self):
        try:
            CONTENT = self.nomad_sdk.create_content(CONTENT_DEFINITION_ID, None)

            self.nomad_sdk.delete_content(CONTENT["contentId"], CONTENT_DEFINITION_ID)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("delete_content() raised an exception unexpectedly!")

    def test_should_get_content_user_tracking(self):
        try:
            CONTENT_USER_TRACKING = self.nomad_sdk.get_content_user_track(self.contentId,
                CONTENT_DEFINITION_ID, "id", False, None, None)
            
            self.assertIsInstance(CONTENT_USER_TRACKING, dict)
            self.assertIn("items", CONTENT_USER_TRACKING)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_content_user_tracking() raised an exception unexpectedly!")

    def test_should_deactivate_content_user_tracking(self):
        try:
            CONTENT_USER_TRACKING = self.nomad_sdk.deactivate_content_user_track(None,
                "6e804251-72a2-4d8c-9589-f68f8f5ec086", 
                "3ff29f61-bd0b-4c17-b855-49db5a292aeb", False)
            
            self.assertIsInstance(CONTENT_USER_TRACKING, dict)
            self.assertIn("items", CONTENT_USER_TRACKING)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("deactivate_content_user_tracking() raised an exception unexpectedly!")