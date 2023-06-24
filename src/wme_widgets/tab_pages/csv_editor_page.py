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

        self.table_widget = QtWidgets.QTableWidget()
        main_layout.addWidget(self.table_widget)

        self.table_widget.setColumnCount(2)
        self.table_widget.setRowCount(1)

        self.expand_header()

        # TODO: to/from json
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

    def _save_changes(self):
        # TODO: implement
        pass

    def on_save_as(self):
        # TODO: implement
        pass

    def on_restore(self):
        if self.unsaved_changes:
            file_path = list(self.file_paths)[0]
            file_name = file_path[file_path.rindex('\\') + 1:]
            dialog = essential_dialogs.ConfirmationDialog("Your changes on " + file_name + " will be lost! Continue?",
                                                          "Warning!")
            if not dialog.exec():
                return

        self.update_page()



