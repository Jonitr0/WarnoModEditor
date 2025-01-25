import os
import shutil

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.utils.color_manager import *
from src.dialogs import essential_dialogs
from src.wme_widgets.project_explorer import file_icon_provider, file_system_model


class ItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, parent=None):
        super(ItemDelegate, self).__init__(parent)
        self.file_ending = ""

    def setEditorData(self, editor:QtWidgets.QWidget, index) -> None:
        # if index is a directory, set file ending to empty string
        path = index.model().get_file_path_for_index(index)
        if os.path.isdir(path):
            self.file_ending = ""
        else:
            self.file_ending = path.split(".")[-1]
        super(ItemDelegate, self).setEditorData(editor, index)

    def setModelData(self, editor:QtWidgets.QWidget, model:QtCore.QAbstractItemModel, index) -> None:
        # if index is a dir and the new name contains a file ending, remove it
        new_name = editor.text()
        if os.path.isdir(model.get_file_path_for_index(index)):
            if "." in new_name:
                new_name = new_name.split(".")[0]
                model.setData(index, new_name)
                return
        # otherwise make sure the new name has the correct file ending
        else:
            if not new_name.endswith(self.file_ending):
                new_name += "." + self.file_ending
                model.setData(index, new_name)
                return
        super(ItemDelegate, self).setModelData(editor, model, index)


