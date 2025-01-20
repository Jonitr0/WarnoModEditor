import os

import ndf_parse as ndf
from ndf_parse.printer import string as ndf_string
from ndf_parse import convert

# TODO: cache this in a file
loaded_files = {}
load_times = {}


def parsed_list_to_py_list(parsed_list: ndf.model.List, d_type=str):
    py_list = []
    for entry in parsed_list.value:
        py_list.append(d_type(entry.value))
    return py_list


def py_list_to_parsed_list(py_list: list):
    parsed_list = ndf.model.List()
    for val in py_list:
        expr = ndf.expression(str(val))
        parsed_list.add(**expr)
    return parsed_list


def parsed_map_to_py_map(parsed_map: ndf.model.Map, d_type_keys=str, d_type_values=str):
    py_map = {}
    for pair in parsed_map:
        py_map[d_type_keys(pair.key)] = d_type_values(pair.value)
    return py_map


def py_map_to_parsed_map(py_map: dict):
    parsed_map = ndf.model.Map()
    for key in py_map.keys():
        pair_str = "(" + str(key) + "," + str(py_map[key]) + ")"
        expr = ndf.expression(pair_str)
        parsed_map.add(key=str(key), value=str(py_map[key]))
    return parsed_map


def round_trip(ndf_text: str):
    return ndf_string(convert(ndf_text))


def get_parsed_ndf_file(file_path: str):
    if file_path in loaded_files and file_path in load_times and load_times[file_path] >= os.path.getmtime(file_path):
        return loaded_files[file_path]
    else:
        with open(file_path, "r") as file:
            ndf_obj = convert(file.read())
            loaded_files[file_path] = ndf_obj
            load_times[file_path] = os.path.getmtime(file_path)
            return ndf_obj


def save_files_to_mod(files_to_objs: dict, mod_path: str):
    for file in files_to_objs.keys():
        text = get_text_from_ndf_obj(files_to_objs[file])
        file_path = os.path.join(mod_path, file)
        with open(file_path, "w") as f:
            f.write(text)
        loaded_files[file_path] = files_to_objs[file]
        load_times[file_path] = os.path.getmtime(file_path)


def get_text_from_ndf_obj(obj):
    return ndf_string(obj)
