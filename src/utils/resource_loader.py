# function to get resource path in standard and packaged execution

import os
import sys

def get_resource_path(relative_path: str):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)