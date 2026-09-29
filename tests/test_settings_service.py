import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from CLMMobile.settings_service import SettingsService


class TestSettingsService(unittest.TestCase):
    def _patched_tmp(self, tmp):
        tmp_path = pathlib.Path(tmp)
        tmp_file = tmp_path / "settings.json"
        return (
            patch.object(SettingsService, "SETTINGS_FILE", tmp_file),
            patch.object(SettingsService, "HOME_PATH", tmp_path),
            tmp_file,
        )

    def test_creates_default_when_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_patch, home_patch, tmp_file = self._patched_tmp(tmp)
            with file_patch, home_patch:
                self.assertFalse(tmp_file.exists())
                svc = SettingsService()
                self.assertTrue(tmp_file.exists())
                self.assertEqual(json.loads(tmp_file.read_text()), {"language": "en"})
                self.assertEqual(svc.get_language(), "en")

    def test_get_set_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_patch, home_patch, tmp_file = self._patched_tmp(tmp)
            with file_patch, home_patch:
                tmp_file.write_text(json.dumps({"language": "en"}))
                svc = SettingsService()
                svc.set_language("fr")
                self.assertEqual(svc.get_language(), "fr")
                self.assertEqual(json.loads(tmp_file.read_text())["language"], "fr")

    def test_set_preserves_other_keys(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_patch, home_patch, tmp_file = self._patched_tmp(tmp)
            with file_patch, home_patch:
                tmp_file.write_text(json.dumps({"language": "en", "foo": 1}))
                svc = SettingsService()
                svc.set_language("nl")
                self.assertEqual(
                    json.loads(tmp_file.read_text()),
                    {"language": "nl", "foo": 1},
                )

    def test_corrupt_json_raises(self):
        with tempfile.TemporaryDirectory() as tmp:
            file_patch, home_patch, tmp_file = self._patched_tmp(tmp)
            with file_patch, home_patch:
                tmp_file.write_text("{invalid")
                svc = SettingsService.__new__(SettingsService)
                with self.assertRaises(json.JSONDecodeError):
                    svc.get_language()


if __name__ == "__main__":
    unittest.main()
