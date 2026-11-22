import unittest 
from unittest.mock import patch
import datetime
from CLMMobile.utils.schedule_service.service import get_cached_data, update_schedule_data, get_schedule_data_auto

MODULE = "CLMMobile.utils.schedule_service.service"

class TestScheduleService(unittest.TestCase):

    MOCK_MIDWEEK_SCHEDULE = {"2026-47": [
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
    ]}

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

    def setUp(self):
        self.fixed_midweek = datetime.datetime(2026, 11, 19)
        self.fixed_weekend = datetime.datetime(2026, 11, 22)

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
    def test_get_schedule_data_auto_cached_is_None_one_None(self, update_schedule_mock, cached_mock, datetime_mock):
        datetime_mock.now.return_value = self.fixed_midweek
        cached_mock.return_value = None 
        update_schedule_mock.return_value = self.MOCK_MIDWEEK_SCHEDULE

        self.assertEqual(self.MOCK_MIDWEEK_SCHEDULE["2026-47"], get_schedule_data_auto())
        update_schedule_mock.assert_called_once()
