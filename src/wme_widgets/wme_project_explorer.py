from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.utils import icon_manager
from src.utils.color_manager import *
from src.wme_widgets import wme_lineedit


class WMEProjectExplorer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # create minimalistic search bar
        search_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(search_layout)
        search_bar = wme_lineedit.WMELineEdit()
        search_bar.setPlaceholderText("Find in Directory...")
        search_layout.addWidget(search_bar)

        search_icon = QtGui.QIcon()
        search_icon.addPixmap(icon_manager.load_pixmap("magnify.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        search_icon.addPixmap(icon_manager.load_pixmap("magnify.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        search_button = QtWidgets.QToolButton()
        search_button.setIcon(search_icon)
        search_button.setToolTip("Find Files")
        search_button.setFixedSize(32, 32)
        search_layout.addWidget(search_button)

        self.tree_view = FileSystemTreeView(self)
        main_layout.addWidget(self.tree_view)


class FileSystemTreeView(QtWidgets.QTreeView):
    open_ndf_editor = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.doubleClicked.connect(self.on_double_click)
        self.setHeaderHidden(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumWidth(160)

    def update_model(self, mod_path: str):
        data_model = QtWidgets.QFileSystemModel()
        data_model.setRootPath(mod_path)
        data_model.setNameFilters(["*.ndf"])
        data_model.setNameFilterDisables(False)
        data_model.setIconProvider(FileIconProvider())

        self.setModel(data_model)
        self.setRootIndex(data_model.index(mod_path))

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def on_double_click(self, index):
        file_path = QtWidgets.QFileSystemModel.filePath(self.model(), index)
        if file_path.endswith(".ndf"):
            self.open_ndf_editor.emit(file_path)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mouseDoubleClickEvent(event)


class FileIconProvider(QtWidgets.QFileIconProvider):

    def icon(self, file_info):
        if isinstance(file_info, QtCore.QFileInfo):
            if file_info.fileName().endswith(".ndf"):
                return icon_manager.load_icon("file.png", COLORS.PRIMARY)
            elif file_info.isDir():
                return icon_manager.load_icon("dir.png", COLORS.SECONDARY_LIGHT)

        return super().icon(file_info)
