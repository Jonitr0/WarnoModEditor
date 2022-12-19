# tab page that allows for search in all .ndf files of the mod

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.wme_widgets import wme_lineedit
from src.wme_widgets.tab_pages import tab_page_base


class GlobalSearchPage(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(main_layout)

        search_bar = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 8, 0, 8)
        main_layout.addLayout(search_bar)

        self.search_line_edit = wme_lineedit.WMELineEdit()
        self.search_line_edit.setPlaceholderText("Find text in all .ndf files of your mod")
        search_bar.addWidget(self.search_line_edit)

        search_button = QtWidgets.QPushButton("Find")
        search_bar.addWidget(search_button)

        # TODO: create and fill this file
        self.help_file_path = "Help_GlobalSearch.html"

