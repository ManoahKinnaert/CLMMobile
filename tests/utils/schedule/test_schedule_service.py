import unittest 
from unittest.mock import patch
import datetime
from CLMMobile.utils.schedule_service.service import get_schedule_data_auto, ciruit_overseer_schedule
from copy import deepcopy

MODULE = "CLMMobile.utils.schedule_service.service"

class MockTranslation:
    def get_string_section(arg):
        return {
            "INTRODUCTION": "",
            "TREASURES TALK": "",
            "SPIRITUAL GEMS": "",
            "BIBLE READING": "",
            "STARTING A CONVERSATION": "",
            "FOLLOWING UP": "",
            "WHAT WOULD YOU SAY?": "",
            "MAKING DISCIPLES": "",
            "EXPLAINING YOUR BELIEFS": "",
            "TALK": "",
            "LIVING TALK": "",
            "CONGREGATION BIBLE STUDY": "",
            "CONCLUDING COMMENTS": "",
            "PUBLIC TALK": "",
            "WATCHTOWER STUDY": "",
            "CIRCUIT OVERSEER TALK": "",
            "SERVICE TALK": ""
        }

class TestScheduleService(unittest.TestCase):

    MOCK_MIDWEEK_SCHEDULE = [
        {"id": 0, "time": 1, "key": "INTRODUCTION"},
        {"id": 1, "time": 10, "key": "TREASURES TALK"},
        {"id": 2, "time": 10, "key": "SPIRITUAL GEMS"},
        {"id": 3, "time": 4, "key": "BIBLE READING", "student": True},
        {"id": 4, "time": 4, "key": "STARTING A CONVERSATION", "student": True},
        {"id": 5, "time": 3, "key": "FOLLOWING UP", "student": True},
        {"id": 6, "time": 5, "key": "WHAT WOULD YOU SAY?", "student": False},
        {"id": 7, "time": 5, "key": "MAKING DISCIPLES", "student": True},
        {"id": 8, "time": 5, "key": "EXPLAINING YOU BELIEFS", "student": True},
        {"id": 9, "time": 5, "key": "TALK", "student": True},
        {"id": 10, "time": 15, "key": "LIVING TALK"},
        {"id": 11, "time": 30, "key": "CONGREGATION BIBLE STUDY"},
        {"id": 12, "time": 3, "key": "CONCLUDING COMMENTS"}
    ]

    MOCK_VARIABLE_ITEMS = [
         {"id": 4, "time": 4, "key": "STARTING A CONVERSATION", "student": True},
        {"id": 5, "time": 3, "key": "FOLLOWING UP", "student": True},
        {"id": 6, "time": 5, "key": "WHAT WOULD YOU SAY?", "student": False},
        {"id": 7, "time": 5, "key": "MAKING DISCIPLES", "student": True},
        {"id": 8, "time": 5, "key": "EXPLAINING YOU BELIEFS", "student": True},
        {"id": 9, "time": 5, "key": "TALK", "student": True}
    ]

    MOCK_WEEKEND_SCHEDULE = [
        {"id": 13, "time": 30, "key": "PUBLIC TALK"},
        {"id": 14, "time": 60, "key": "WATCHTOWER STUDY"}
    ]

    MOCK_MIDWEEK_SCHEDULE_CIRCUIT_OVERSEER = [
        {"id": 0, "time": 1, "key": "INTRODUCTION"},
        {"id": 1, "time": 10, "key": "TREASURES TALK"},
        {"id": 2, "time": 10, "key": "SPIRITUAL GEMS"},
        {"id": 3, "time": 4, "key": "BIBLE READING", "student": True},
        {"id": 4, "time": 4, "key": "STARTING A CONVERSATION", "student": True},
        {"id": 5, "time": 3, "key": "FOLLOWING UP", "student": True},
        {"id": 6, "time": 5, "key": "WHAT WOULD YOU SAY?", "student": False},
        {"id": 7, "time": 5, "key": "MAKING DISCIPLES", "student": True},
        {"id": 8, "time": 5, "key": "EXPLAINING YOU BELIEFS", "student": True},
        {"id": 9, "time": 5, "key": "TALK", "student": True},
        {"id": 10, "time": 15, "key": "LIVING TALK"},
        {"id": 11, "time": 30, "key": "SERVICE TALK", "name": ""}  # add "name" key
    ]

    MOCK_WEEKEND_SCHEDULE_CIRCUIT_OVERSEER = [
        {"id": 13, "time": 30, "key": "PUBLIC TALK"},
        {"id": 14, "time": 30, "key": "WATCHTOWER STUDY"},
        {"id": 15, "time": 30, "key": "CIRCUIT OVERSEER TALK", "name": ""}  # add "name" key
    ]

    def setUp(self):
        self.fixed_midweek = datetime.datetime(2026, 11, 19)
        self.fixed_weekend = datetime.datetime(2026, 11, 22)

    """
    Testing get_schedule_data_auto in 'normal mode'
    """
    @patch(f"{MODULE}.datetime.datetime")
    @patch(f"{MODULE}.get_cached_data")
    @patch(f"{MODULE}.update_schedule_data")
    def test_get_schedule_data_auto_cached_is_None_both_None(self, update_schedule_mock, cached_mock, datetime_mock):
        datetime_mock.now.return_value = self.fixed_midweek
        cached_mock.return_value = None 
        update_schedule_mock.return_value = None 

        self.assertEqual({}, get_schedule_data_auto())
        update_schedule_mock.assert_called_once()

    @patch(f"{MODULE}.datetime.datetime")
    @patch(f"{MODULE}.get_cached_data")
    @patch(f"{MODULE}.update_schedule_data")
    def test_get_schedule_data_auto_cached_is_None_midweek(self, update_schedule_mock, cached_mock, datetime_mock):
        datetime_mock.now.return_value = self.fixed_midweek
        cached_mock.return_value = None 
        update_schedule_mock.return_value = {"2026-47": self.MOCK_MIDWEEK_SCHEDULE}

        self.assertEqual(self.MOCK_MIDWEEK_SCHEDULE, get_schedule_data_auto())
        update_schedule_mock.assert_called_once()

    @patch(f"{MODULE}.datetime.datetime")
    @patch(f"{MODULE}.get_cached_data")
    @patch(f"{MODULE}.update_schedule_data")
    def test_get_schedule_data_auto_cached_is_None_weekend(self, update_schedule_mock, cached_mock, datetime_mock):
        datetime_mock.now.return_value = self.fixed_weekend
        cached_mock.return_value = None 
        update_schedule_mock.return_value = self.MOCK_WEEKEND_SCHEDULE

        self.assertEqual({"weekend": self.MOCK_WEEKEND_SCHEDULE}, get_schedule_data_auto())
        update_schedule_mock.assert_called_once()


    """
    Testing circuit overseer mode
    """
    @patch(f"{MODULE}.datetime.datetime")
    def test_circuit_overseer_mode_midweek(self, datetime_mock):
        datetime_mock.now.return_value = self.fixed_midweek
        schedule = self.MOCK_MIDWEEK_SCHEDULE.copy()
        ciruit_overseer_schedule(schedule, MockTranslation)
        self.assertEqual(self.MOCK_MIDWEEK_SCHEDULE_CIRCUIT_OVERSEER, schedule)

    @patch(f"{MODULE}.datetime.datetime")
    def test_circuit_overseer_mode_weekend(self, datetime_mock):
        datetime_mock.now.return_value = self.fixed_weekend
        schedule = deepcopy(self.MOCK_WEEKEND_SCHEDULE)
        ciruit_overseer_schedule(schedule, MockTranslation)
        self.assertEqual(self.MOCK_WEEKEND_SCHEDULE_CIRCUIT_OVERSEER, schedule)
