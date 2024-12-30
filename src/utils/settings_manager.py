import os.path

from PySide6 import QtCore

from src.utils import resource_loader

import json
import logging

LAST_OPEN_KEY = "wme_last_open"
WARNO_PATH_KEY = "wme_warno_path"
VERSION_KEY = "wme_version"
LAST_REPORTED_VERSION_KEY = "wme_last_reported_version"
THEME_KEY = "wme_theme"
NEXT_THEME_KEY = "wme_next_theme"
SHOW_EXPLORER_FILESIZE_KEY = "wme_show_explorer_filesize"
APP_STATE = "wme_app_state"
AUTO_BACKUP_FREQUENCY_KEY = "wme_auto_backup_frequency"
AUTO_BACKUP_COUNT_KEY = "wme_auto_backup_count"
LAST_AUTO_BACKUP_KEY = "wme_last_auto_backup"
MOD_STATE_CHANGED_KEY = "wme_mod_state_changed"


def get_settings_value(key: str, default=None):
    config = _open_config()
    if not config.__contains__(key):
        return default
    return config[key]


def write_settings_value(key: str, val):
    config = _open_config()
    config[key] = val
    _save_config(config)
    SettingsChangedNotifier.instance.setting_changed(key, val)


def _open_config() -> dict:
    file_path = resource_loader.get_persistant_path("wme_config.json")
    json_obj = {}

    try:
        with open(file_path, "r") as f:
            json_obj = json.load(f)
    except Exception as e:
        logging.info("Config not found or could not be opened: " + str(e))

    return json_obj


def _save_config(json_obj: dict):
    file_path = resource_loader.get_persistant_path("wme_config.json")
    json_str = json.dumps(json_obj, indent=4)

    try:
        with open(file_path, "w+") as f:
            f.write(json_str)
    except Exception as e:
        logging.info("Config could not be saved: " + str(e))


def get_current_warno_version() -> int:
    # TODO: try to load from ndf first
    warno_path = get_settings_value(WARNO_PATH_KEY)
    if not warno_path:
        logging.warning("Unable to load WARNO version path!")
        return 0
    version_path = os.path.join(warno_path, "Data", "PC")
    highest = 0
    for ver in os.listdir(version_path):
        if int(ver) > highest:
            highest = int(ver)
    return highest


class SettingsChangedNotifier(QtCore.QObject):
    instance = None
    mod_state_changed = QtCore.Signal(bool)
    app_state_saved = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        SettingsChangedNotifier.instance = self

    def setting_changed(self, key: str, val):
        if key == MOD_STATE_CHANGED_KEY:
            self.mod_state_changed.emit(bool(val))
        elif key == APP_STATE:
            self.app_state_saved.emit()
