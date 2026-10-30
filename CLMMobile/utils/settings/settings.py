from typing import Any
import json 

from CLMMobile.utils import HOMEPATH, SETTINGS_FILE

class Settings:

    # collection of default settings
    DEFAULT = {
        "language": "en"
    }

    def __init__(self):
        if not SETTINGS_FILE.exists():
            self._create_settings()


    def get_all(self) -> Any:
        try:
            with open(SETTINGS_FILE, "r") as settings_file:
                return json.load(settings_file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR]: {e}")
            return None

    def get(self, key: str) -> Any:
        try:
            return self.get_all()[key]
        except KeyError as e:
            print(f"[ERROR]: {e}")
            return None

    def _write(self, data):
        try:
            with open(SETTINGS_FILE, "w") as settings_file:
                json.dump(data, settings_file, ensure_ascii=False, indent=4)
        except FileNotFoundError as e:
            print(f"[ERROR]: {e}")

    def set(self, key: str, val: Any):
        data = self._get_all()
        data[key] = val 
        self._write(data)

    def _create_settings(self):
        HOMEPATH.mkdir(parents=True, exist_ok=True)
        self._write(self.DEFAULT)
