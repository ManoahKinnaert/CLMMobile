import unittest
from unittest.mock import MagicMock, patch
import datetime as real_datetime
import json
import pathlib
import tempfile

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


class TestAssembleWeekend(unittest.TestCase):
    def test_fixed_schedule(self):
        talks = assemble_schedule_weekend()
        self.assertEqual(len(talks), 2)
        self.assertEqual(talks[0].talk_type, TalkType.PUBLIC_TALK)
        self.assertEqual(talks[0].time_limit, 30)
        self.assertEqual(talks[1].talk_type, TalkType.WATCHTOWER_STUDY)
        self.assertEqual(talks[1].time_limit, 60)


class TestAssembleMidweek(unittest.TestCase):
    @patch("CLMMobile.schedule_service.schedule_service.get_schedule_data_auto")
    def test_branch_and_counters(self, mock_feed):
        mock_feed.return_value = [
            {"talkType": 100, "minutes": 4},
            {"talkType": 199, "minutes": 5},
            {"talkType": 200, "minutes": 8},
        ]
        talks = assemble_schedule_midweek()
        self.assertEqual(len(talks), 4 + 3 + 2)
        # ministry talks: talkType // 100 == 1
        self.assertEqual(talks[4].talk_type, TalkType.MINISTRY_TALK)
        self.assertEqual(talks[4].meeting_section, MeetingSection.APPLY_TO_MINISTRY)
        self.assertEqual(talks[4].num, 1)
        self.assertEqual(talks[4].time_limit, 4)
        self.assertEqual(talks[5].talk_type, TalkType.MINISTRY_TALK)
        self.assertEqual(talks[5].num, 2)
        # living talks: everything else
        self.assertEqual(talks[6].talk_type, TalkType.LIVING_TALK)
        self.assertEqual(talks[6].meeting_section, MeetingSection.LIVING_AS_CHRISTIANS)
        self.assertEqual(talks[6].num, 1)
        self.assertEqual(talks[6].time_limit, 8)

    @patch("CLMMobile.schedule_service.schedule_service.get_schedule_data_auto")
    def test_empty_feed(self, mock_feed):
        mock_feed.return_value = []
        talks = assemble_schedule_midweek()
        self.assertEqual(len(talks), 6)
        self.assertEqual(talks[0].talk_type, TalkType.OPENING_COMMENTS)
        self.assertEqual(talks[-2].talk_type, TalkType.CONGREGATION_BIBLE_STUDY)
        self.assertEqual(talks[-2].time_limit, 30)
        self.assertEqual(talks[-1].talk_type, TalkType.CLOSING_COMMENTS)
        self.assertEqual(talks[-1].time_limit, 3)

    @patch("CLMMobile.schedule_service.schedule_service.get_schedule_data_auto")
    def test_boundary_99_vs_100(self, mock_feed):
        mock_feed.return_value = [
            {"talkType": 99, "minutes": 4},
            {"talkType": 100, "minutes": 5},
        ]
        talks = assemble_schedule_midweek()
        self.assertEqual(talks[4].talk_type, TalkType.LIVING_TALK)
        self.assertEqual(talks[5].talk_type, TalkType.MINISTRY_TALK)


class TestAssembleSchedule(unittest.TestCase):
    @patch("CLMMobile.schedule_service.schedule_service.assemble_schedule_weekend")
    @patch("CLMMobile.schedule_service.schedule_service.assemble_schedule_midweek")
    @patch("CLMMobile.schedule_service.schedule_service.datetime")
    def test_weekend_routing(self, mock_dt, mock_mid, mock_end):
        mock_dt.datetime.now.return_value.isocalendar.return_value = (2026, 40, 6)
        assemble_schedule()
        mock_end.assert_called_once()
        mock_mid.assert_not_called()

    @patch("CLMMobile.schedule_service.schedule_service.assemble_schedule_weekend")
    @patch("CLMMobile.schedule_service.schedule_service.assemble_schedule_midweek")
    @patch("CLMMobile.schedule_service.schedule_service.datetime")
    def test_midweek_routing(self, mock_dt, mock_mid, mock_end):
        mock_dt.datetime.now.return_value.isocalendar.return_value = (2026, 40, 3)
        assemble_schedule()
        mock_mid.assert_called_once()
        mock_end.assert_not_called()


