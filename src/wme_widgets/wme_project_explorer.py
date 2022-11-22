from PySide6 import QtWidgets, QtCore
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
        search_bar = wme_lineedit.WMELineEdit()
        search_bar.setPlaceholderText("Find in Directory...")
        main_layout.addWidget(search_bar)

        self.tree_view = FileSystemTreeView(self)
        main_layout.addWidget(self.tree_view)

        search_bar.textChanged.connect(self.tree_view.on_find_text_changed)


class FileSystemTreeView(QtWidgets.QTreeView):
    open_ndf_editor = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.doubleClicked.connect(self.on_double_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)
        self.setHeaderHidden(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumWidth(160)
        self.mod_path = ""
        self.setIconSize(QtCore.QSize(20, 20))

    def update_model(self, mod_path: str):
        data_model = FileSystemModel()
        data_model.setRootPath(mod_path)
        data_model.setNameFilters(["*.ndf"])
        data_model.setNameFilterDisables(False)
        data_model.setIconProvider(FileIconProvider())

        self.setModel(data_model)
        self.setRootIndex(data_model.index(mod_path))
        self.mod_path = mod_path

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def on_double_click(self, index):
        # map index to source
        file_path = QtWidgets.QFileSystemModel.filePath(self.model(), index)
        if file_path.endswith(".ndf"):
            self.open_ndf_editor.emit(file_path)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mouseDoubleClickEvent(event)

    def on_context_menu(self, point: QtCore.QPoint):
        index = self.indexAt(point)

        file_path = QtWidgets.QFileSystemModel.filePath(self.model(), index)
        # .ndf context menu
        if file_path.endswith(".ndf"):
            context_menu = QtWidgets.QMenu(self)
            ndf_editor_action = context_menu.addAction("Open in text editor")

            action = context_menu.exec_(self.mapToGlobal(point))
            if action == ndf_editor_action:
                self.open_ndf_editor.emit(file_path)

    def on_find_text_changed(self, text: str):
        if text == "":
            self.model().setNameFilters(["*.ndf"])
            self.collapseAll()
        else:
            self.model().setNameFilters(["*" + text + "*.ndf"])
            self.expandRecursively(self.model().index(self.mod_path))


class FileIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, file_info):
        if isinstance(file_info, QtCore.QFileInfo):
            if file_info.fileName().endswith(".ndf"):
                return icon_manager.load_icon("file.png", COLORS.PRIMARY)
            elif file_info.isDir():
                return icon_manager.load_icon("dir.png", COLORS.SECONDARY_LIGHT)

        return super().icon(file_info)


class FileSystemModel(QtWidgets.QFileSystemModel):
    def hasChildren(self, parent) -> bool:
        # no possible children
        if parent.flags() & Qt.ItemNeverHasChildren:
            return False

        name_filters = self.nameFilters()
        # iterate through children
        file_path = QtWidgets.QFileSystemModel.filePath(self, parent)
        qdir = QtCore.QDir(file_path)
        qdir.setNameFilters(name_filters)
        dir_iter = QtCore.QDirIterator(qdir, QtCore.QDirIterator.Subdirectories)
        if dir_iter.hasNext():
            return True
        else:
            return False

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.ToolTipRole:
            return index.data()
        else:
            return super().data(index, role)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags  # 0
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ToolTip

