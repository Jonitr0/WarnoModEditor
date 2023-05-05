from PySide6 import QtWidgets

from src.dialogs import base_dialog
from src.wme_widgets import wme_lineedit


class NewBackupDialog(base_dialog.BaseDialog):
    def __init__(self):
        self.line_edit = wme_lineedit.WMELineEdit()

        super().__init__()
        self.setWindowTitle("Create backup")

        self.line_edit.setFocus()

    def setup_ui(self):
        info_label = QtWidgets.QLabel("A name will be automatically generated "
                                      "from the current time if you leave the name field empty.")
        self.main_layout.addWidget(info_label)

        self.line_edit.setPlaceholderText("Enter backup name")
        self.main_layout.addWidget(self.line_edit)

    def get_name(self):
        return self.line_edit.text()