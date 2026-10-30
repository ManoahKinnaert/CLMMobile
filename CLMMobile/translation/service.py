import json 
import pathlib
from CLMMobile.utils import TRANS_DIR
from CLMMobile.utils.settings import Settings

HOME_DIR = pathlib.Path.home().joinpath(".clmmobile")

class Translation:
    """
    For this class we assume the settings file already exists.
    The purpose of it is to get the current interface language, set the current
    interface language and get the appropriate strings associated with a section of the user interface.
    """

    def __init__(self, settings: Settings):
        self._settings = settings
        self._lang: str = self._get_language() 
        self._cached_strings: dict = {}
        self._update_cached_strings(self._lang)

    @property 
    def language(self):
        return self._lang 

    @language.setter 
    def language(self, new_lang: str):
        """
        Set the current language by identifier and update cache accordingly.
        Silently returns None if new_lang is invalid.
        """
        if not pathlib.Path(TRANS_DIR / f"{new_lang}.json").is_file() or self._lang == new_lang:
            return
        self._set_language(new_lang)
        self._update_cached_strings(new_lang)
        self._lang = new_lang

    def _get_language(self):
        """
        Get the current user interface language in the settings file.
        """
        return self._settings.get("language")

    def _set_language(self, new_lang: str):
        """
        Set the current user interface language in the settings file.
        """
        self._settings.set("language", new_lang)

    def _update_cached_strings(self, lang: str):
        """
        Update the translation string cache.
        """
        try:
            with open(pathlib.Path(TRANS_DIR / f"{lang}.json"), "r", encoding="utf-8") as translations:
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