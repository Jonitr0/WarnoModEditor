# dialog displaying a markdown-formatted text

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.dialogs import base_dialog
from src.utils import markdown_loader


class RichTextDialog(base_dialog.BaseDialog):
    def __init__(self, md_file_path: str, title: str):
        self.rich_text_label = QtWidgets.QLabel()
        self.rich_text_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.rich_text_label.setTextFormat(Qt.RichText)
        self.rich_text_label.setAlignment(Qt.AlignCenter)
        self.rich_text_label.setText(markdown_loader.get_md_text(md_file_path))
        self.rich_text_label.setWordWrap(True)

        super().__init__(ok_only=True)

        self.setWindowTitle(title)
        self.title_bar.set_title(title)
        self.setModal(False)

    def setup_ui(self):
        self.main_layout.addWidget(self.rich_text_label)
