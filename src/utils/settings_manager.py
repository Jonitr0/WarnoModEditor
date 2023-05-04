from src.utils import resource_loader

import json
import logging

# TODO: some of this can be saved in the config
LAST_OPEN_KEY = "wme_last_open"
WARNO_PATH_KEY = "wme_warno_path"
VERSION_KEY = "wme_version"
THEME_KEY = "wme_theme"
SHOW_EXPLORER_FILESIZE_KEY = "wme_show_explorer_filesize"
APP_STATE = "wme_app_state"


def get_settings_value(key: str, default=None):
    config = _open_config()
    if not config.__contains__(key):
        return default
    return config[key]


def write_settings_value(key: str, val):
    config = _open_config()
    config[key] = val
    _save_config(config)


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
    json_str = json.dumps(json_obj)

    try:
        with open(file_path, "w+") as f:
            f.write(json_str)
    except Exception as e:
        logging.info("Config could not be saved: " + str(e))
