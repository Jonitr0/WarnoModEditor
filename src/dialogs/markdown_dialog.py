# dialog displaying a markdown-formatted text

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.dialogs.base_dialog import BaseDialog
from src.utils import markdown_loader


class MarkdownDialog(BaseDialog):
    def __init__(self, md_file_path: str, title: str):
        self.md_label = QtWidgets.QLabel()
        self.md_label.setTextFormat(Qt.MarkdownText)
        self.md_label.setText(markdown_loader.get_md_text(md_file_path))
        self.md_label.setMaximumWidth(500)
        self.md_label.setWordWrap(True)

        super().__init__(ok_only=True)
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.md_label)
