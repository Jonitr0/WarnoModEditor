from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

from dialogs.base_dialog import BaseDialog


class NewModDialog(BaseDialog):
    def __init__(self, warno_path):
        self.generate_checkbox = QtWidgets.QCheckBox()
        self.name_line_edit = QtWidgets.QLineEdit()
        self.warno_path = warno_path

        super().__init__()
        self.setWindowTitle("Create new mod")

    def setup_ui(self):
        checkbox_layout = QtWidgets.QHBoxLayout(self)

        self.name_line_edit.setPlaceholderText("Enter the name of your new mod")
        self.main_layout.addWidget(self.name_line_edit)

        checkbox_layout.setAlignment(Qt.AlignCenter)
        self.main_layout.addLayout(checkbox_layout)

        self.generate_checkbox.setChecked(True)
        generate_info = "The generation step is needed before a mod can be activated in-game or uploaded to the " \
                        "Steam Workshop. For a short period of time, the screen will turn black and the WARNO Mod " \
                        "Editor will become unresponsive during the process. You can always generate your mod later" \
                        " if you don't do it now."
        checkbox_layout.addWidget(self.generate_checkbox)
        checkbox_label = QtWidgets.QLabel("Generate mod after creation")
        checkbox_layout.addWidget(checkbox_label)

        generate_info_label = QtWidgets.QLabel(generate_info)
        generate_info_label.setWordWrap(True)
        generate_info_label.setFixedWidth(600)
        self.main_layout.addWidget(generate_info_label)

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

    def get_mod_generate(self):
        return self.generate_checkbox.checkState()