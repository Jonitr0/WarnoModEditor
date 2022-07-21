from PySide2 import QtGui
from utils import theme_manager, settings_manager
import logging
import xml.etree.ElementTree as ET

colors = {}


def get_color(key: str):
    if not colors:
        load_colors()
    if not colors.__contains__(key):
        logging.warning("No color found for key " + key)
        return QtGui.QColor.red
    return colors[key]


def load_colors():
    theme_name = settings_manager.get_settings_value(settings_manager.THEME_KEY)
    path, invert_secondary = theme_manager.get_theme_file(theme_name)
    colors_xml = ET.parse(path)
    root = colors_xml.getroot()
    for child in root:
        color_name = child.attrib['name']
        if invert_secondary and color_name == 'secondaryLightColor':
            colors['secondaryDarkColor'] = child.text
        elif invert_secondary and color_name == 'secondaryDarkColor':
            colors['secondaryLightColor'] = child.text
        else:
            colors[color_name] = child.text

