from PySide2 import QtWidgets

from dialogs import base_dialog


class SelectBackupDialog(base_dialog.BaseDialog):
    def __init__(self, text: str, title: str, backup_list: []):
        self.label = QtWidgets.QLabel(text)
        self.combobox = QtWidgets.QComboBox(backup_list)

        super().__init__()
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)
        self.main_layout.addLayout(self.combobox)

    def get_selection(self):
        return self.combobox.currentText()
