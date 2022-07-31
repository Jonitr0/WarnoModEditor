from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from dialogs.base_dialog import BaseDialog


class NewModDialog(BaseDialog):
    def __init__(self, warno_path):
        self.name_line_edit = QtWidgets.QLineEdit()
        self.warno_path = warno_path

        super().__init__()
        self.setWindowTitle("Create new mod")

    def setup_ui(self):
        self.name_line_edit.setPlaceholderText("Enter the name of your new mod")
        self.name_line_edit.setMinimumWidth(400)
        self.main_layout.addWidget(self.name_line_edit)

    def accept(self):
        mod_name = self.name_line_edit.text()
        if mod_name == "":
            QtWidgets.QMessageBox().information(self, "Name empty",
                                                "The name of your mod cannot be empty.")
            return
        elif QtCore.QDir(self.warno_path + "/Mods/" + mod_name).exists():
            QtWidgets.QMessageBox().information(self, "Directory already exists",
                                                "A mod directory with this name already exists.")
            return

        super().accept()

    def get_mod_name(self):
        return self.name_line_edit.text()