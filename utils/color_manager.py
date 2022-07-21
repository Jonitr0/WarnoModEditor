from utils import theme_manager, settings_manager
from enum import Enum
import logging
import xml.etree.ElementTree as ET

colors = {}


class COLORS(Enum):
    PRIMARY = "primaryColor"
    PRIMARY_LIGHT = "primaryLightColor"
    SECONDARY = "secondaryColor"
    SECONDARY_LIGHT = "secondaryLightColor"
    SECONDARY_DARK = "secondaryDarkColor"
    PRIMARY_TEXT = "primaryTextColor"
    SECONDARY_TEXT = "secondaryTextColor"


def get_color(key: str):
    if not colors:
        load_colors()
    if not colors.__contains__(key):
        logging.warning("No color found for key " + key)
        return "#ff0000"
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
