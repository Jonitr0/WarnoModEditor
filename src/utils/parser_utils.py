import ndf_parse as ndf
from ndf_parse.printer import string as ndf_string
from ndf_parse import convert


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
