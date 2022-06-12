from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


class NewModDialog(QtWidgets.QDialog):
    def __init__(self, warno_path):
        super().__init__()

        self.generate_checkbox = QtWidgets.QCheckBox()
        self.name_line_edit = QtWidgets.QLineEdit()
        self.warno_path = warno_path
        self.setup_ui()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.Dialog)
        self.setWindowTitle("Create new mod")

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        checkbox_layout = QtWidgets.QHBoxLayout()
        button_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        self.name_line_edit.setPlaceholderText("Enter the name of your new mod")
        main_layout.addWidget(self.name_line_edit)

        checkbox_layout.setAlignment(Qt.AlignCenter)
        main_layout.addLayout(checkbox_layout)

        self.generate_checkbox.setChecked(True)
        checkbox_layout.addWidget(self.generate_checkbox)
        checkbox_label = QtWidgets.QLabel("Generate mod after creation")
        checkbox_layout.addWidget(checkbox_label)

        main_layout.addLayout(button_layout)
        main_layout.setAlignment(button_layout, Qt.AlignCenter)

        # setup ok button
        ok_button = QtWidgets.QPushButton()
        ok_button.setText("OK")
        ok_button.setFixedWidth(50)
        ok_button.clicked.connect(self.on_ok)
        button_layout.addWidget(ok_button)

        # setup cancel button
        cancel_button = QtWidgets.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.setFixedWidth(50)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

    def on_ok(self):
        mod_name = self.name_line_edit.text()
        if mod_name == "":
            QtWidgets.QMessageBox().information(self, "Name empty",
                                                "The name of your mod cannot be empty.")
            return
        elif QtCore.QDir(self.warno_path + "/Mods/" + mod_name).exists():
            QtWidgets.QMessageBox().information(self, "Directory already exists",
                                                "A mod directory with this name already exists.")
            return

        self.accept()

    def get_mod_name(self):
        return self.name_line_edit.text()

    def get_mod_generate(self):
        return self.generate_checkbox.checkState()