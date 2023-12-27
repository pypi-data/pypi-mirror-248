import unittest

from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG

CONTENT_ID = "6e804251-72A2-4D8C-9589-f68f8f5ec086"

class TestAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

    def test_get_audit(self):
        try:
            AUDIT = self.nomad_sdk.get_audit(CONTENT_ID)
            
            self.assertIsInstance(AUDIT, list)
            self.assertTrue(all("assetRootName"in item for item in AUDIT))
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_audit() raised an exception unexpectedly!")

if __name__ == '__main__':
    unittest.main()