import unittest
import time
from unittest.mock import MagicMock

from CLMMobile.timer.timer import Timer


class DummySocketIO:
    """Minimal stand-in for flask_socketio.SocketIO used by Timer."""

    def __init__(self):
        self.background_task = None
        self.emitted = []
        self.sleep_count = 0

    def start_background_task(self, target):
        self.background_task = target

    def sleep(self, seconds):
        self.sleep_count += 1

    def emit(self, event, data, namespace):
        self.emitted.append((event, data, namespace))


class DummyDataService:
    """Minimal stand-in for CLMMobile.utils.data.DataService used by Timer."""

    def __init__(self):
        self.meeting = None
        self.added_talks = []

    def init_meeting(self):
        self.meeting = object()

    def add_talk(self, talk_type, measured_time, time_limit, sequence_number=0):
        self.added_talks.append((talk_type, measured_time, time_limit, sequence_number))


SCHEDULE = [
    {"id": 0, "key": "INTRODUCTION", "time": 1},
    {"id": 1, "key": "TREASURES TALK", "time": 10},
    {"id": 2, "key": "SPIRITUAL GEMS", "time": 10},
]


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.socket = DummySocketIO()
        self.db = DummyDataService()
        self.timer = Timer(self.socket, self.db)
        self.timer.schedule = SCHEDULE

    def test_initial_state(self):
        self.assertFalse(self.timer.running)
        self.assertIsNone(self.timer.limit)
        self.assertIsNone(self.timer.remaining)
        self.assertEqual(self.timer.over_time, 0)
        self.assertIsNone(self.timer.end_time)
        self.assertEqual(self.timer.current, 0)
        self.assertEqual(self.timer.schedule, SCHEDULE)
        self.assertIsNotNone(self.socket.background_task)

    def test_schedule_setter_copies(self):
        new_schedule = [{"id": 99, "key": "X", "time": 5}]
        self.timer.schedule = new_schedule
        self.assertEqual(self.timer.schedule, new_schedule)
        # the returned list is a copy (different list object)
        self.assertIsNot(self.timer.schedule, new_schedule)

    def test_setup_time(self):
        self.timer.current = 1
        self.timer.setup_time()
        self.assertEqual(self.timer.limit, 10 * 60)
        self.assertEqual(self.timer.remaining, 10 * 60)
        self.assertEqual(self.timer.over_time, 0)
        self.assertIsNone(self.timer.end_time)

    def test_start_sets_running(self):
        self.timer.setup_time()
        with unittest.mock.patch("CLMMobile.timer.timer.time.monotonic", return_value=1000.0):
            self.timer.start()
        self.assertTrue(self.timer.running)
        self.assertEqual(self.timer.end_time, 1000.0 + self.timer.remaining)

    def test_start_when_already_running_is_noop(self):
        self.timer.setup_time()
        self.timer.start()
        first_end_time = self.timer.end_time
        with unittest.mock.patch("CLMMobile.timer.timer.time.monotonic", return_value=9999.0):
            self.timer.start()
        self.assertEqual(self.timer.end_time, first_end_time)

    def test_stop_when_not_running_still_saves_and_advances(self):
        # stop() always persists and advances, even when not running
        self.timer.setup_time()
        self.timer.stop()
        self.assertFalse(self.timer.running)
        self.assertEqual(len(self.db.added_talks), 1)
        self.assertEqual(self.db.added_talks[0][0], SCHEDULE[0]["id"])
        self.assertEqual(self.timer.current, 1)

    def test_stop_saves_and_advances(self):
        self.timer.setup_time()
        with unittest.mock.patch("CLMMobile.timer.timer.time.monotonic", side_effect=[1000.0, 1005.0]):
            self.timer.start()
            self.timer.stop()
        self.assertFalse(self.timer.running)
        # remaining should be ~limit - 5 seconds, clamped >= 0
        self.assertGreaterEqual(self.timer.remaining, 0)
        self.assertLessEqual(self.timer.remaining, self.timer.limit)
        # db was saved and timer advanced to next talk
        self.assertEqual(len(self.db.added_talks), 1)
        self.assertEqual(self.db.added_talks[0][0], SCHEDULE[0]["id"])
        self.assertEqual(self.timer.current, 1)

    def test_next_advances_and_wraps(self):
        self.timer.setup_time()
        self.timer.next()
        self.assertEqual(self.timer.current, 1)
        self.assertEqual(self.timer.limit, SCHEDULE[1]["time"] * 60)

        self.timer.next()
        self.timer.next()
        self.assertEqual(self.timer.current, 0)  # wrapped around

    def test_next_when_running_is_noop(self):
        self.timer.setup_time()
        self.timer.running = True
        self.timer.next()
        self.assertEqual(self.timer.current, 0)

    def test_prev_goes_back(self):
        self.timer.current = 2
        self.timer.setup_time()
        self.timer.prev()
        self.assertEqual(self.timer.current, 1)

    def test_prev_at_zero_stays(self):
        self.timer.current = 0
        self.timer.prev()
        self.assertEqual(self.timer.current, 0)

    def test_prev_when_running_is_noop(self):
        self.timer.current = 2
        self.timer.running = True
        self.timer.prev()
        self.assertEqual(self.timer.current, 2)

    def test_set_current_valid(self):
        self.timer.set_current(2)
        self.assertEqual(self.timer.current, 2)
        self.assertEqual(self.timer.limit, SCHEDULE[2]["time"] * 60)

    def test_set_current_out_of_range_ignored(self):
        self.timer.set_current(-1)
        self.assertEqual(self.timer.current, 0)
        self.timer.set_current(len(SCHEDULE))
        self.assertEqual(self.timer.current, 0)

    def test_set_current_when_running_ignored(self):
        self.timer.current = 1
        self.timer.running = True
        self.timer.set_current(0)
        self.assertEqual(self.timer.current, 1)

    def test_run_emits_once_then_stops(self):
        # make socket.sleep raise so the infinite _run loop exits after one pass
        class StopSleep(Exception):
            pass

        self.socket.sleep = lambda s: (_ for _ in ()).throw(StopSleep())

        self.timer.setup_time()
        self.timer.running = True
        self.timer.end_time = time.monotonic() + 30.0
        with self.assertRaises(StopSleep):
            self.timer._run()
        self.assertEqual(len(self.socket.emitted), 2)
        self.assertEqual(self.socket.emitted[0][0], "clockdata")
        self.assertAlmostEqual(self.socket.emitted[0][1]["remaining"], 30, delta=1)
        self.assertEqual(self.socket.emitted[1][0], "webclockdata")

    def test_emit_clockdata(self):
        self.timer.setup_time()
        remaining, overtime = 42, 5
        self.timer._emit((remaining, overtime))
        self.assertEqual(len(self.socket.emitted), 2)
        self.assertEqual(self.socket.emitted[0][0], "clockdata")
        self.assertEqual(self.socket.emitted[0][1]["remaining"], 42)
        self.assertEqual(self.socket.emitted[0][1]["over_time"], 5)
        self.assertEqual(self.socket.emitted[1][0], "webclockdata")


if __name__ == "__main__":
    unittest.main()
