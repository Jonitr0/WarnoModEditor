import logging
import os.path

from PySide6 import QtWidgets, QtCore, QtGui

from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages.text_editor_page import wme_find_replace_bar, wme_code_editor
from src.dialogs import essential_dialogs

from src.utils import icon_manager
from src.utils.color_manager import *


class NdfEditorPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        self.find_bar = wme_find_replace_bar.FindBar()
        self.replace_bar = wme_find_replace_bar.ReplaceBar()
        self.code_editor = wme_code_editor.WMECodeEditor()
        self.help_file_path = "Help_NdfEditor.html"
        self.setup_ui()

    def setup_ui(self):
        # TODO: add zoom
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        new_action = tool_bar.addAction(icon_manager.load_icon("file.png", COLORS.PRIMARY), "New (Ctrl + N)")
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.on_new)

        open_action = tool_bar.addAction(icon_manager.load_icon("open.png", COLORS.PRIMARY), "Open (Ctrl + O)")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open)

        save_action = tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        save_as_action = tool_bar.addAction(icon_manager.load_icon("save_as.png", COLORS.PRIMARY),
                                            "Save As (Ctrl + Shift+ S)")
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.on_save_as)

        self.restore_action = tool_bar.addAction(icon_manager.load_icon("restore.png", COLORS.PRIMARY),
                                                 "Reload File (F5)")
        self.restore_action.setShortcut("F5")
        self.restore_action.setEnabled(False)
        self.restore_action.triggered.connect(self.on_restore)

        tool_bar.addSeparator()

        undo_icon = QtGui.QIcon()
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.undo_action = tool_bar.addAction(undo_icon, "Undo (Ctrl + Z)")
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setDisabled(True)
        self.undo_action.triggered.connect(self.on_undo)

        redo_icon = QtGui.QIcon()
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.redo_action = tool_bar.addAction(redo_icon, "Redo (Ctrl + Y)")
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setDisabled(True)
        self.redo_action.triggered.connect(self.on_redo)

        tool_bar.addSeparator()

        self.find_action = tool_bar.addAction(icon_manager.load_icon("magnify.png", COLORS.PRIMARY), "Find (Ctrl + F)")
        self.find_action.setShortcut("Ctrl+F")
        self.find_action.setCheckable(True)
        self.find_action.toggled.connect(self.on_find)

        self.replace_action = tool_bar.addAction(icon_manager.load_icon("replace.png", COLORS.PRIMARY),
                                                 "Replace (Ctrl + R)")
        self.replace_action.setShortcut("Ctrl+R")
        self.replace_action.setCheckable(True)
        self.replace_action.toggled.connect(self.on_replace)

        main_layout.addWidget(self.find_bar)
        self.find_bar.setHidden(True)
        self.find_bar.request_find_pattern.connect(self.code_editor.find_pattern)
        self.find_bar.request_find_reset.connect(self.code_editor.reset_find)
        self.find_bar.request_uncheck.connect(self.on_find_bar_close)
        self.find_bar.request_next.connect(self.code_editor.goto_next_find)
        self.find_bar.request_prev.connect(self.code_editor.goto_prev_find)
        self.find_bar.tab_pressed.connect(self.replace_bar.setFocus)

        main_layout.addWidget(self.replace_bar)
        self.replace_bar.setHidden(True)
        self.replace_bar.request_uncheck.connect(self.replace_action.setChecked)
        self.replace_bar.request_replace.connect(self.replace_next)
        self.replace_bar.request_replace_all.connect(self.replace_all)
        self.replace_bar.tab_pressed.connect(self.find_bar.setFocus)

        main_layout.addWidget(self.code_editor)
        self.code_editor.search_complete.connect(self.on_search_complete)
        self.code_editor.unsaved_changes.connect(self.set_unsaved_changes)
        self.code_editor.document().undoAvailable.connect(self.on_undo_available)
        self.code_editor.document().redoAvailable.connect(self.on_redo_available)

    def on_new(self):
        if self.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog(self.tab_name)
            result = dialog.exec()
            if not result == QtWidgets.QDialog.Accepted:
                return
            elif dialog.save_changes:
                self.save_changes()
        mod_path = main_widget.instance.get_loaded_mod_path()
        # get file path
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "New .ndf File", mod_path, "*.ndf")
        if file_path == "":
            return
        file_path = file_path.replace("/", "\\")
        if not file_path.endswith(".ndf"):
            file_path = file_path.append(".ndf")
        # clear/create file
        try:
            open(file_path, 'w').close()
        except Exception as e:
            logging.error("Could not create file " + file_path + ": " + str(e))
        # reset editor
        self.code_editor.setPlainText("")
        self.code_editor.document().clearUndoRedoStacks()
        # reset page
        self.file_paths.clear()
        self.file_paths.add(file_path)
        self.unsaved_changes = False
        # update tab name
        self.tab_name = file_path[file_path.rindex('\\') + 1:]
        self.unsaved_status_change.emit(False, self)

    def on_open(self):
        file_path, _ = QtWidgets.QFileDialog().getOpenFileName(self,
                                                               "Select .ndf File",
                                                               main_widget.instance.get_loaded_mod_path(),
                                                               "*.ndf")
        if not QtCore.QFile.exists(file_path):
            return
        self.open_file(file_path)

    def open_file(self, file_path):
        main_widget.instance.show_loading_screen("opening file...")
        try:
            with open(file_path, encoding="UTF-8") as f:
                self.code_editor.setPlainText(f.read())
            super().open_file(file_path)
        except Exception as e:
            logging.error("Could not open file " + file_path + ": " + str(e))
            main_widget.instance.hide_loading_screen()
        # update tab name
        file_path = file_path.replace("/", "\\")
        self.tab_name = file_path[file_path.rindex('\\') + 1:]
        self.unsaved_status_change.emit(False, self)
        self.restore_action.setEnabled(True)

        main_widget.instance.hide_loading_screen()

    def _save_changes(self):
        file_path = self.file_paths[0]
        if file_path == "":
            mod_path = main_widget.instance.get_loaded_mod_path()
            # get file path
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "New .ndf File", mod_path, "*.ndf")
            if file_path == "":
                return
            # set tab name
            file_path = file_path.replace("/", "\\")
            if not file_path.endswith(".ndf"):
                file_path = file_path.append(".ndf")
            self.tab_name = file_path[file_path.rindex('\\') + 1:]
        ret = False
        try:
            with open(file_path, "w", encoding="UTF-8") as f:
                f.write(self.code_editor.toPlainText())
            ret = True
        except Exception as e:
            logging.error("Could not save to file " + file_path + ": " + str(e))
        return ret

    def on_save_as(self):
        mod_path = main_widget.instance.get_loaded_mod_path()
        # get file path
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "New .ndf File", mod_path, "*.ndf")
        if file_path == "":
            return
        file_path = file_path.replace("/", "\\")
        if not file_path.endswith(".ndf"):
            file_path = file_path.append(".ndf")
        # clear/create file
        try:
            f = open(file_path, 'w')
            f.write(self.code_editor.toPlainText())
            f.close()
        except Exception as e:
            logging.error("Error while writing to file " + file_path + ": " + str(e))
        # reset page
        self.file_paths.clear()
        self.file_paths.add(file_path)
        self.unsaved_changes = False
        self.restore_action.setEnabled(True)
        # update tab name
        self.tab_name = file_path[file_path.rindex('\\') + 1:]
        self.unsaved_status_change.emit(False, self)

    def on_restore(self):
        if self.unsaved_changes:
            file_path = self.file_paths[0]
            file_name = file_path[file_path.rindex('\\') + 1:]
            dialog = essential_dialogs.ConfirmationDialog("Your changes on " + file_name + " will be lost! Continue?",
                                                          "Warning!")
            if not dialog.exec():
                return

        self.update_page()

    def update_page(self):
        # if not yet saved, just clear the editor
        if len(self.file_paths) == 0:
            self.code_editor.setPlainText("")
        else:
            last_pos = self.code_editor.get_cursor_pos()
            self.open_file(self.file_paths[0])
            self.code_editor.set_cursor_pos(last_pos)

    def on_find_bar_close(self, _):
        self.find_action.setChecked(False)
        self.replace_bar.on_close()

    def on_find(self, checked):
        selection = self.code_editor.get_selected_text()
        if checked:
            self.find_bar.setHidden(False)
            self.find_bar.line_edit.setFocus()
            # if editor has selection, search for it
            if len(selection) > 0:
                self.find_bar.line_edit.setText(selection)
                self.code_editor.find_pattern(selection)
                self.code_editor.goto_prev_find()
            if self.replace_action.isChecked():
                self.find_action.setChecked(False)

        elif len(selection) > 0 and not self.replace_action.isChecked():
            self.find_action.setChecked(True)

        elif not self.replace_action.isChecked():
            self.find_bar.reset()

    def on_replace(self, checked):
        if checked:
            self.find_bar.setHidden(False)
            self.find_action.setChecked(False)
            self.replace_bar.setHidden(False)
            self.replace_bar.line_edit.setFocus()
        else:
            self.replace_bar.setHidden(True)
            self.replace_bar.line_edit.setText("")
            if not self.find_bar.isHidden():
                self.find_action.setChecked(True)

    def on_search_complete(self):
        results = len(self.code_editor.get_find_results())
        if results == 0:
            self.find_bar.set_label_text("0 results for \"" + self.find_bar.line_edit.text() + "\"")
            self.find_bar.enable_find_buttons(False)
        else:
            self.find_bar.set_label_text(str(results) + " results for \"" + self.find_bar.line_edit.text() + "\"")
            self.find_bar.enable_find_buttons(True)

    def on_undo_available(self, available: bool):
        self.undo_action.setDisabled(not available)

    def on_redo_available(self, available: bool):
        self.redo_action.setDisabled(not available)

    def on_undo(self):
        self.code_editor.document().undo()

    def on_redo(self):
        self.code_editor.document().redo()

    def replace_next(self, replace_pattern):
        find_pattern = self.find_bar.line_edit.text()
        self.code_editor.replace_next(find_pattern, replace_pattern)

    def replace_all(self, replace_pattern):
        find_pattern = self.find_bar.line_edit.text()
        self.code_editor.replace_all(find_pattern, replace_pattern)

    def from_json(self, json_obj: dict):
        if not json_obj["filePath"] == "":
            self.open_file(json_obj["filePath"])
        cursor = self.code_editor.textCursor()
        cursor.setPosition(json_obj["cursorPos"])
        self.code_editor.setTextCursor(cursor)

    def to_json(self) -> dict:
        return {
            "filePath": list(self.file_paths)[0],
            "cursorPos": self.code_editor.textCursor().position()
        }
