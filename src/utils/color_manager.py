from src.utils import settings_manager
from src.utils import theme_manager
from enum import Enum
import logging
import xml.etree.ElementTree as ET

colors = {
            'danger': '#dc3545',
            'warning': '#ffc107',
            'success': '#17a2b8',
}

loaded = False

class COLORS(Enum):
    PRIMARY = "primaryColor"
    PRIMARY_LIGHT = "primaryLightColor"
    SECONDARY = "secondaryColor"
    SECONDARY_LIGHT = "secondaryLightColor"
    SECONDARY_DARK = "secondaryDarkColor"
    PRIMARY_TEXT = "primaryTextColor"
    SECONDARY_TEXT = "secondaryTextColor"
    KEYWORDS = "keywordsColor"
    TYPES = "typesColor"
    NUMBERS = "numbersColor"
    STRINGS = "stringsColor"
    SINGLE_COMMENT = "singleCommentColor"
    MULTI_COMMENT = "multiCommentColor"
    FIND_HIGHLIGHT = "findHighlightColor"
    DANGER = "danger"
    WARNING = "warning"
    SUCCESS = "success"


def get_color_key(key: str):
    global loaded
    if not loaded:
        load_colors()
        loaded = True
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
    # load editor colors
    if invert_secondary:
        path = "resources/light_highlight.xml"
    else:
        path = "resources/dark_highlight.xml"
    colors_xml = ET.parse(path)
    root = colors_xml.getroot()
    for child in root:
        color_name = child.attrib['name']
        colors[color_name] = child.text
