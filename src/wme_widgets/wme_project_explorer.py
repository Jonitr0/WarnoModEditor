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

    def on_find_text_changed(self, text: str):
        if text == "":
            self.model().setNameFilters(["*.ndf"])
            self.collapseAll()
        else:
            text = text.replace(".", "\\.")
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
        dir_iter = QtCore.QDirIterator(file_path)
        result = False
        while dir_iter.hasNext():
            dir = dir_iter.next()
            if dir_iter.fileInfo().isDir() and not dir.endswith("."):
                result = result | self.hasChildren(self.index(dir))
            elif dir_iter.fileInfo().isFile():
                # check each name filter
                for filter in name_filters:
                    # split name filter
                    filter_list = filter.split("*")
                    for filter_part in filter_list:
                        if not dir.__contains__(filter_part):
                            break
                    # sort out .ndfbin files
                    if not dir.endswith(filter_list[len(filter_list)-1]):
                        continue
                    # return True if at least one filter is satisfied
                    return True
        return result

