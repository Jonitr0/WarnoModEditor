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
        self.setHeaderHidden(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumWidth(160)
        self.mod_path = ""

    def update_model(self, mod_path: str):
        data_model = QtWidgets.QFileSystemModel()
        data_model.setRootPath(mod_path)
        data_model.setNameFilters(["*.ndf"])
        data_model.setNameFilterDisables(False)
        data_model.setFilter(QtCore.QDir.Files | QtCore.QDir.Dirs)
        data_model.setIconProvider(FileIconProvider())

        #proxy_model = QtCore.QSortFilterProxyModel()
        #proxy_model.setSourceModel(data_model)
        #proxy_model.setRecursiveFilteringEnabled(True)
        # TODO: make this filter stuff

        #self.setModel(proxy_model)
        self.setModel(data_model)
        #root_index = proxy_model.mapFromSource(data_model.index(mod_path))
        #self.setRootIndex(root_index)
        self.setRootIndex(data_model.index(mod_path))
        self.mod_path = mod_path

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def on_double_click(self, index):
        # map index to source
        index = self.model().mapToSource(index)
        #file_path = QtWidgets.QFileSystemModel.filePath(self.model().sourceModel(), index)
        file_path = QtWidgets.QFileSystemModel.filePath(self.model(), index)
        if file_path.endswith(".ndf"):
            self.open_ndf_editor.emit(file_path)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mouseDoubleClickEvent(event)

    def on_find_text_changed(self, text: str):
        if text == "":
            self.model().setNameFilters(["*.ndf"])
            self.collapseAll()
        else:
            text = text.replace(".", "\\.")
            self.model().setNameFilters(["*" + text + "*.ndf"])
            self.expandRecursively(self.model().index(self.mod_path))

        #reg_exp = QtCore.QRegularExpression(text, QtCore.QRegularExpression.CaseInsensitiveOption)
        #self.model().setFilterRegularExpression(reg_exp)


class FileIconProvider(QtWidgets.QFileIconProvider):

    def icon(self, file_info):
        if isinstance(file_info, QtCore.QFileInfo):
            if file_info.fileName().endswith(".ndf"):
                return icon_manager.load_icon("file.png", COLORS.PRIMARY)
            elif file_info.isDir():
                return icon_manager.load_icon("dir.png", COLORS.SECONDARY_LIGHT)

        return super().icon(file_info)
