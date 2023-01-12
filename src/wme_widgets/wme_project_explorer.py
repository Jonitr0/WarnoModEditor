from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.utils import icon_manager, settings_manager
from src.utils.color_manager import *
from src.wme_widgets import wme_lineedit, main_widget


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

        # file size checkbox
        file_size_label = QtWidgets.QLabel("Show file sizes: ")
        self.file_size_checkbox = QtWidgets.QCheckBox()
        check_status = settings_manager.get_settings_value(settings_manager.SHOW_EXPLORER_FILESIZE_KEY)
        if check_status is not None:
            self.file_size_checkbox.setChecked(check_status)
        else:
            self.file_size_checkbox.setChecked(False)
        file_size_layout = QtWidgets.QHBoxLayout()
        file_size_layout.addWidget(file_size_label)
        file_size_layout.addWidget(self.file_size_checkbox)
        file_size_layout.addStretch()
        main_layout.addLayout(file_size_layout)

        self.tree_view = FileSystemTreeView(self)
        main_layout.addWidget(self.tree_view)
        self.file_size_checkbox.stateChanged.connect(self.tree_view.on_show_size_changed)

        search_bar.textChanged.connect(self.tree_view.on_find_text_changed)

    def update_model(self, mod_path: str):
        self.tree_view.update_model(mod_path)
        self.file_size_checkbox.stateChanged.emit(self.file_size_checkbox.checkState())

        main_widget.MainWidget.instance.show_loading_screen("Loading file system...")

        # load file system
        for i in range(20):
            self.tree_view.expandAll()
            QtWidgets.QApplication.processEvents()

        self.tree_view.collapseAll()

        main_widget.MainWidget.instance.hide_loading_screen()


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

        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.header().setStretchLastSection(False)
        self.setColumnWidth(1, 80)

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
        context_menu = QtWidgets.QMenu(self)

        # .ndf context menu
        if file_path.endswith(".ndf"):
            ndf_editor_action = context_menu.addAction("Open in text editor")

        context_menu.addSeparator()
        expand_all_action = context_menu.addAction("Expand All")
        collapse_all_action = context_menu.addAction("Collapse All")

        action = context_menu.exec_(self.mapToGlobal(point))

        # resolve
        if file_path.endswith(".ndf") and action == ndf_editor_action:
            self.open_ndf_editor.emit(file_path)
        elif action == expand_all_action:
            self.expandAll()
        elif action == collapse_all_action:
            self.collapseAll()

    def on_find_text_changed(self, text: str):
        if text == "":
            self.model().setNameFilters(["*.ndf"])
            self.collapseAll()
        else:
            self.model().setNameFilters(["*" + text + "*.ndf"])
            self.expandAll()

    def on_show_size_changed(self, state: int):
        if state == 0:
            self.hideColumn(1)
            settings_manager.write_settings_value(settings_manager.SHOW_EXPLORER_FILESIZE_KEY, 0)
        else:
            self.showColumn(1)
            settings_manager.write_settings_value(settings_manager.SHOW_EXPLORER_FILESIZE_KEY, 1)


class FileIconProvider(QtWidgets.QFileIconProvider):
    def icon(self, file_info):
        if isinstance(file_info, QtCore.QFileInfo):
            if file_info.fileName().endswith(".ndf"):
                return icon_manager.load_icon("text_file.png", COLORS.PRIMARY)
            elif file_info.isDir():
                return icon_manager.load_icon("dir.png", COLORS.SECONDARY_LIGHT)

        return super().icon(file_info)


# TODO (0.1.1): hide empty dirs
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
