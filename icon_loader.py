from PySide2 import QtGui, QtCore

loadedIcons = {}


def load_icon(name: str, size: int = 32):
    if loadedIcons.__contains__(name):
        return loadedIcons[name]
    else:
        icon = QtGui.QIcon()
        icon.addFile("resources/img/" + name, QtCore.QSize(size, size))
        loadedIcons[name] = icon
        return icon
