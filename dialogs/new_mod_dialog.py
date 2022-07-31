from PySide6 import QtWidgets, QtCore

from dialogs.base_dialog import BaseDialog
from dialogs import message_dialog


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
            message_dialog.MessageDialog("Name empty",
                                         "The name of your mod cannot be empty.").exec()
            return
        elif QtCore.QDir(self.warno_path + "/Mods/" + mod_name).exists():
            message_dialog.MessageDialog("Directory already exists",
                                         "A mod directory with this name already exists.").exec()
            return

        super().accept()

    def get_mod_name(self):
        return self.name_line_edit.text()
