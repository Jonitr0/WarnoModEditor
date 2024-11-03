# function to get resource path in standard and packaged execution

import os
import sys


def get_resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def get_persistant_path(relative_path: str):
    # get AppData path
    app_data = os.getenv("APPDATA")
    wme_path = os.path.join(app_data, "WarnoModEditor")

    if not os.path.exists(wme_path):
        os.makedirs(wme_path)

    return os.path.join(wme_path, relative_path)


def get_export_path(relative_path: str):
    # get documents path
    documents = os.path.expanduser("~\\Documents")
    export_path = os.path.join(documents, "WarnoModEditor")

    if not os.path.exists(export_path):
        os.makedirs(export_path)

    if not os.path.exists(os.path.join(export_path, "Scripts")):
        os.makedirs(os.path.join(export_path, "Scripts"))

    return os.path.join(export_path, relative_path)
