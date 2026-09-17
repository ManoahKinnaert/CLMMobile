import json 
import pathlib

class TranslationService:
    FILE = pathlib.Path(__file__).resolve().parent.parent 
    TRANS_DIR = FILE / "assets/translations"

    def __init__(self, language: str="en"):
        self._lang = language
        self._cached_meeting_codes = None

    @property
    def language(self): return self._lang 

    @language.setter 
    def language(self, new_lang: str):
        if not pathlib.Path(str(self.TRANS_DIR / "{new_lang}.json")).exists():
            return  # we don't allow setting a language that doesn't exist
        # reset cached meeting codes
        self._cached_meeting_codes = None
        self._lang = new_lang 

    def get_lang_name(self):
        return self._get("name")

    def get_meeting_codes(self):
        if self._cached_meeting_codes is None: 
            self._cached_meeting_codes = self._get("meeting_codes")
        return self._cached_meeting_codes
    
    def _get(self, key: str):
        return self._get_all()[key]

    def _get_all(self):
        with open(self._resolve_file(), "r") as lang_file:
            return json.load(lang_file)
    
    def _resolve_file(self):
        return str(self.TRANS_DIR / f"{self._lang}.json")