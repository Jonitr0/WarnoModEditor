from PySide6 import QtWidgets, QtCore

from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import main_widget

from src.dialogs import essential_dialogs
from src.utils import icon_manager
from src.utils.color_manager import *

import csv


class CsvEditorPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

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

        add_row_before_action = tool_bar.addAction(icon_manager.load_icon("add_row_before.png", COLORS.PRIMARY),
                                                   "Add row before selected (Ctrl + Alt + Arrow Up)")
        add_row_before_action.setShortcut("Ctrl+Alt+Up")
        add_row_before_action.triggered.connect(self.on_add_row_before)

        add_row_after_action = tool_bar.addAction(icon_manager.load_icon("add_row_after.png", COLORS.PRIMARY),
                                                  "Add row after selected (Ctrl + Alt + Arrow Down)")
        add_row_after_action.setShortcut("Ctrl+Alt+Down")
        add_row_after_action.triggered.connect(self.on_add_row_after)

        delete_row_action = tool_bar.addAction(icon_manager.load_icon("remove_row.png", COLORS.PRIMARY),
                                               "Remove selected rows (Shift + Del)")
        delete_row_action.setShortcut("Shift+Del")
        delete_row_action.triggered.connect(self.on_remove_row)

        self.table_widget = QtWidgets.QTableWidget()
        main_layout.addWidget(self.table_widget)

        self.table_widget.cellChanged.connect(self.on_table_changed)
        self.table_widget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(1)
        self.expand_header()

        # TODO: help page

    def expand_header(self):
        for i in range(self.table_widget.columnCount()):
            self.table_widget.horizontalHeader().setSectionResizeMode(i, QtWidgets.QHeaderView.Stretch)

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
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "New .csv File", mod_path, "*.csv")
        if file_path == "":
            return
        file_path = file_path.replace("/", "\\")
        if not file_path.endswith(".csv"):
            file_path = file_path.append(".csv")
        # clear/create file
        try:
            open(file_path, 'w').close()
        except Exception as e:
            logging.error("Could not create file " + file_path + ": " + str(e))
        # reset table
        self.table_widget.clear()
        # reset page
        self.file_paths.clear()
        self.file_paths.add(file_path)
        self.unsaved_changes = False
        # update tab name
        self.tab_name = file_path[file_path.rindex('\\') + 1:]
        self.unsaved_status_change.emit(False, self)

    def on_open(self):
        file_path, _ = QtWidgets.QFileDialog().getOpenFileName(self,
                                                               "Select .csv File",
                                                               main_widget.instance.get_loaded_mod_path(),
                                                               "*.csv")
        if not QtCore.QFile.exists(file_path):
            return
        self.open_file(file_path)

    def open_file(self, file_path):
        main_widget.instance.show_loading_screen("Opening file...")
        self.table_widget.clear()
        self.table_widget.setRowCount(0)
        try:
            with open(file_path, encoding="UTF-8") as f:
                reader = csv.reader(f, delimiter=';')
                header = next(reader)
                self.table_widget.setColumnCount(len(header))
                self.table_widget.setHorizontalHeaderLabels(header)
                for row, values in enumerate(reader):
                    self.table_widget.insertRow(row)
                    for column, value in enumerate(values):
                        self.table_widget.setItem(row, column, QtWidgets.QTableWidgetItem(value))
            super().open_file(file_path)
        except Exception as e:
            logging.error("Could not open file " + file_path + ": " + str(e))
            main_widget.instance.hide_loading_screen()
        self.expand_header()
        # update tab name
        file_path = file_path.replace("/", "\\")
        self.tab_name = file_path[file_path.rindex('\\') + 1:]
        self.unsaved_status_change.emit(False, self)
        self.restore_action.setEnabled(True)

        main_widget.instance.hide_loading_screen()

    def write_table_to_file(self, file_path):
        columns = range(self.table_widget.columnCount())
        header = [self.table_widget.horizontalHeaderItem(column).text()
                  for column in columns]
        with open(file_path, "w", encoding="utf-8") as f:
            writer = csv.writer(f, delimiter=';', lineterminator="\n")
            writer.writerow(header)
            for row in range(self.table_widget.rowCount()):
                row_texts = []
                for column in columns:
                    if not self.table_widget.item(row, column):
                        row_texts.append("")
                    else:
                        row_texts.append(self.table_widget.item(row, column).text())
                writer.writerow(row_texts)

    def _save_changes(self):
        if len(self.file_paths) == 0:
            self.on_save_as()
            return

        file_path = list(self.file_paths)[0]
        if file_path == "":
            mod_path = main_widget.instance.get_loaded_mod_path()
            # get file path
            file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "New .csv File", mod_path, "*.csv")
            if file_path == "":
                return
            # set tab name
            file_path = file_path.replace("/", "\\")
            if not file_path.endswith(".csv"):
                file_path = file_path.append(".csv")
            self.tab_name = file_path[file_path.rindex('\\') + 1:]
        ret = False
        try:
            self.write_table_to_file(file_path)
            ret = True
        except Exception as e:
            logging.error("Could not save to file " + file_path + ": " + str(e))
        return ret

    def on_save_as(self):
        mod_path = main_widget.instance.get_loaded_mod_path()
        # get file path
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, "New .csv File", mod_path, "*.csv")
        if file_path == "":
            return
        file_path = file_path.replace("/", "\\")
        if not file_path.endswith(".csv"):
            file_path = file_path.append(".csv")
        # clear/create file
        try:
            self.write_table_to_file(file_path)
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
            file_path = list(self.file_paths)[0]
            file_name = file_path[file_path.rindex('\\') + 1:]
            dialog = essential_dialogs.ConfirmationDialog("Your changes on " + file_name + " will be lost! Continue?",
                                                          "Warning!")
            if not dialog.exec():
                return

        self.update_page()

    def update_page(self):
        # if not yet saved, just clear the editor
        if len(self.file_paths) == 0:
            self.table_widget.setColumnCount(2)
            self.table_widget.setRowCount(1)
            self.expand_header()
        else:
            self.open_file(list(self.file_paths)[0])

    def on_add_row_before(self):
        selection_list = self.table_widget.selectedRanges()
        if not selection_list:
            self.table_widget.insertRow(0)
        else:
            selection_min_val = self.table_widget.rowCount()
            for selection in selection_list:
                if selection.topRow() < selection_min_val:
                    selection_min_val = selection.topRow()

            self.table_widget.insertRow(selection_min_val)

        self.unsaved_changes = True

    def on_add_row_after(self):
        selection_list = self.table_widget.selectedRanges()
        if not selection_list:
            self.table_widget.insertRow(self.table_widget.rowCount())
        else:
            selection_max_val = -1
            for selection in selection_list:
                if selection.bottomRow() > selection_max_val:
                    selection_max_val = selection.bottomRow()

            self.table_widget.insertRow(selection_max_val + 1)

        self.unsaved_changes = True

    def on_remove_row(self):
        selection_list = self.table_widget.selectedRanges()
        if not selection_list:
            if self.table_widget.rowCount() == 0:
                return

            self.table_widget.removeRow(self.table_widget.rowCount() - 1)

        # this is so stupid...
        selection_list_tmp = []

        while len(selection_list) > 0:
            selection_max_val = -1
            selection_max_index = -1

            for i in range(len(selection_list)):
                selection = selection_list[i]
                if selection.topRow() > selection_max_val:
                    selection_max_val = selection.topRow()
                    selection_max_index = i

            selection_list_tmp.append(selection_list[selection_max_index])
            del selection_list[selection_max_index]

        selection_list = selection_list_tmp

        for selection in selection_list:
            start = selection.topRow()
            length = selection.bottomRow() + 1 - start

            while length > 0:
                self.table_widget.removeRow(start)
                length -= 1

        self.unsaved_changes = True

    def from_json(self, json_obj: dict):
        if not json_obj["filePath"] == "":
            self.open_file(json_obj["filePath"])

    def to_json(self) -> dict:
        if len(self.file_paths) == 0:
            file_path = ""
        else:
            file_path = list(self.file_paths)[0]
        return {
            "filePath": file_path
        }

    def on_table_changed(self):
        self.unsaved_changes = True
