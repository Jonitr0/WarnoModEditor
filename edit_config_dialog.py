from pathlib import Path

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


class WarnoPathDialog(QtWidgets.QDialog):
    def __init__(self, config: QtCore.QSettings):
        self.icon_path_line_edit = QtWidgets.QLineEdit()
        self.config = config
        super().__init__()

        self.setup_ui()
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.Dialog)
        self.setWindowTitle("Edit mod configuration")

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout(self)
        main_layout.addLayout(form_layout)

        name_line_edit = QtWidgets.QLineEdit()
        name_line_edit.setText(str(self.config.value("Properties/Name")))
        name_line_edit.textChanged.connect(self.on_name_changed)
        form_layout.addRow("Name", name_line_edit)

        description_line_edit = QtWidgets.QLineEdit()
        description_line_edit.setText(str(self.config.value("Properties/Description")))
        description_line_edit.textChanged.connect(self.on_description_changed)
        form_layout.addRow("Description", description_line_edit)

        self.icon_path_line_edit.setText(str(self.config.value("Properties/PreviewImagePath")))
        self.icon_path_line_edit.textChanged.connect(self.on_icon_path_changed)
        browse_button = QtWidgets.QPushButton()
        browse_button.setText("Browse..")
        browse_button.clicked.connect(self.on_icon_browse)
        icon_path_layout = QtWidgets.QHBoxLayout()
        icon_path_layout.addWidget(self.icon_path_line_edit)
        icon_path_layout.addWidget(browse_button)
        form_layout.addRow("Preview Image Path", icon_path_layout)

        cosmetic_checkbox = QtWidgets.QCheckBox()
        cosmetic_checkbox.setChecked(int(self.config.value("Properties/CosmeticOnly")))
        cosmetic_checkbox.stateChanged.connect(self.on_cosmetic)
        form_layout.addRow("Cosmetic only", cosmetic_checkbox)

        form_layout.addRow("Mod Version", QtWidgets.QSpinBox())
        form_layout.addRow("Deck Format Version", QtWidgets.QSpinBox())

    def on_name_changed(self, name: str):
        self.config.setValue("Properties/Name", name)

    def on_description_changed(self, desc: str):
        self.config.setValue("Properties/Description", desc)

    def on_icon_path_changed(self, icon_path: str):
        self.config.setValue("Properties/PreviewImagePath", icon_path)

    def on_icon_browse(self):
        icon_path = self.icon_path_line_edit.text()
        if not QtCore.QDir(icon_path).exists():
            icon_path = str(Path.home())
        icon_path, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Enter WARNO path", icon_path)
        self.icon_path_line_edit.setText(icon_path)

    def on_cosmetic(self, state):
        self.config.setValue("Properties/CosmeticOnly", state)

    def get_config(self):
        return self.config
