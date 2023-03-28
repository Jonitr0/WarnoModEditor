# function to get resource path in standard and packaged execution

import os
import sys
from pathlib import Path

def get_resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def get_persistant_path(relative_path: str):
    home_path = str(Path.home())
    wme_path = os.path.join(home_path, "WarnoModEditor")

    if not os.path.exists(wme_path):
        os.makedirs(wme_path)

    return os.path.join(wme_path, relative_path)
