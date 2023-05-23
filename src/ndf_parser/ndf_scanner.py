import logging
import os
import re

from src.wme_widgets import main_widget


def get_assignment_ids(file_name: str) -> [str]:
    file_name = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(), file_name)
    with open(file_name, mode="r", encoding="utf-8") as f:
        file_content = f.read()

    current_index = 0
    assignment_regex = re.compile("(\\w+)\\sis\\s")
    ids = []

    while True:
        res = assignment_regex.search(file_content, current_index, file_content.find("(", current_index))
        if not res:
            break
        ids.append(res.group(1))

        current_index = traverse_object(file_content, current_index)

    return ids


# get start and end index of a given top level object in an NDF file
def get_object_range(file_name: str, obj_name: str) -> (str, int, int):
    file_name = os.path.join(main_widget.MainWidget.instance.get_loaded_mod_path(), file_name)
    with open(file_name, mode="r", encoding="utf-8") as f:
        file_content = f.read()

    try:
        start = file_content.index(obj_name)
    except Exception as e:
        logging.warning("Object " + obj_name + " not found in " + file_name + ": " + str(e))
        return -1, -1

    end = traverse_object(file_content, start)
    return file_content[start:end], start, end


# walk over an ndf object, return end index
def traverse_object(file_content: str, current_index: int) -> int:
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
    return current_index
