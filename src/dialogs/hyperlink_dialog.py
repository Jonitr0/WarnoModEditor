from PySide6 import QtWidgets

from src.dialogs import base_dialog


class HyperlinkDialog(base_dialog.BaseDialog):
    def __init__(self, text: str = "", link: str = ""):
        self.link_edit = QtWidgets.QLineEdit()
        self.link_edit.setText(link)
        self.text_edit = QtWidgets.QLineEdit()
        self.text_edit.setText(text)

        super().__init__()
        self.setWindowTitle("Add/Edit hyperlink")

    def setup_ui(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(10)
        self.main_layout.addLayout(form_layout)

        form_layout.addRow("Displayed Text:", self.text_edit)
        form_layout.addRow("Link:", self.link_edit)

    def get_data(self):
        return self.text_edit.text(), self.link_edit.text()
