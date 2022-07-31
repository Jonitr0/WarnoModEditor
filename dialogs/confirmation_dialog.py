# dialog asking user to confirm or cancel something

from PySide6 import QtWidgets

from dialogs import base_dialog


class ConfirmationDialog(base_dialog.BaseDialog):
    def __init__(self, text: str, title: str):
        self.label = QtWidgets.QLabel(text)

        super().__init__(urgent=True)
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)
