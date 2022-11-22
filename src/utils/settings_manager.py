from PySide6 import QtCore

LAST_OPEN_KEY = "wme_last_open"
WARNO_PATH_KEY = "wme_warno_path"
THEME_KEY = "wme_theme"
SHOW_EXPLORER_FILESIZE_KEY = "wme_show_explorer_filesize"

settings = QtCore.QSettings("jonitro", "WarnoModEditor")


def get_settings_value(key: str):
    return settings.value(key)


def write_settings_value(key: str, val):
    settings.setValue(key, val)
