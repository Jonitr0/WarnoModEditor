from PySide6 import QtWidgets, QtCore

from src.utils import icon_manager
from src.utils.color_manager import *

class FileIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, file_info):
        if isinstance(file_info, QtCore.QFileInfo):
            if file_info.fileName().endswith(".ndf"):
                return icon_manager.load_icon("text_file.png", COLORS.PRIMARY)
            elif file_info.isDir():
                return icon_manager.load_icon("dir.png", COLORS.SECONDARY_LIGHT)

        return super().icon(file_info)