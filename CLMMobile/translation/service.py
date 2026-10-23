import json 
import pathlib
from CLMMobile.utils import ASSETS_DIR

HOME_DIR = pathlib.Path.home().joinpath(".clmmobile")

class Translation:
    """
    For this class we assume the settings file already exists.
    The purpose of it is to get the current interface language, set the current
    interface language and get the appropriate strings associated with a section of the user interface.
    """
    TRANS_DIR = ASSETS_DIR / "translations"
    SETTINGS = HOME_DIR / "settings.json"

    def __init__(self):
        self._lang: str = self._get_language() 
        self._cached_strings: dict = {}

    @property 
    def language(self):
        return self._lang 

    @language.setter 
    def language(self, new_lang: str):
        """
        Set the current language by identifier and update cache accordingly.
        Silently returns None if new_lang is invalid.
        """
        if not pathlib.Path(self.TRANS_DIR / f"{new_lang}.json").exists() or self._lang == new_lang:
            return
        self._lang = new_lang
        self._set_language()
        self._update_cached_strings()

    def _get_language(self):
        """
        Get the current user interface language in the settings file.
        """
        try:
            with open(self.SETTINGS, "r") as settings_file:
                settings = json.load(settings_file)
            return settings["language"]
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            print(f"[ERROR]: {e}")
            return None

    def _set_language(self):
        """
        Set the current user interface language in the settings file.
        """
        try:
            with open(self.SETTINGS, "r+") as settings_file:
                settings = json.load(settings_file)
                settings["language"] = self._lang 
                json.dump(settings, settings_file, ensure_ascii=False, indent=4)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR]: {e}")

    def _update_cached_strings(self):
        """
        Update the translation string cache.
        """
        try:
            with open(pathlib.Path(self.TRANS_DIR / f"{self._lang}.json")) as translations:
                self._cached_strings = json.load(translations)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"[ERROR]: {e}")

    def get_string_section(self, section: str):
        """
        Get translation strings for a particular section of the ui.
        Silently returns None if the section doesn't exist.
        """
        if section in self._cached_strings:
            return self._cached_strings[section]