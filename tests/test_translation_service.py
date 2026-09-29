import unittest
from unittest.mock import MagicMock, patch

from CLMMobile.translation_service import TranslationService


def _make_svc(lang="en"):
    settings = MagicMock()
    settings.get_language.return_value = lang
    svc = TranslationService(settings)
    return svc, settings


class TestTranslationService(unittest.TestCase):
    def test_init_reads_language_from_settings(self):
        svc, _ = _make_svc("en")
        self.assertEqual(svc.language, "en")

    def test_setter_valid_clears_cache_and_persists(self):
        svc, settings = _make_svc("en")
        svc._cached_meeting_codes = {"x": 1}
        svc._cached_ui_strings = {"y": 2}
        svc.language = "fr"
        self.assertIsNone(svc._cached_meeting_codes)
        self.assertIsNone(svc._cached_ui_strings)
        self.assertEqual(svc.language, "fr")
        settings.set_language.assert_called_once_with("fr")
        # real asset content switched
        self.assertEqual(svc.get_lang_name(), "Français")
        self.assertEqual(svc.get_meeting_codes()["MEETING"], "Réunion")

    def test_setter_invalid_ignored(self):
        svc, settings = _make_svc("en")
        svc.language = "xx"
        self.assertEqual(svc.language, "en")
        settings.set_language.assert_not_called()

    def test_meeting_codes_cached(self):
        svc, _ = _make_svc("en")
        with patch.object(svc, "_get_all", wraps=svc._get_all) as spy:
            first = svc.get_meeting_codes()
            second = svc.get_meeting_codes()
        self.assertIs(first, second)
        self.assertEqual(spy.call_count, 1)
        self.assertEqual(first["MEETING"], "Meeting")
        self.assertIn("PUBLIC_TALK", first)

    def test_ui_strings_cached(self):
        svc, _ = _make_svc("en")
        with patch.object(svc, "_get_all", wraps=svc._get_all) as spy:
            first = svc.get_ui_strings()
            second = svc.get_ui_strings()
        self.assertIs(first, second)
        self.assertEqual(spy.call_count, 1)
        self.assertIn("home", first)
        self.assertEqual(first["home"]["overview-lbl"], "Overview - How to connect")

    def test_get_languages_real_dir(self):
        svc, _ = _make_svc("en")
        self.assertCountEqual(svc.get_languages(), ["en", "fr", "nl"])

    def test_get_languages_splits_extension(self):
        svc, _ = _make_svc("en")
        with patch(
            "CLMMobile.translation_service.translation_service.os.listdir",
            return_value=["en.json", "fr.json"],
        ):
            self.assertEqual(svc.get_languages(), ["en", "fr"])

    def test_missing_key_raises(self):
        svc, _ = _make_svc("en")
        with self.assertRaises(KeyError):
            svc._get("bogus")

    def test_section_codes_follow_real_content(self):
        svc_en, _ = _make_svc("en")
        svc_fr, _ = _make_svc("fr")
        svc_nl, _ = _make_svc("nl")
        self.assertEqual(
            svc_en.get_meeting_section_codes()["TREASURES_FROM_GODS_WORD"],
            "Treasures from Gods word",
        )
        self.assertEqual(
            svc_fr.get_meeting_section_codes()["TREASURES_FROM_GODS_WORD"],
            "Joyaux de la parole de dieu",
        )
        self.assertEqual(
            svc_nl.get_meeting_section_codes()["TREASURES_FROM_GODS_WORD"],
            "Schatten uit Gods woord",
        )


if __name__ == "__main__":
    unittest.main()
