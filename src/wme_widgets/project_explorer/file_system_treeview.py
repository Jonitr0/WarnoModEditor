import shutil
import os

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.utils.color_manager import *
from src.dialogs import essential_dialogs
from src.wme_widgets.project_explorer import file_icon_provider, file_system_model


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
        proxy_model = file_system_model.FileSystemModel()
        proxy_model.data_model.setRootPath(mod_path)
        proxy_model.setNameFilters(["*.ndf"])
        proxy_model.data_model.setNameFilterDisables(False)
        proxy_model.data_model.setIconProvider(file_icon_provider.FileIconProvider())

        self.setModel(proxy_model)
        root_index = proxy_model.data_model.index(mod_path)
        proxy_index = proxy_model.mapFromSource(root_index)
        self.setRootIndex(proxy_index)
        self.mod_path = mod_path

        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.header().setSectionResizeMode(1, QtWidgets.QHeaderView.Fixed)
        self.header().setStretchLastSection(False)
        self.setColumnWidth(1, 80)

        self.hideColumn(2)
        self.hideColumn(3)

    def on_double_click(self, index):
        # map index to source
        file_path = self.model().get_file_path_for_index(index)
        if file_path.endswith(".ndf"):
            self.open_ndf_editor.emit(file_path)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mouseDoubleClickEvent(event)

    def on_context_menu(self, point: QtCore.QPoint):
        index = self.indexAt(point)

        file_path = self.model().get_file_path_for_index(index)
        context_menu = QtWidgets.QMenu(self)

        # .ndf context menu
        if file_path.endswith(".ndf"):
            ndf_editor_action = context_menu.addAction("Open in text editor")

        context_menu.addSeparator()
        expand_all_action = context_menu.addAction("Expand All")
        collapse_all_action = context_menu.addAction("Collapse All")

        context_menu.addSeparator()
        delete_action = context_menu.addAction("Delete")

        action = context_menu.exec_(self.mapToGlobal(point))

        # resolve
        if file_path.endswith(".ndf") and action == ndf_editor_action:
            self.open_ndf_editor.emit(file_path)
        elif action == expand_all_action:
            self.expandAll()
        elif action == collapse_all_action:
            self.collapseAll()
        elif action == delete_action:
            self.on_delete(file_path)

    def on_delete(self, file_path: str):
        if os.path.isdir(file_path):
            text = "Do you really want to delete " + file_path + " and its contents?\n" \
                                                                 "The directory will be actually deleted, not moved to the recycle bin. You will not be able to undo this!"
        else:
            text = "Do you really want to delete " + file_path + "?\n" \
                                                                 "The file will be actually deleted, not moved to the recycle bin. You will not be able to undo this!"
        dialog = essential_dialogs.ConfirmationDialog(text, "Confirm deletion")
        # return if not confirmed
        if not dialog.exec():
            return

        file_path = file_path.replace("/", "\\")

        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            os.remove(file_path)

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
