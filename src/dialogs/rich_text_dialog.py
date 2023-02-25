# dialog displaying a markdown-formatted text

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.wme_widgets import base_window
from src.utils import markdown_loader


class RichTextDialog(base_window.BaseWindow):
    def __init__(self, md_file_path: str, title: str):
        super().__init__()

        self.content_layout = QtWidgets.QHBoxLayout()
        self.content_layout.setContentsMargins(10, 10, 10, 10)
        self.bar_layout.addLayout(self.content_layout)

        self.rich_text_label = QtWidgets.QLabel()
        self.rich_text_label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.rich_text_label.setTextFormat(Qt.RichText)
        self.rich_text_label.setAlignment(Qt.AlignCenter)
        self.rich_text_label.setText(markdown_loader.get_md_text(md_file_path))
        self.rich_text_label.setWordWrap(True)

        self.content_layout.addWidget(self.rich_text_label)

        self.setWindowTitle(title)
        self.title_bar.set_title(title)
