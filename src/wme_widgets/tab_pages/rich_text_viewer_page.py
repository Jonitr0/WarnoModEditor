# tab page that displays html files

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages import tab_page_base
from src.utils import markdown_loader
from src.utils.color_manager import *


class RichTextViewerPage(tab_page_base.TabPageBase):
    def __init__(self, md_file_path: str):
        super().__init__()

        hyperlink_color = get_color_for_key(COLORS.PRIMARY.value)

        text = markdown_loader.get_md_text(md_file_path)
        text = text.replace("<a href=", "<a style =\"color: " + hyperlink_color + "\"href=")

        rich_text_label = QtWidgets.QLabel()
        rich_text_label.setTextFormat(Qt.RichText)
        rich_text_label.setText(text)
        rich_text_label.setAlignment(Qt.AlignTop)
        rich_text_label.setOpenExternalLinks(True)
        rich_text_label.setWordWrap(True)
        rich_text_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(rich_text_label)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)


