import unittest

from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG

import time

CONTENT_DEFINITION_ID = "73d06e60-9607-4018-b666-775790c0f0c2"
RELATED_CONTENT_ID = "f06762c8-a3d1-4f5d-bd2f-2f41f5c7ff9a"

class TestContentAdmin(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

        cls.TEMP_ASSET = cls.nomad_sdk.create_placeholder_asset(
            CONTENT_DEFINITION_ID, "Temp Asset.exe")
        
        time.sleep(5)
        
    @classmethod
    def tearDownClass(cls):
        cls.nomad_sdk.delete_asset(cls.TEMP_ASSET["id"])

    @unittest.skip("Skipping test_add_custom_properties")
    def test_add_custom_properties(self):
        try:
            CUSTOM_PROPERTIES = self.nomad_sdk.add_custom_property(
                self.TEMP_ASSET["id"], 'Custom Property', None,
                { 
                    "customProp1": "First Custom Property", 
                    "customProp2": "Second Custom Property" 
                })
            
            self.assertIsInstance(CUSTOM_PROPERTIES, dict)
            self.assertIn("id", CUSTOM_PROPERTIES)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("add_custom_properties() raised an exception unexpectedly!")
    
    def test_add_related_content(self):
        try:
            RELATED_CONTENT = self.nomad_sdk.add_related_content(
                self.TEMP_ASSET["id"], RELATED_CONTENT_ID, "asset")

            time.sleep(5)
            ASSET_DETAILS = self.nomad_sdk.get_asset_details(self.TEMP_ASSET["id"])

            self.assertTrue(any(relatedContent["id"] == RELATED_CONTENT_ID for relatedContent in ASSET_DETAILS["relatedContent"]))
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("add_related_content() raised an exception unexpectedly!")

    def test_delete_related_content(self):
        try:
            DELETE_INFO = self.nomad_sdk.delete_related_content(self.TEMP_ASSET["id"], 
                RELATED_CONTENT_ID, "asset")
        
            time.sleep(5)
            ASSET_DETAILS = self.nomad_sdk.get_asset_details(self.TEMP_ASSET["id"])

            self.assertFalse(any(relatedContent["id"] == RELATED_CONTENT_ID for relatedContent in ASSET_DETAILS["relatedContent"]))
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("delete_related_content() raised an exception unexpectedly!")

    def test_tag(self):
        try:
            TAG = self.nomad_sdk.create_tag_or_collection("tag", "Test Tag")
            
            TAG_ID = TAG["id"]

            self.nomad_sdk.add_tag_or_collection("tag", self.TEMP_ASSET["id"], 
                "asset", "Test Tag", TAG_ID, False)
        
            time.sleep(5)
            ASSET_DETAILS = self.nomad_sdk.get_asset_details(self.TEMP_ASSET["id"])

            self.assertTrue(any(tag["id"] == TAG_ID for tag in ASSET_DETAILS["tags"]))

            self.nomad_sdk.remove_tag_or_collection("tag", self.TEMP_ASSET["id"], 
                "asset", TAG_ID)
        
            time.sleep(5)
            ASSET_DETAILS = self.nomad_sdk.get_asset_details(self.TEMP_ASSET["id"])

            if "tags" in ASSET_DETAILS:
                self.assertFalse(any(tag["id"] == TAG_ID for tag in ASSET_DETAILS["tags"]))
            else:
                self.assertNotIn("tags", ASSET_DETAILS)

            self.nomad_sdk.delete_tag_or_collection("tag", TAG_ID)

            time.sleep(5)
            with self.assertRaises(Exception) as context:
                self.nomad_sdk.get_tag_or_collection("tag", TAG_ID)
           
            self.assertTrue('Get Tag or Collection Failed: 404' in str(context.exception))
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("test raised an exception unexpectedly!")

    def test_collection(self):
        try:
            COLLECTION = self.nomad_sdk.create_tag_or_collection("collection", "Test Collection")

            COLLECTION_ID = COLLECTION["id"]
            
            self.nomad_sdk.add_tag_or_collection("collection", self.TEMP_ASSET["id"], 
                "asset", "Test Collection", COLLECTION_ID, False)
        
            time.sleep(5)
            ASSET_DETAILS = self.nomad_sdk.get_asset_details(self.TEMP_ASSET["id"])

            self.assertTrue(any(collection["id"] == COLLECTION_ID for collection in ASSET_DETAILS["collections"]))

            self.nomad_sdk.remove_tag_or_collection("collection", self.TEMP_ASSET["id"], 
                "asset", COLLECTION_ID)
        
            time.sleep(5)
            ASSET_DETAILS = self.nomad_sdk.get_asset_details(self.TEMP_ASSET["id"])

            if "collections" in ASSET_DETAILS:
                self.assertFalse(any(collection["id"] == COLLECTION_ID for collection in ASSET_DETAILS["collections"]))
            else:
                self.assertNotIn("collections", ASSET_DETAILS)

            self.nomad_sdk.delete_tag_or_collection("collection", COLLECTION_ID)

            time.sleep(5)
            with self.assertRaises(Exception) as context:
                self.nomad_sdk.get_tag_or_collection("collection", COLLECTION_ID)
           
            self.assertTrue('Get Tag or Collection Failed: 404' in str(context.exception))

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("add_collection() raised an exception unexpectedly!")

    def test_bulk_update_metadata(self):
        try:
            COLLECTIONS = ["d7e21c67-e78d-4ccb-8b3b-550698cef770",
                "b113d491-173c-4e04-b507-f8b30f584a27"]

            RELATED_CONTENT = ["4d3be401-d66e-4848-9dee-89fc43ce2a4c"]

            TAGS = ["80dae5d4-20c4-41a5-8edf-588a2d84b0e2",
                "d0104c26-6941-47da-908b-f39ce9a5a9ce"]

            self.nomad_sdk.bulk_update_metadata([self.TEMP_ASSET["id"]],
                COLLECTIONS, RELATED_CONTENT, TAGS, None)
        
        except Exception as error:
            print(error.args[0])
            self.fail("bulk_update_metadata() raised an exception unexpectedly!")

def main():
    unittest.main()