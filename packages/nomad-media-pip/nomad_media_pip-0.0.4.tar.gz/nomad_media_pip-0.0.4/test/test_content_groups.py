import unittest

from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG

class TestContentGroups(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

        cls.content_group_id = cls.nomad_sdk.create_content_group("Test Content Group")["id"]

    @classmethod
    def tearDownClass(cls):
        cls.nomad_sdk.delete_content_group(cls.content_group_id)

    def test_get_content_groups(self):
        try:
            CONTENT_GROUPS = self.nomad_sdk.get_content_groups()
            
            self.assertIsInstance(CONTENT_GROUPS, list)
            self.assertGreater(len(CONTENT_GROUPS), 0)
            self.assertTrue(all("id" in content_group for content_group in CONTENT_GROUPS))
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("get_content_groups() raised an exception unexpectedly!")

    def test_create_content_group(self):
        try:
            CONTENT_GROUP = self.nomad_sdk.create_content_group("Test Content Group 1")
            
            self.assertIsInstance(CONTENT_GROUP, dict)
            self.assertIn("id", CONTENT_GROUP)

            self.nomad_sdk.delete_content_group(CONTENT_GROUP["id"])
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("create_content_group() raised an exception unexpectedly!")

    def test_get_content_group(self):
        try:
            CONTENT_GROUP = self.nomad_sdk.get_content_group(self.content_group_id)
            
            self.assertIsInstance(CONTENT_GROUP, dict)
            self.assertIn("id", CONTENT_GROUP)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("get_content_group() raised an exception unexpectedly!")

    def test_rename_content_group(self):
        try:
            CONTENT_GROUP = self.nomad_sdk.rename_content_group(self.content_group_id, "Test Content Group Renamed")
            
            self.assertIsInstance(CONTENT_GROUP, dict)
            self.assertIn("id", CONTENT_GROUP)
            self.assertEqual(CONTENT_GROUP["name"], "Test Content Group Renamed")
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("rename_content_group() raised an exception unexpectedly!")

    def test_add_content_to_content_group(self):
        try:
            CONTENTS = ['f77d514e-092b-4a37-91e7-9c5d1c7ba7ff', 'f06762c8-a3d1-4f5d-bd2f-2f41f5c7ff9a'];

            CONTENT_GROUP = self.nomad_sdk.add_contents_to_content_group(self.content_group_id, CONTENTS)
            
            self.assertIsInstance(CONTENT_GROUP, dict)
            self.assertIn("id", CONTENT_GROUP)

            CONTENT_GROUP_INFO = self.nomad_sdk.get_content_group(self.content_group_id)

            self.assertGreater(len(CONTENT_GROUP_INFO["contents"]), 0)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("add_content_to_content_group() raised an exception unexpectedly!")

    def test_share_content_with_user(self):
        try:
            USER_ID = "1f8271f4-febc-4090-874e-86619441703e"

            CONTENT_GROUP = self.nomad_sdk.share_content_group_with_user(self.content_group_id, 
                                                                         [USER_ID])
            
            self.assertIsInstance(CONTENT_GROUP, dict)
            self.assertIn("id", CONTENT_GROUP)

            CONTENT_GROUP_INFO = self.nomad_sdk.get_content_group(self.content_group_id)
            
            self.assertEqual(USER_ID, CONTENT_GROUP_INFO["sharedUsers"][0]["id"])
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("share_content_with_user() raised an exception unexpectedly!")

    def test_get_portal_groups(self):
        try:
            PORTAL_GROUPS = self.nomad_sdk.get_portal_groups(["savedSearches", "contentGroups", "sharedContentGroups"])

            self.assertIsInstance(PORTAL_GROUPS, dict)
            self.assertIn("savedSearches", PORTAL_GROUPS)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("get_portal_groups() raised an exception unexpectedly!")

    def test_stop_sharing_contnet_group_with_user(self):
        try:
            USER_ID = "1f8271f4-febc-4090-874e-86619441703e"

            CONTENT_GROUP = self.nomad_sdk.stop_sharing_content_group_with_user(self.content_group_id, 
                                                                                [USER_ID])
            
            self.assertIsInstance(CONTENT_GROUP, dict)
            self.assertIn("id", CONTENT_GROUP)

            CONTENT_GROUP_INFO = self.nomad_sdk.get_content_group(self.content_group_id)
            
            self.assertEqual(len(CONTENT_GROUP_INFO["sharedUsers"]), 0)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("stop_sharing_contnet_group_with_user() raised an exception unexpectedly!")

    def test_remove_content_from_content_group(self):
        try:
            CONTENTS = ['f77d514e-092b-4a37-91e7-9c5d1c7ba7ff', 'f06762c8-a3d1-4f5d-bd2f-2f41f5c7ff9a'];

            CONTENT_GROUP = self.nomad_sdk.remove_contents_from_content_group(self.content_group_id, CONTENTS)
            
            self.assertIsInstance(CONTENT_GROUP, dict)
            self.assertIn("id", CONTENT_GROUP)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("remove_content_from_content_group() raised an exception unexpectedly!")

    def test_delete_content_group(self):
        try:
            CONTENT_GROUP = self.nomad_sdk.create_content_group("Test Content Group 2")

            self.nomad_sdk.delete_content_group(CONTENT_GROUP["id"])
            
            CONTENT_GROUPS = self.nomad_sdk.get_content_groups()

            self.assertNotIn(CONTENT_GROUP["id"], [content_group["id"] for content_group in CONTENT_GROUPS])
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.nomad_sdk.create_content_group("Test Content Group")
                self.fail("delete_content_group() raised an exception unexpectedly!")