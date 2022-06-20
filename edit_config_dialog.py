from pathlib import Path

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


class WarnoPathDialog(QtWidgets.QDialog):
    def __init__(self, config_values: dict):
        self.icon_path_line_edit = QtWidgets.QLineEdit()
        self.config_values = config_values
        super().__init__()

        self.setup_ui()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.Dialog)
        self.setWindowTitle("Edit mod configuration")

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout(self)
        main_layout.addLayout(form_layout)

        # TODO: Add tooltips for all labels

        name_line_edit = QtWidgets.QLineEdit()
        name_line_edit.setText(str(self.config_values["Properties/Name"]))
        name_line_edit.textChanged.connect(self.on_name_changed)
        form_layout.addRow("Name", name_line_edit)

        description_line_edit = QtWidgets.QLineEdit()
        description_line_edit.setText(str(self.config_values["Properties/Description"]))
        description_line_edit.textChanged.connect(self.on_description_changed)
        form_layout.addRow("Description", description_line_edit)

        self.icon_path_line_edit.setText(str(self.config_values["Properties/PreviewImagePath"]))
        self.icon_path_line_edit.textChanged.connect(self.on_icon_path_changed)
        browse_button = QtWidgets.QPushButton()
        browse_button.setText("Browse..")
        browse_button.clicked.connect(self.on_icon_browse)
        icon_path_layout = QtWidgets.QHBoxLayout()
        icon_path_layout.addWidget(self.icon_path_line_edit)
        icon_path_layout.addWidget(browse_button)
        form_layout.addRow("Preview Image Path", icon_path_layout)

        cosmetic_checkbox = QtWidgets.QCheckBox()
        cosmetic_checkbox.setChecked(int(self.config_values["Properties/CosmeticOnly"]))
        cosmetic_checkbox.stateChanged.connect(self.on_cosmetic_changed)
        form_layout.addRow("Cosmetic only", cosmetic_checkbox)

        mod_version_spinbox = QtWidgets.QSpinBox()
        mod_version_spinbox.setMinimum(0)
        mod_version_spinbox.setValue(int(self.config_values["Properties/Version"]))
        mod_version_spinbox.valueChanged.connect(self.on_mod_version_changed)
        form_layout.addRow("Mod Version", mod_version_spinbox)

        deck_format_version_spinbox = QtWidgets.QSpinBox()
        deck_format_version_spinbox.setMinimum(0)
        deck_format_version_spinbox.setValue(int(self.config_values["Properties/DeckFormatVersion"]))
        deck_format_version_spinbox.valueChanged.connect(self.on_deck_format_version_changed)
        form_layout.addRow("Deck Format Version", deck_format_version_spinbox)

        button_layout = QtWidgets.QHBoxLayout(self)
        main_layout.addLayout(button_layout)
        main_layout.setAlignment(button_layout, Qt.AlignCenter)

        # setup ok button
        ok_button = QtWidgets.QPushButton()
        ok_button.setText("OK")
        ok_button.setFixedWidth(80)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        # setup cancel button
        cancel_button = QtWidgets.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.setFixedWidth(80)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

    def on_name_changed(self, name: str):
        self.config_values["Properties/Name"] =  name

    def on_description_changed(self, desc: str):
        self.config_values["Properties/Description"] = desc

    def on_icon_path_changed(self, icon_path: str):
        self.config_values["Properties/PreviewImagePath"] = icon_path

    def on_icon_browse(self):
        icon_path = self.icon_path_line_edit.text()
        if not QtCore.QDir(icon_path).exists():
            icon_path = str(Path.home())
        icon_path, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Enter WARNO path", icon_path)
        self.icon_path_line_edit.setText(icon_path)

    def on_cosmetic_changed(self, state):
        self.config_values["Properties/CosmeticOnly"] = state

    def on_mod_version_changed(self, version):
        self.config_values["Properties/Version"] = version

    def on_deck_format_version_changed(self, version):
        self.config_values["Properties/DeckFormatVersion"] = version

    def get_config_values(self):
        return self.config_values
