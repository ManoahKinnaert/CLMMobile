import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from CLMMobile.utils.settings import Settings
from CLMMobile.utils.translation import Translation
from CLMMobile.utils.reports.generator import Generator


class TestGeneratorCircuitOverseer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        settings = Settings()
        settings.set("language", "en")
        cls.trans = Translation(settings)
        cls.gen = Generator(cls.trans)

    def test_cbs_becomes_service_talk_under_co(self):
        name = self.gen._talk_name(11, "living as christians", circuit_overseer=True)
        self.assertEqual(name, "Service Talk")

    def test_circuit_overseer_talk_in_weekend_under_co(self):
        name = self.gen._talk_name(15, "weekend", circuit_overseer=True)
        self.assertEqual(name, "Circuit Overseer Talk")

    def test_cbs_stays_cbs_without_co(self):
        name = self.gen._talk_name(11, "living as christians", circuit_overseer=False)
        self.assertEqual(name, "Congregation Bible Study")

    def test_no_co_flag_defaults_to_false(self):
        name = self.gen._talk_name(11, "living as christians")
        self.assertEqual(name, "Congregation Bible Study")
