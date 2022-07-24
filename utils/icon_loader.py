from PySide2 import QtGui
from PySide2.QtCore import Qt

from utils.color_manager import *

loadedIcons = {}


def load_icon(name: str, color: COLORS):
    if loadedIcons.__contains__((name, color)):
        return loadedIcons[(name, color)]
    else:
        pixmap = QtGui.QPixmap("resources/img/" + name)
        mask = pixmap.createMaskFromColor(Qt.white, Qt.MaskOutColor)
        pixmap.fill(QtGui.QColor(get_color(color.value)))
        pixmap.setMask(mask)

        icon = QtGui.QIcon(pixmap)
        loadedIcons[(name, color)] = icon
        return icon
