import unittest

from src.nomad_sdk import Nomad_SDK
from config.config import CONFIG

import time

CONTENT_DEFINITION_ID = "412a30e3-73ee-4eae-b739-e1fc87601c7d"

class TestConfig(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.nomad_sdk = Nomad_SDK(CONFIG)

        cls.TEMP_LIVE_INPUT = cls.nomad_sdk.create_live_input("Test Live Input", 
            "212.22.113.111/12", "RTMP_PUSH", None, None, None, None)
        
        cls.EVENT_ID = cls.nomad_sdk.create_and_update_event(None,
                None, "New Event", None, "2024-01-01T00:00:00.000Z",
                "2024-01-01T11:00:00.000Z", None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None,
                None, None, None)
        
    @classmethod
    def tearDownClass(cls):
        cls.nomad_sdk.delete_live_input(cls.TEMP_LIVE_INPUT["id"])

        EVENTS = get_events(cls)

        DELETE_IDS = [event['id'] for event in EVENTS if event['title'] == "New Event"]
        for DELETE_ID in DELETE_IDS:
            cls.nomad_sdk.delete_event(DELETE_ID, CONTENT_DEFINITION_ID)

    def test_create_event(self):
        try:
            EVENT = self.nomad_sdk.create_and_update_event(None,
                None, "New Event", None, "2024-01-01T00:00:00.000Z",
                "2024-01-01T11:00:00.000Z", None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None,
                None, None, None)
            
            self.assertIsInstance(EVENT, str)
            self.assertEqual(EVENT, "New Event")

            self.nomad_sdk.delete_event(EVENT["id"], CONTENT_DEFINITION_ID)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("create_event() raised an exception unexpectedly!")

    def test_extent_live_schedule(self):
        try:
            self.nomad_sdk.extend_live_schedule(self.EVENT_ID, 
                [
                    {
                        "description": "Monday",
                        "id": "16bebfa8-65cc-451e-9744-d09d6c761e4a"
                    },
                    {
                        "description": "Thursday",
                        "id": "2691d391-e1b1-43b6-97e2-5fc6b39479ef"
                    }
                ], 2, None)
            
            EVENTS = get_events(self)

            EVENT_NAME_COUNT = len([event for event in EVENTS if event['title'] == "New Event"])

            self.assertGreater(EVENT_NAME_COUNT, 1)

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("extend_live_schedule() raised an exception unexpectedly!")

    def test_add_live_schedule_to_event(self):
        try:
            self.nomad_sdk.add_live_schedule_to_event(self.EVENT_ID, None, None, None, None, None, 
                {
                    "id": self.TEMP_LIVE_INPUT["id"], 
                    "description": self.TEMP_LIVE_INPUT["name"]
                }, None, None, None, None)
            
            LIVE_SCHEDULE_INFO = self.nomad_sdk.get_live_schedule(self.EVENT_ID)

            self.assertEqual("Scheduled", LIVE_SCHEDULE_INFO["status"]["description"])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("add_live_schedule_to_event() raised an exception unexpectedly!")

    def test_get_live_schedule(self):
        try:
            LIVE_SCHEDULE_INFO = self.nomad_sdk.get_live_schedule(self.EVENT_ID)
            
            self.assertIsInstance(LIVE_SCHEDULE_INFO, dict)
            self.assertIn("contentId", LIVE_SCHEDULE_INFO)
        
        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("get_live_schedule() raised an exception unexpectedly!")

    def test_start_live_schedule(self):
        try:
            self.nomad_sdk.start_live_schedule(self.EVENT_ID)

            LIVE_SCHEDULE_INFO = self.nomad_sdk.get_live_schedule(self.EVENT_ID)

            self.assertEqual("Active", LIVE_SCHEDULE_INFO["status"]["description"])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("start_live_schedule() raised an exception unexpectedly!")

    def test_stop_live_schedule(self):
        try:
            while True:
                try:
                    self.nomad_sdk.stop_live_schedule(self.EVENT_ID)
                    break
                except:
                    time.sleep(5)

            LIVE_SCHEDULE_INFO = self.nomad_sdk.get_live_schedule(self.EVENT_ID)

            self.assertEqual("Terminated", LIVE_SCHEDULE_INFO["status"]["description"])

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("stop_live_schedule() raised an exception unexpectedly!")

    def test_delete_event(self):
        try:
            EVENT = self.nomad_sdk.create_and_update_event(None,
                None, "New Delete Event", None, "2024-01-01T00:00:00.000Z",
                "2024-01-01T11:00:00.000Z", None, None, None, None, None, None, None,
                None, None, None, None, None, None, None, None, None, None, None,
                None, None, None)
            
            self.nomad_sdk.delete_event(EVENT["id"], CONTENT_DEFINITION_ID)

            EVENTS = get_events(self)

            self.assertEqual(0, len([event for event in EVENTS if event['title'] == "New Delete Event"]))

        except Exception as error:
            if self.nomad_sdk.config["apiType"] != "admin":
                self.assertEqual(str(error), "This function is only available for admin API type.")
            else:
                print(error.args[0])
                self.fail("delete_event() raised an exception unexpectedly!")

def get_events(nomad_sdk):
    EVENTS = nomad_sdk.search(None, None, None,
        [
            {
                "fieldName": "contentDefinitionId",
                "operator": "Equals",
                "values": CONTENT_DEFINITION_ID
            }
        ], None, None, None, None, True, None)

    return EVENTS["items"]
