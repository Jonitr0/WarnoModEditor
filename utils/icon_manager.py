import logging

from PySide2 import QtGui
from PySide2.QtCore import Qt

from utils.color_manager import *

loadedIcons = {}


def load_icon(name: str, color: COLORS):
    return QtGui.QIcon(load_pixmap(name, color))


def load_pixmap(name: str, color: COLORS):
    if loadedIcons.__contains__((name, color)):
        return loadedIcons[(name, color)]
    else:
        pixmap = QtGui.QPixmap("resources/img/" + name)
        if pixmap.isNull():
            logging.warning("No icon found for " + name)
        mask = pixmap.createMaskFromColor(Qt.white, Qt.MaskOutColor)
        pixmap.fill(QtGui.QColor(get_color_key(color.value)))
        pixmap.setMask(mask)
        loadedIcons[(name, color)] = pixmap

        return pixmap
