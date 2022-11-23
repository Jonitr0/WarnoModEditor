import logging

from PySide6 import QtGui
from PySide6.QtCore import Qt

from src.utils.color_manager import *
from src.utils.resource_loader import get_resource_path

loadedIcons = {}


def load_icon(name: str, color: COLORS):
    return QtGui.QIcon(load_pixmap(name, color))


def load_pixmap(name: str, color: COLORS):
    if loadedIcons.__contains__((name, color)):
        return loadedIcons[(name, color)]
    else:
        pixmap = QtGui.QPixmap(get_resource_path("resources/img/" + name))
        if pixmap.isNull():
            logging.warning("No icon found for " + name)
        mask = pixmap.createMaskFromColor(Qt.white, Qt.MaskOutColor)
        pixmap.fill(QtGui.QColor(get_color_for_key(color.value)))
        pixmap.setMask(mask)
        loadedIcons[(name, color)] = pixmap

        return pixmap