class TestFeedIO(unittest.TestCase):
    def _mock_datetime(self, mock_dt, year, week, dow):
        mock_dt.datetime.now.return_value.isocalendar.return_value = (year, week, dow)
        mock_dt.datetime.fromisoformat.side_effect = lambda s: real_datetime.datetime.fromisoformat(s)

    @patch("CLMMobile.schedule_service.schedule_service.urllib.request.urlopen")
    def test_update_success(self, mock_urlopen):
        import CLMMobile.schedule_service.schedule_service as svc
        payload = [{"date": "2026-09-29T00:00:00", "talks": []}]
        mock_resp = MagicMock()
        mock_resp.read.return_value = json.dumps(payload).encode()
        mock_urlopen.return_value = mock_resp
        with tempfile.TemporaryDirectory() as tmp:
            tmp_feed = pathlib.Path(tmp) / "feed" / "meetingfeed.json"
            with patch.object(svc, "FEED_PATH", tmp_feed):
                from CLMMobile.schedule_service.schedule_service import update_schedule_data_auto
                self.assertEqual(update_schedule_data_auto(), payload)
                self.assertEqual(json.loads(tmp_feed.read_text()), payload)

    @patch("CLMMobile.schedule_service.schedule_service.urllib.request.urlopen")
    def test_update_failure_returns_none(self, mock_urlopen):
        import CLMMobile.schedule_service.schedule_service as svc
        mock_urlopen.side_effect = Exception("net down")
        with tempfile.TemporaryDirectory() as tmp:
            tmp_feed = pathlib.Path(tmp) / "feed" / "meetingfeed.json"
            with patch.object(svc, "FEED_PATH", tmp_feed):
                from CLMMobile.schedule_service.schedule_service import update_schedule_data_auto
                self.assertIsNone(update_schedule_data_auto())

    @patch("CLMMobile.schedule_service.schedule_service.update_schedule_data_auto")
    @patch("CLMMobile.schedule_service.schedule_service.datetime")
    def test_get_returns_relevant_week_no_update(self, mock_dt, mock_update):
        import CLMMobile.schedule_service.schedule_service as svc
        self._mock_datetime(mock_dt, 2026, 40, 2)  # Tue week 40
        feed = [
            {"date": "2026-09-29T00:00:00", "talks": [{"talkType": 100, "minutes": 4}]},
            {"date": "2026-10-05T00:00:00", "talks": [{"talkType": 200, "minutes": 8}]},
        ]  # latest = week 41 -> 40 >= 41 False -> no update
        with tempfile.TemporaryDirectory() as tmp:
            tmp_feed = pathlib.Path(tmp) / "meetingfeed.json"
            tmp_feed.write_text(json.dumps(feed))
            with patch.object(svc, "FEED_PATH", tmp_feed):
                from CLMMobile.schedule_service.schedule_service import get_schedule_data_auto
                self.assertEqual(get_schedule_data_auto(), [{"talkType": 100, "minutes": 4}])
                mock_update.assert_not_called()

    @patch("CLMMobile.schedule_service.schedule_service.update_schedule_data_auto")
    @patch("CLMMobile.schedule_service.schedule_service.datetime")
    def test_get_stale_cache_triggers_update(self, mock_dt, mock_update):
        import CLMMobile.schedule_service.schedule_service as svc
        self._mock_datetime(mock_dt, 2026, 42, 1)  # Mon week 42
        feed = [
            {"date": "2026-09-29T00:00:00", "talks": [{"talkType": 100, "minutes": 4}]},
            {"date": "2026-10-12T00:00:00", "talks": [{"talkType": 200, "minutes": 8}]},
        ]  # latest = week 42 -> 42 >= 42 True -> update
        with tempfile.TemporaryDirectory() as tmp:
            tmp_feed = pathlib.Path(tmp) / "meetingfeed.json"
            tmp_feed.write_text(json.dumps(feed))
            with patch.object(svc, "FEED_PATH", tmp_feed):
                from CLMMobile.schedule_service.schedule_service import get_schedule_data_auto
                self.assertEqual(get_schedule_data_auto(), [{"talkType": 200, "minutes": 8}])
                mock_update.assert_called_once()

if __name__ == "__main__":
    unittest.main()