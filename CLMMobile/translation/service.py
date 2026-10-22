import json 
import pathlib
from CLMMobile.utils import ASSETS_DIR

HOME_DIR = pathlib.Path.home().joinpath(".clmmobile")

class Translation:
    TRANS_DIR = ASSETS_DIR / "translations"
    SETTINGS = HOME_DIR / "settings.json"

    def __init__(self):
        self._lang: str = self._get_language() 

    @property 
    def language(self):
        return self._lang 

    @language.setter 
    def language(self, new_lang: str):
        if not pathlib.Path(self.TRANS_DIR / f"{new_lang}.json").exists():
            return
        self._lang = new_lang
        self._set_language()

    def _get_language(self):
        with open(self.SETTINGS, "r") as settings_file:
            settings = json.load(settings_file)
        return settings["language"]

    def _set_language(self):
        with open(self.SETTINGS, "rw") as settings_file:
            settings = json.load(settings_file)
            settings["language"] = self._lang 
            json.dump(settings, settings_file, ensure_ascii=False, indent=4)