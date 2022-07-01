from PySide2 import QtWidgets
from dialogs.base_dialog import BaseDialog


class WarnoPathDialog(BaseDialog):
    def __init__(self, warno_path):
        self.line_edit = QtWidgets.QLineEdit()
        self.warno_path = warno_path

        super().__init__()
        self.setWindowTitle("Set WARNO path")

    def setup_ui(self):
        # setup layouts
        text_layout = QtWidgets.QHBoxLayout(self)

        # setup label
        info_label = QtWidgets.QLabel()
        info_label.setText("Please enter the path to your WARNO installation.\nIt could look like this: "
                           "\"C:/Program Files (x86)/Steam/steamapps/common/WARNO\"")
        self.main_layout.addWidget(info_label)
        self.main_layout.addLayout(text_layout)

        # setup line edit
        self.line_edit.setText(self.warno_path)
        text_layout.addWidget(self.line_edit)

        # setup "browse" button
        browse_button = QtWidgets.QPushButton()
        browse_button.setText("Browse..")
        # TODO: remove lambda
        browse_button.clicked.connect(self.open_warno_path_dialog)
        text_layout.addWidget(browse_button)

    def open_warno_path_dialog(self):
        warno_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter WARNO path", self.line_edit.text())

        self.line_edit.setText(warno_path)

    def get_path(self):
        return self.line_edit.text().removesuffix("/")
