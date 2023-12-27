import unittest
from unittest import skip
from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG

class TestAssetUpload(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

    def test_upload_asset(self):
        try:
            ID = self.nomad_sdk.upload_asset(
                None, None, None, None, None, None, "replace",
                "./test/The-Office.jpeg", "73d06e60-9607-4018-b666-775790c0f0c2"
            )
            self.assertIsInstance(ID, str)

            offset = 0
            found = False
            while True:
                SEARCH_INFO = self.nomad_sdk.search(
                    None, offset, None,
                    [
                        {
                            "fieldName": "contentDefinitionId",
                            "operator": "Equals",
                            "values": "3ff29f61-bd0b-4c17-b855-49db5a292aeb"
                        },
                        {
                            "fieldName": "assetType",
                            "operator": "Equals",
                            "values": 2
                        },
                        {
                            "fieldName": "parentId",
                            "operator": "Equals",
                            "values": "73d06e60-9607-4018-b666-775790c0f0c2"
                        }
                    ],
                    None, None, None, None, None, None)
                
                for item in SEARCH_INFO:
                    if item['id'] == ID:
                        found = True
                        break

                if len(SEARCH_INFO) != 100:
                    break
                
                offset += 1
            
            self.assertEqual(found, True)
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("upload_asset() raised an exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()
