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



        # TODO: browse button
        form_layout.addRow("Preview Image Path", QtWidgets.QLineEdit())
        form_layout.addRow("Cosmetic only", QtWidgets.QCheckBox())
        form_layout.addRow("Mod Version", QtWidgets.QSpinBox())
        form_layout.addRow("Deck Format Version", QtWidgets.QSpinBox())

    def on_name_changed(self, name: str):
        self.config.setValue("Properties/Name", name)

    def on_description_changed(self, desc: str):
        self.config.setValue("Properties/Description", desc)

    def on_icon_path_changed(self, icon_path: str):
        self.config.setValue("Properties/PreviewImagePath", icon_path)

    def on_icon_browse(self):
        pass

    def get_config(self):
        return self.config
