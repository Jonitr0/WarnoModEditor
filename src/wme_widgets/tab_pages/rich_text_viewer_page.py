# tab page that displays html files

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages import base_tab_page
from src.utils import markdown_loader
from src.utils.color_manager import *


class RichTextViewerPage(base_tab_page.BaseTabPage):
    def __init__(self, rt_file_path: str = ""):
        super().__init__()

        self.rt_file_path = rt_file_path

        self.rich_text_label = QtWidgets.QLabel()
        self.rich_text_label.setTextFormat(Qt.RichText)
        self.rich_text_label.setAlignment(Qt.AlignTop)
        self.rich_text_label.setOpenExternalLinks(True)
        self.rich_text_label.setWordWrap(True)
        self.rich_text_label.setTextInteractionFlags(Qt.TextSelectableByMouse | Qt.LinksAccessibleByMouse)

        if self.rt_file_path != "":
            self.load_file()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.rich_text_label)

        main_layout = QtWidgets.QHBoxLayout()
        main_layout.addWidget(scroll_area)
        self.setLayout(main_layout)

    def load_file(self):
        hyperlink_color = get_color_for_key(COLORS.PRIMARY.value)

        text = markdown_loader.get_md_text(self.rt_file_path)
        text = text.replace("<a href=", "<a style =\"color: " + hyperlink_color + "\"href=")
        self.rich_text_label.setText(text)

    def to_json(self) -> dict:
        page_json = {"richTextFile": self.rt_file_path}
        return page_json

    def from_json(self, json_obj: dict):
        self.rt_file_path = json_obj["richTextFile"]
        self.load_file()
