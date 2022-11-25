# tab page that displays markdown files

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages import tab_page_base
from src.utils import markdown_loader


class MdViewerPage(tab_page_base.TabPageBase):
    def __init__(self, md_file_path: str):
        super().__init__()

        md_label = QtWidgets.QLabel()
        md_label.setTextFormat(Qt.MarkdownText)
        md_label.setText(markdown_loader.get_md_text(md_file_path))
        md_label.setAlignment(Qt.AlignTop)
        md_label.setWordWrap(True)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(md_label)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)


