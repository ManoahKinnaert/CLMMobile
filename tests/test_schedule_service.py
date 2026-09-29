import unittest
from unittest.mock import MagicMock
import sys, pathlib

from CLMMobile.schedule_service import (
    Talk,
    TalkType,
    MeetingSection,
    assemble_schedule
)
from CLMMobile.schedule_service.schedule_service import assemble_schedule_midweek, assemble_schedule_weekend

class TestTalk(unittest.TestCase):
    def test_repr(self):
        t = Talk(TalkType.PUBLIC_TALK, MeetingSection.WEEKEND, time_limit=30)
        self.assertEqual(repr(t), "TalkType: TalkType.PUBLIC_TALK / Time limit: 30 min.")

    def test_to_dict_no_num(self):
        trans = MagicMock()
        trans.get_meeting_codes.return_value = {"OPENING_COMMENTS": "Opening comments"} 
        talk = Talk(TalkType.OPENING_COMMENTS, MeetingSection.INTRO, time_limit=1)
        d = talk.to_dict(trans)
        self.assertEqual(d["talktype"], "OPENING_COMMENTS")
        self.assertEqual(d["meeting section"], "INTRO")
        self.assertEqual(d["name"], "Opening comments ")
        self.assertEqual(d["time"], 1)

    def test_to_dict_with_num(self):
        trans = MagicMock()
        trans.get_meeting_codes.return_value = {"MINISTRY_TALK": "Ministry"}
        talk = Talk(TalkType.MINISTRY_TALK, MeetingSection.APPLY_TO_MINISTRY, time_limit=4, num=2)
        d = talk.to_dict(trans)
        self.assertEqual(d["talktype"], "MINISTRY_TALK")
        self.assertEqual(d["meeting section"], "APPLY_TO_MINISTRY")
        self.assertEqual(d["name"], "Ministry 2")
        self.assertEqual(d["time"], 4)

if __name__ == "__main__":
    unittest.main()