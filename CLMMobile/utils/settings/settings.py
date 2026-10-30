from typing import Any
import json 
import pathlib

class Settings:

    HOMEPATH = pathlib.Path.home().joinpath(".clmmobile")
    SETTINGS_FILE = HOMEPATH.joinpath("settings.json")
    # collection of default settings
    DEFAULT = {
        "language": "en"
    }

    def __init__(self):
        if not self.SETTINGS_FILE.exists():
            self._create_settings()


    def _get_all(self) -> Any:
        try:
            with open(self.SETTINGS_FILE, "r") as settings_file:
                return json.load(settings_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR]: {e}")
            return None

    def _get(self, key: str) -> Any:
        try:
            return self._get_all()[key]
        except KeyError as e:
            print(f"[ERROR]: {e}")
            return None

    def _write(self, data):
        try:
            with open(self.SETTINGS_FILE, "w") as settings_file:
                json.dump(data, settings_file, ensure_ascii=False, indent=4)
        except FileNotFoundError as e:
            print(f"[ERROR]: {e}")

    def _set(self, key: str, val: Any):
        data = self._get_all()
        data[key] = val 
        self._write(data)

    def _create_settings(self):
        self.HOMEPATH.mkdir(parents=True, exist_ok=True)
        self._write(self.DEFAULT)
