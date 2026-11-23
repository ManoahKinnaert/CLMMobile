import unittest
from unittest.mock import patch

from CLMMobile.utils.settings import Settings

MODULE = "CLMMobile.utils.settings"

class TestSettings(unittest.TestCase):
    def setUp(self):
        return super().setUp()

    @patch("pathlib.Path.exists")
    @patch(f"{MODULE}.Settings._create_settings")
    def test_init_settings_does_not_exist_create_settings_called(self, create_settings, path_exists):
        path_exists.return_value = False
        create_settings.return_value = None
        Settings()
        create_settings.assert_called_once()

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    @patch(f"{MODULE}.Settings._write")
    def test_init_settings_does_not_exist_mk_path_called(self, write, mk_path, path_exists):
        path_exists.return_value = False
        mk_path.return_value = None 
        write.return_value = None
        Settings()
        mk_path.assert_called_once()

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    @patch(f"{MODULE}.Settings._write")
    def test_init_settings_does_not_exist_write_called(self, write, mk_path, path_exists):
        path_exists.return_value = False
        mk_path.return_value = None 
        write.return_value = None
        Settings()
        write.assert_called_once()

    @patch("pathlib.Path.exists")
    @patch("pathlib.Path.mkdir")
    @patch(f"{MODULE}.Settings._write")
    def test_init_settings_does_not_exist_write_args(self, write, mk_path, path_exists):
        path_exists.return_value = False
        mk_path.return_value = None 
        write.return_value = None
        Settings()
        expected = Settings.DEFAULT
        args = write.call_args[0][0]
        self.assertEqual(expected, args)

    @patch("pathlib.Path.exists")
    @patch(f"{MODULE}.Settings._create_settings")
    def test_init_settings_does_exist(self, create_settings, path_exists):
        path_exists.return_value = True
        create_settings.return_value = None
        Settings()
        create_settings.assert_not_called()