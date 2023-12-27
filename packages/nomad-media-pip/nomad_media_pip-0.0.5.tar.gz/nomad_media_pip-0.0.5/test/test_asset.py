import unittest

from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG
import time

ADMIN_ASSET_ID = "f77d514e-092b-4a37-91e7-9c5d1c7ba7ff"
FOLDER_ID = "73d06e60-9607-4018-b666-775790c0f0c2"
PORTAL_ASSET_ID = "c558e400-836d-497a-829e-4b87378b1d11"

class TestAsset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

    def test_archive_asset(self):
        try:
            ARCHIVE_INFO = self.nomad_sdk.archive_asset(ADMIN_ASSET_ID)

            self.assertIsInstance(ARCHIVE_INFO, dict)
            self.assertIn('id', ARCHIVE_INFO)

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("archive_asset() raised an exception unexpectedly!")

    def test_clip_asset(self):
        try:
            CLIP_INFO = self.nomad_sdk.clip_asset(ADMIN_ASSET_ID, "00:00:00;00", 
                "00:00:10;00", "Test Clip", None, None, None, None, None, None)

            self.assertIsInstance(CLIP_INFO, dict)
            self.assertIn('id', CLIP_INFO)

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("clip_asset() raised an exception unexpectedly!")

    def test_create_annotation(self):
        try:
            ANNOTATION_INFO = self.nomad_sdk.create_annotation(PORTAL_ASSET_ID, 
                "00:00:00;00", "00:00:10;00", "First Keyword", "Second Keyword", 
                "Description", 
                {
                    "description": "United States",
                    "id": "cee90a86-ea42-4723-801b-568851296481"
                }, None, None)

            self.assertIsInstance(ANNOTATION_INFO, dict)
            self.assertIn('id', ANNOTATION_INFO)
            self.assertIn('startTimeCode', ANNOTATION_INFO)
            self.assertIn('endTimeCode', ANNOTATION_INFO)
            self.assertIn('imageUrl', ANNOTATION_INFO)
            self.assertIn('properties', ANNOTATION_INFO)

            self.nomad_sdk.delete_annotation(PORTAL_ASSET_ID, ANNOTATION_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("create_annotation() raised an exception unexpectedly!")

    def test_create_asset_ad_break(self):
        try:
            AD_BREAK_INFO = self.nomad_sdk.create_asset_ad_break(ADMIN_ASSET_ID, 
                "00:00:00;00", None, None)

            self.assertIsInstance(AD_BREAK_INFO, dict)
            self.assertIn('id', AD_BREAK_INFO)
            self.assertIn('adBreakType', AD_BREAK_INFO)

            self.nomad_sdk.delete_asset_ad_break(ADMIN_ASSET_ID, AD_BREAK_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("create_asset_ad_break() raised an exception unexpectedly!")

    def test_create_folder_asset(self):
        try:
            FOLDER_ASSET_INFO = self.nomad_sdk.create_folder_asset(FOLDER_ID, "Test Folder")

            self.assertIsInstance(FOLDER_ASSET_INFO, dict)
            self.assertIn('id', FOLDER_ASSET_INFO)

            self.nomad_sdk.delete_asset(FOLDER_ASSET_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("create_folder_asset() raised an exception unexpectedly!")

    def test_create_placeholder_asset(self):
        try:
            PLACEHOLDER_ASSET_INFO = self.nomad_sdk.create_placeholder_asset(FOLDER_ID, 
                "Test Placeholder.exe")

            self.assertIsInstance(PLACEHOLDER_ASSET_INFO, dict)
            self.assertIn('id', PLACEHOLDER_ASSET_INFO)

            self.nomad_sdk.delete_asset(PLACEHOLDER_ASSET_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("create_placeholder_asset() raised an exception unexpectedly!")

    def test_create_screenshot_at_timecode(self):
        try:
            SCREENSHOT_INFO = self.nomad_sdk.create_screenshot_at_timecode(ADMIN_ASSET_ID, 
                "00:00:01;00")

            self.assertIsInstance(SCREENSHOT_INFO, dict)
            self.assertIn('id', SCREENSHOT_INFO)

            self.nomad_sdk.delete_asset(SCREENSHOT_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("create_screenshot_at_timecode() raised an exception unexpectedly!")

    def test_delete_annotation(self):
        try:
            ANNOTATION_INFO = self.nomad_sdk.create_annotation(PORTAL_ASSET_ID, 
                "00:00:00;00", "00:00:10;00", "First Keyword", "Second Keyword", 
                "Description", 
                {
                    "description": "United States",
                    "id": "cee90a86-ea42-4723-801b-568851296481"
                }, None, None)

            self.nomad_sdk.delete_annotation(PORTAL_ASSET_ID, ANNOTATION_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("delete_annotation() raised an exception unexpectedly!")

    def test_delete_asset(self):
        try:
            ASSET_INFO = self.nomad_sdk.create_placeholder_asset(FOLDER_ID,
                "Test Placeholder.exe")
            
            self.nomad_sdk.delete_asset(ASSET_INFO['id'])
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("delete_asset() raised an exception unexpectedly!")

    def test_delete_asset_ad_break(self):
        try:
            AD_BREAK_INFO = self.nomad_sdk.create_asset_ad_break(ADMIN_ASSET_ID, 
                "00:00:05;00", None, None)

            self.nomad_sdk.delete_asset_ad_break(ADMIN_ASSET_ID, AD_BREAK_INFO['id'])
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("delete_asset_ad_break() raised an exception unexpectedly!")

    def download_archive_asset(self):
        try:
            ARCHIVE_INFO = self.nomad_sdk.archive_asset(ADMIN_ASSET_ID)

            self.nomad_sdk.download_archive_asset(ARCHIVE_INFO['id'], "./test/")

            self.assertIsInstance(ARCHIVE_INFO, dict)
            self.assertIn('items', ARCHIVE_INFO)
            self.assertTrue(all('id' in item for item in ARCHIVE_INFO['items']))
            self.assertTrue('totalItems', ARCHIVE_INFO)

        except Exception as error:
            print(error.args[0])
            self.fail("download_archive_asset() raised an exception unexpectedly!")

    def test_duplicate_asset(self):
        try:
            DUPLICATE_INFO = self.nomad_sdk.duplicate_asset(ADMIN_ASSET_ID)

            self.assertIsInstance(DUPLICATE_INFO, dict)
            self.assertIn('id', DUPLICATE_INFO)

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("duplicate_asset() raised an exception unexpectedly!")

    def test_get_annotation(self):
        try:
            ANNOTATION_INFO = self.nomad_sdk.create_annotation(PORTAL_ASSET_ID, 
                "00:00:00;00", "00:00:10;00", "First Keyword", "Second Keyword", 
                "Description", 
                {
                    "description": "United States",
                    "id": "cee90a86-ea42-4723-801b-568851296481"
                }, None, None)

            ASSET_ANNOTATIONS = self.nomad_sdk.get_annotations(PORTAL_ASSET_ID)

            self.assertIsInstance(ASSET_ANNOTATIONS, list)
            self.assertTrue(all('id' in annotation for annotation in ASSET_ANNOTATIONS))

            self.nomad_sdk.delete_annotation(PORTAL_ASSET_ID, ANNOTATION_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("get_annotation() raised an exception unexpectedly!")

    def test_get_asset(self):
        try:
            ASSET_INFO = self.nomad_sdk.get_asset(ADMIN_ASSET_ID)

            self.assertIsInstance(ASSET_INFO, dict)
            self.assertIn('id', ASSET_INFO)

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_asset() raised an exception unexpectedly!")

    def test_get_asset_ad_breaks(self):
        try:
            AD_BREAK_INFO = self.nomad_sdk.create_asset_ad_break(ADMIN_ASSET_ID, 
                "00:00:00;00", None, None)

            time.sleep(5)
            ASSET_AD_BREAKS = self.nomad_sdk.get_asset_ad_breaks(ADMIN_ASSET_ID)

            self.assertIsInstance(ASSET_AD_BREAKS, list)
            self.assertTrue(all('id' in ad_break for ad_break in ASSET_AD_BREAKS))

            self.nomad_sdk.delete_asset_ad_break(ADMIN_ASSET_ID, AD_BREAK_INFO['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_asset_ad_breaks() raised an exception unexpectedly!")

    def test_get_asset_details(self):
        try:
            ASSET_DETAILS = self.nomad_sdk.get_asset_details(ADMIN_ASSET_ID)

            self.assertIsInstance(ASSET_DETAILS, dict)
            self.assertIn('assetId', ASSET_DETAILS)
            
        except Exception as error:
            print(error.args[0])
            self.fail("get_asset_details() raised an exception unexpectedly!")

    def test_get_asset_manifest_with_cookies(self):
        try:
            ASSET_MANIFEST = self.nomad_sdk.get_asset_manifest_with_cookies(
                "ab6f4043-8461-41b2-aa3f-bc64079fdc60", "050dc1aa-945f-4f91-81b3-c6dd35d57a3b")

            self.assertIsInstance(ASSET_MANIFEST, dict)
            self.assertIn('responseCookies', ASSET_MANIFEST)

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else: 
                print(error.args[0])
                self.fail("get_asset_manifest_with_cookies() raised an exception unexpectedly!")

    def test_get_asset_metadata(self):
        try:
            ASSET_METADATA = self.nomad_sdk.get_asset_metadata_summary(ADMIN_ASSET_ID)

            self.assertIsInstance(ASSET_METADATA, list)
            self.assertTrue(all('id' in metadata for metadata in ASSET_METADATA))

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail('get_asset_metadata() raised an exception unexpectedly!')

    def test_get_asset_parent_folders(self):
        try:
            PARENT_FOLDERS = self.nomad_sdk.get_asset_parent_folders(ADMIN_ASSET_ID, None)

            self.assertIsInstance(PARENT_FOLDERS, dict)
            self.assertIn('items', PARENT_FOLDERS)
            self.assertTrue(all('id' in item for item in PARENT_FOLDERS['items']))
            self.assertIn('totalItemCount', PARENT_FOLDERS)

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_asset_parent_folders() raised an exception unexpectedly!")

    def test_get_user_uploads(self):
        try:
            USER_UPLOADS = self.nomad_sdk.get_user_uploads(True)

            self.assertIsInstance(USER_UPLOADS, list)
            self.assertTrue(all('id' in part for part in USER_UPLOADS))

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_user_uploads() raised an exception unexpectedly!")

    def test_get_user_upload_parts(self):
        try:
            UPLOAD_PARTS = self.nomad_sdk.get_user_uploads(True)

            USER_UPLOAD_PARTS = self.nomad_sdk.get_user_upload_parts(UPLOAD_PARTS[0]['id'])

            self.assertIsInstance(USER_UPLOAD_PARTS, list)
            self.assertTrue(all('id' in part for part in USER_UPLOAD_PARTS))

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_user_upload_parts() raised an exception unexpectedly!")

    def test_import_annotations(self):
        try:
            count = 0
            try:
                PRE_ANNOTATIONS = self.nomad_sdk.get_annotations(PORTAL_ASSET_ID)
                count = len(PRE_ANNOTATIONS)
            except:
                pass

            self.nomad_sdk.import_annotations(PORTAL_ASSET_ID,
                [
                    {
                        "startTimeCode": "00:00:10;00"
                    },
                    {
                        "startTimeCode": "00:00:10;00",
                        "endTimeCode": "00:00:11;00"
                    }
                ])
            
            time.sleep(10)

            ANNOTATIONS = self.nomad_sdk.get_annotations(PORTAL_ASSET_ID)

            self.assertTrue(len(ANNOTATIONS) > count)

            for annotation in ANNOTATIONS:
                self.nomad_sdk.delete_annotation(PORTAL_ASSET_ID, annotation['id'])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
            else:
                print(error.args[0])
                self.fail("import_annotations() raised an exception unexpectedly!")

    def test_index_asset(self):
        try:
            self.nomad_sdk.index_asset(ADMIN_ASSET_ID)

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
             else:
                print(error.args[0])
                self.fail("index_asset() raised an exception unexpectedly!")

    def test_reprocess_asset(self):
        try:
            REPROCESS_INFO = self.nomad_sdk.reprocess_asset(ADMIN_ASSET_ID)

            self.assertIsInstance(REPROCESS_INFO, dict)
            self.assertIn('items', REPROCESS_INFO)
            self.assertTrue(all('id' in item for item in REPROCESS_INFO['items']))
            self.assertIn('totalItemCount', REPROCESS_INFO)

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
             else:
                print(error.args[0])
                self.fail("reprocess_asset() raised an exception unexpectedly!") 

    def test_restore_asset(self):
        try:
            self.nomad_sdk.restore_asset(ADMIN_ASSET_ID)

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
             else:
                print(error.args[0])
                self.fail("restore_asset() raised an exception unexpectedly!")

    def test_share_asset(self):
        try:
            SHARE_INFO = self.nomad_sdk.share_asset(PORTAL_ASSET_ID,
                [{ "id": "02d88875-d7fc-4a68-a397-54f55d177dfc" }], None, 5)
            
            self.assertIsInstance(SHARE_INFO, str)

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
             else:
                print(error.args[0])
                self.fail("share_asset() raised an exception unexpectedly!")

    def test_update_annotation(self):
        try:
            ANNOTATION_INFO = self.nomad_sdk.create_annotation(PORTAL_ASSET_ID, 
                "00:00:00;00", "00:00:10;00", "First Keyword", "Second Keyword", 
                "Description", 
                {
                    "description": "United States",
                    "id": "cee90a86-ea42-4723-801b-568851296481"
                }, None, None)

            self.nomad_sdk.update_annotation(PORTAL_ASSET_ID, 
                ANNOTATION_INFO["id"], "00:00:00;00", "00:00:10;00", "First Keyword", 
                "Second Keyword", "Description", 
                {
                    "description": "United States",
                    "id": "cee90a86-ea42-4723-801b-568851296481"
                }, None, None)

            self.assertIsInstance(ANNOTATION_INFO, dict)
            self.assertIn('id', ANNOTATION_INFO)
            self.assertIn('startTimeCode', ANNOTATION_INFO)
            self.assertIn('endTimeCode', ANNOTATION_INFO)
            self.assertIn('imageUrl', ANNOTATION_INFO)
            self.assertIn('properties', ANNOTATION_INFO)

            self.nomad_sdk.delete_annotation(PORTAL_ASSET_ID, ANNOTATION_INFO['id'])

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "portal":
                self.assertEqual(str(error), "This function is only available for portal API type.")
             else:
                print(error.args[0])
                self.fail("update_annotation() raised an exception unexpectedly!")

    def test_update_asset(self):
        try:
            self.nomad_sdk.update_asset(ADMIN_ASSET_ID, None,
                "2023-11-21T00:00:00Z", None, None, None)

            ASSET_INFO = self.nomad_sdk.get_asset_details(ADMIN_ASSET_ID)

            self.assertEqual(ASSET_INFO['properties']['displayDate'], "2023-11-21T00:00:00Z")

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
             else:
                print(error.args[0])
                self.fail("update_asset() raised an exception unexpectedly!")
                                                    
    def test_update_asset_ad_break(self):
        try:
            AD_BREAK_INFO = self.nomad_sdk.create_asset_ad_break(ADMIN_ASSET_ID, 
                "00:00:00;00", None, None)

            self.nomad_sdk.update_asset_ad_break(ADMIN_ASSET_ID, AD_BREAK_INFO['id'],
                "00:00:10;00", None, None)

            self.assertIsInstance(AD_BREAK_INFO, dict)
            self.assertIn('id', AD_BREAK_INFO)
            self.assertIn('adBreakType', AD_BREAK_INFO)

            self.nomad_sdk.delete_asset_ad_break(ADMIN_ASSET_ID, AD_BREAK_INFO['id'])

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
             else:
                print(error.args[0])
                self.fail("update_asset_ad_break() raised an exception unexpectedly!")

    def test_update_asset_language(self):
        try:
            self.nomad_sdk.update_asset_language(ADMIN_ASSET_ID, 
                "9838d9e8-b215-4e04-93f2-8b3ed5ed33bd")

            ASSET_INFO = self.nomad_sdk.get_asset_details(ADMIN_ASSET_ID)

            self.assertEqual(ASSET_INFO['properties']['language']['id'], "9838d9e8-b215-4e04-93f2-8b3ed5ed33bd")

        except Exception as error:
             if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
             else:
                print(error.args[0])
                self.fail("update_asset_language() raised an exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