class FileSystemTreeView(QtWidgets.QTreeView):
    open_text_editor = QtCore.Signal(str)
    open_csv_editor = QtCore.Signal(str)
    restore_backup = QtCore.Signal(str)
    image_preview = QtCore.Signal(str)
    run_script = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.doubleClicked.connect(self.on_double_click)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_context_menu)
        self.setHeaderHidden(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.setEditTriggers(QtWidgets.QAbstractItemView.EditKeyPressed)
        self.setMinimumWidth(160)
        self.mod_path = ""
        self.setIconSize(QtCore.QSize(20, 20))
        self.delete_origin = False
        self.setItemDelegate(ItemDelegate())

    def update_model(self, mod_path: str):
        proxy_model = file_system_model.FileSystemModel()
        proxy_model.set_root_path(mod_path)
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
            self.open_text_editor.emit(file_path)
        elif file_path.endswith(".csv"):
            self.open_csv_editor.emit(file_path)
        elif file_path.endswith(tuple([".png", ".jpg", ".bmp"])):
            self.image_preview.emit(file_path)
        elif file_path.endswith(".bat"):
            self.run_script.emit(os.path.basename(file_path))

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mouseDoubleClickEvent(event)

    def on_context_menu(self, point: QtCore.QPoint):
        index = self.indexAt(point)
        file_path = self.model().get_file_path_for_index(index)
        context_menu = QtWidgets.QMenu(self)

        # text file context menu
        if file_path.endswith(".ndf"):
            text_editor_action = context_menu.addAction("Open in text editor")

        if file_path.endswith(".csv"):
            csv_editor_action = context_menu.addAction("Open in CSV editor")

        if file_path.endswith(".zip") and file_path.__contains__("Backup"):
            restore_backup_action = context_menu.addAction("Restore backup")

        if file_path.endswith(tuple([".png", ".jpg", ".bmp"])):
            image_preview_action = context_menu.addAction("Preview Image")

        if file_path.endswith(".bat"):
            run_action = context_menu.addAction("Run Script")

        if os.path.isdir(file_path):
            expand_action = None
            collapse_action = None
            if self.isExpanded(index):
                collapse_action = context_menu.addAction("Collapse")
            else:
                expand_action = context_menu.addAction("Expand")

        context_menu.addSeparator()
        expand_all_action = context_menu.addAction("Expand All")
        collapse_all_action = context_menu.addAction("Collapse All")

        # if not clickd on empty space
        if file_path != "":
            context_menu.addSeparator()
            rename_action = context_menu.addAction("Rename")
            copy_action = context_menu.addAction("Copy")
            copy_action.setShortcut("Ctrl+C")
            cut_action = context_menu.addAction("Cut")
            cut_action.setShortcut("Ctrl+X")
            paste_action = context_menu.addAction("Paste")
            paste_action.setShortcut("Ctrl+V")

            context_menu.addSeparator()
            delete_action = context_menu.addAction("Delete")
            delete_action.setShortcut("Del")

        action = context_menu.exec_(self.mapToGlobal(point))

        # resolve
        if file_path.endswith(".ndf") and action == text_editor_action:
            self.open_text_editor.emit(file_path)
        elif file_path.endswith(".csv") and action == csv_editor_action:
            self.open_csv_editor.emit(file_path)
        elif file_path.endswith(".zip") and file_path.__contains__("Backup") and action == restore_backup_action:
            file_name = os.path.basename(file_path)
            self.restore_backup.emit(file_name)
        elif file_path.endswith(tuple([".png", ".jpg", ".bmp"])) and action == image_preview_action:
            self.image_preview.emit(file_path)
        elif file_path.endswith(".bat") and action == run_action:
            self.run_script.emit(os.path.basename(file_path))
        elif os.path.isdir(file_path) and action == expand_action:
            self.expand(index)
        elif os.path.isdir(file_path) and action == collapse_action:
            self.collapse(index)
        elif action == expand_all_action:
            self.expandAll()
        elif action == collapse_all_action:
            self.collapseAll()
        elif file_path != "":
            if action == rename_action:
                self.edit(index)
            elif action == copy_action:
                self.on_copy(file_path)
            elif action == cut_action:
                self.on_cut(file_path)
            elif action == paste_action:
                self.on_paste(file_path)
            elif action == delete_action:
                self.on_delete(file_path)

    def on_copy(self, file_path: str):
        mime_data = QtCore.QMimeData()
        mime_data.setUrls([QtCore.QUrl.fromLocalFile(file_path)])
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setMimeData(mime_data)
        self.delete_origin = False

    def on_cut(self, file_path: str):
        mime_data = QtCore.QMimeData()
        mime_data.setUrls([QtCore.QUrl.fromLocalFile(file_path)])
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setMimeData(mime_data)
        self.delete_origin = True

    def on_paste(self, file_path: str):
        clipboard = QtWidgets.QApplication.clipboard()
        mime_data = clipboard.mimeData()
        if mime_data.hasUrls():
            urls = mime_data.urls()
            for url in urls:
                source_path = url.toLocalFile()
                if not os.path.isdir(file_path):
                    file_path = os.path.dirname(file_path)
                target_path = os.path.join(file_path, os.path.basename(source_path))
                if os.path.exists(target_path):
                    if os.path.isdir(target_path):
                        target_path = os.path.join(file_path, os.path.basename(source_path) + "_copy")
                    else:
                        file_name = os.path.basename(source_path).split(".")[0]
                        file_ending = os.path.basename(source_path).split(".")[-1]
                        target_path = os.path.join(file_path, file_name + "_copy." + file_ending)
                if os.path.isdir(source_path):
                    if self.delete_origin:
                        shutil.move(source_path, target_path)
                    else:
                        shutil.copytree(source_path, target_path)
                else:
                    if self.delete_origin:
                        QtCore.QFile.rename(source_path, target_path)
                    else:
                        QtCore.QFile.copy(source_path, target_path)

    def on_delete(self, file_path: str):
        if os.path.isdir(file_path):
            text = "Do you really want to delete " + file_path + " and its contents?"
        else:
            text = "Do you really want to delete " + file_path + "?"
        dialog = essential_dialogs.ConfirmationDialog(text, "Confirm deletion")
        # return if not confirmed
        if not dialog.exec():
            return

        file_path = file_path.replace("/", "\\")

        if os.path.isdir(file_path):
            shutil.rmtree(file_path)
        else:
            QtCore.QFile.moveToTrash(file_path)

        settings_manager.write_settings_value(settings_manager.MOD_STATE_CHANGED_KEY, 1)

    def on_find_text_changed(self, text: str):
        if text == "":
            self.model().show_all_dirs = True
            self.model().setNameFilters([])
            self.collapseAll()
        else:
            self.model().show_all_dirs = False
            self.model().setNameFilters(["*" + text + "*"])
            self.expandAll()

    def on_show_size_changed(self, state: int):
        if state == 0:
            self.hideColumn(1)
            settings_manager.write_settings_value(settings_manager.SHOW_EXPLORER_FILESIZE_KEY, 0)
        else:
            self.showColumn(1)
            settings_manager.write_settings_value(settings_manager.SHOW_EXPLORER_FILESIZE_KEY, 1)
