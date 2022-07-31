# dialog that informs the user of something

from PySide6 import QtWidgets

from dialogs import base_dialog


class MessageDialog(base_dialog.BaseDialog):
    def __init__(self, title: str, text: str):
        self.label = QtWidgets.QLabel(text)

        super().__init__(ok_only=True, urgent=True)
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)
