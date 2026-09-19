import json 
import pathlib
from typing import Any

class SettingsService:
    HOME_PATH = pathlib.Path.home().joinpath(".clmtimer")
    SETTINGS_FILE = HOME_PATH.joinpath("settings.json") 
    # collection of default settings, will be updated in the future
    DEFAULT = {
        "language": "en"
    }

    def __init__(self):
        # check if the settings file exists, if it doesn't we want to create it...
        if not self.SETTINGS_FILE.exists():
            self._create_settings()


    def get_language(self) -> str:
        return self._get("language")

    def set_language(self, lang: str):
        self._set("language", lang)

    def _create_settings(self):
        self.SETTINGS_FILE.touch()
        self._write(self.DEFAULT)

    def _get(self, key: str) -> Any:
        return self._get_all()[key]

    def _get_all(self) -> Any:
        with open(self.SETTINGS_FILE, "r") as settings_file:
            return json.load(settings_file) 

    def _set(self, key: str, val: Any):
        data = self._get_all()
        data[key] = val 
        self._write(data)

    def _write(self, data):
        with open(self.SETTINGS_FILE, "w") as settings_file:
            json.dump(data, settings_file, ensure_ascii=False, indent=4)
        