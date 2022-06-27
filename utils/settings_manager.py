from PySide2 import QtCore

LAST_OPEN_KEY = "wme_last_open"
WARNO_PATH_KEY = "wme_warno_path"

settings = QtCore.QSettings("jonitro", "WarnoModEditor")


def get_settings_value(key: str):
    return settings.value(key)


def write_settings_value(key: str, val):
    settings.setValue(key, val)
