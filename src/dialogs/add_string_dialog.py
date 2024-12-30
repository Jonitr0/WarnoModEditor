from PySide6 import QtWidgets

from src.wme_widgets import wme_essentials
from src.dialogs import base_dialog, essential_dialogs


class AddStringDialog(base_dialog.BaseDialog):
    def __init__(self):
        self.file_combobox = wme_essentials.WMECombobox()
        self.token_lineedit = wme_essentials.WMELineEdit()
        self.string_lineedit = wme_essentials.WMELineEdit()

        super(AddStringDialog, self).__init__()
        self.setWindowTitle("Add String")

    def setup_ui(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(form_layout)

        self.file_combobox.addItems([
            "COMPANIES.csv",
            "INTERFACE_INGAME.csv",
            "INTERFACE_OUTGAME.csv",
            "PLATOONS.csv",
            "UNITS.csv"
        ])

        form_layout.addRow("File:", self.file_combobox)

        self.token_lineedit.setPlaceholderText("Token to represent string")
        form_layout.addRow("Token:", self.token_lineedit)

        self.string_lineedit.setPlaceholderText("String value")
        form_layout.addRow("String:", self.string_lineedit)
        
    def get_result(self):
        return self.file_combobox.currentText(), self.token_lineedit.text(), self.string_lineedit.text()
    
    def accept(self) -> None:
        if self.token_lineedit.text() == "":
            essential_dialogs.MessageDialog("Unable to add string", "Token cannot be empty.").exec()
            return
        super(AddStringDialog, self).accept()

