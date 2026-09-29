import json 
import pathlib
import os 

from CLMMobile.settings_service import SettingsService

class TranslationService:
    FILE = pathlib.Path(__file__).resolve().parent.parent 
    TRANS_DIR = FILE / "assets/translations"

    def __init__(self, settings_service: SettingsService):
        self._settings_service: SettingsService = settings_service
        self._lang: str = self._settings_service.get_language()
        self._cached_meeting_codes: dict = None
        self._cached_ui_strings: dict = None

    @property
    def language(self): 
        return self._lang 

    @language.setter 
    def language(self, new_lang: str):
        if not pathlib.Path(str(self.TRANS_DIR / f"{new_lang}.json")).exists():
            return  # we don't allow setting a language that doesn't exist
        # reset cached meeting codes
        self._cached_meeting_codes = None
        self._cached_ui_strings = None
        self._lang = new_lang 
        self._settings_service.set_language(new_lang)

    def get_lang_name(self):
        return self._get("name")

    def get_languages(self):
        return [lang.split(".")[0] for lang in os.listdir(str(self.TRANS_DIR))]

    def get_meeting_codes(self):
        if self._cached_meeting_codes is None: 
            self._cached_meeting_codes = self._get("meeting_codes")
        return self._cached_meeting_codes

    def get_meeting_section_codes(self):
        return self._get("meeting_section_codes")

    def get_ui_strings(self):
        if self._cached_ui_strings is None:
            self._cached_ui_strings = self._get("ui")
        return self._cached_ui_strings
    
    def _get(self, key: str):
        return self._get_all()[key]

    def _get_all(self):
        with open(self._resolve_file(), "r") as lang_file:
            return json.load(lang_file)
    
    def _resolve_file(self):
        return str(self.TRANS_DIR / f"{self._lang}.json")

if __name__ == "__main__":
    trans = TranslationService()
    print(trans.get_languages())