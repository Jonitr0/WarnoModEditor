import os
import re

from src.wme_widgets import main_widget


def get_assignment_ids(file_name: str) -> [str]:
    file_name = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(), file_name)
    with open(file_name, mode="r", encoding="utf-8") as f:
        file_content = f.read()
        f.close()

    current_index = 0
    assignment_regex = re.compile("(\\w+)\\sis\\s")
    ids = []

    while True:
        res = assignment_regex.search(file_content, current_index, file_content.find("(", current_index))
        if not res:
            break
        ids.append(res.group(1))

        current_index = file_content.find("(", current_index) + 1
        level = 1
        while level > 0:
            next_open = file_content.find("(", current_index)
            next_close = file_content.find(")", current_index)
            if next_open < 0 or next_close < 0:
                break
            if next_open < next_close:
                level += 1
                current_index = next_open + 1
            else:
                level -= 1
                current_index = next_close + 1

    return ids

def get_object_range(file_name: str, obj_name: str) -> (int, int):
    file_name = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(), file_name)
    with open(file_name, mode="r", encoding="utf-8") as f:
        file_content = f.read()
        f.close()

