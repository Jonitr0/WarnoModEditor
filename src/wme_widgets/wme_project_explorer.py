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
        self.search_bar = wme_lineedit.WMELineEdit()
        self.search_bar.setPlaceholderText("Find in Directory...")
        main_layout.addWidget(self.search_bar)

        self.tree_view = FileSystemTreeView(self)
        main_layout.addWidget(self.tree_view)

        self.search_bar.returnPressed.connect(lambda: self.tree_view.on_find_text_changed(self.search_bar.text()))


class FileSystemTreeView(QtWidgets.QTreeView):
    open_ndf_editor = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.doubleClicked.connect(self.on_double_click)
        self.setHeaderHidden(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumWidth(160)

    def update_model(self, mod_path: str):
        data_model = DirProxy(mod_path)
        self.setModel(data_model)
        self.setRootIndex(data_model.get_root_index())

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def on_double_click(self, index):
        # map index to source
        source_index = self.model().mapToSource(index)
        file_path = QtWidgets.QFileSystemModel.filePath(self.model().dirModel, source_index)
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
            self.model().setNameFilters(["*" + text + "*.ndf"])
            self.expandToDepth(10)


class FileIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, file_info):
        if isinstance(file_info, QtCore.QFileInfo):
            if file_info.fileName().endswith(".ndf"):
                return icon_manager.load_icon("file.png", COLORS.PRIMARY)
            elif file_info.isDir():
                return icon_manager.load_icon("dir.png", COLORS.SECONDARY_LIGHT)

        return super().icon(file_info)


# from: https://stackoverflow.com/questions/38609516/hide-empty-parent-folders-qtreeview-qfilesystemmodel
class DirProxy(QtCore.QSortFilterProxyModel):
    nameFilters = ["*.ndf"]
    mod_path = ''

    def __init__(self, mod_path: str):
        super().__init__()
        self.dirModel = QtWidgets.QFileSystemModel()
        self.dirModel.setFilter(
            QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs | QtCore.QDir.Files)
        self.dirModel.setRootPath(mod_path)
        self.dirModel.setNameFilterDisables(False)
        self.dirModel.setIconProvider(FileIconProvider())
        self.setSourceModel(self.dirModel)
        self.mod_path = mod_path

    def get_root_index(self):
        return self.mapFromSource(self.dirModel.index(self.mod_path))

    def setNameFilters(self, filters):
        if not isinstance(filters, (tuple, list)):
            filters = [filters]
        self.nameFilters = filters
        self.invalidateFilter()

    def hasChildren(self, parent):
        sourceParent = self.mapToSource(parent)
        if not self.dirModel.hasChildren(sourceParent):
            return False
        qdir = QtCore.QDir(self.dirModel.filePath(sourceParent))
        return bool(qdir.entryInfoList(qdir.NoDotAndDotDot | qdir.AllEntries | qdir.AllDirs))

    def filterAcceptsRow(self, row, parent):
        source = self.dirModel.index(row, 0, parent)
        if source.isValid():
            if self.dirModel.isDir(source):
                qdir = QtCore.QDir(self.dirModel.filePath(source))
                if self.nameFilters:
                    qdir.setNameFilters(self.nameFilters)
                return self.contains_filter_file(qdir)

            elif self.nameFilters:  # <- index refers to a file
                qdir = QtCore.QDir(self.dirModel.filePath(source))
                return qdir.match(self.nameFilters,
                                  self.dirModel.fileName(source))  # <- returns true if the file matches the nameFilters
        return True

    def contains_filter_file(self, qdir: QtCore.QDir) -> bool:
        qdir_iter = QtCore.QDirIterator(qdir, QtCore.QDirIterator.Subdirectories)
        if qdir_iter.hasNext():
            return True
        else:
            return False


