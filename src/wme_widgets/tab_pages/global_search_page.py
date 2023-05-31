# tab page that allows for search in all .ndf files of the mod
import json
import os

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.wme_widgets import wme_essentials, main_widget
from src.wme_widgets.tab_pages import base_tab_page
from src.utils import icon_manager
from src.utils.color_manager import *


class GlobalSearchPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        self.setLayout(main_layout)

        search_bar = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(0, 8, 0, 8)
        main_layout.addLayout(search_bar)

        self.search_line_edit = wme_essentials.WMELineEdit()
        self.search_line_edit.setPlaceholderText("Find text in all .ndf files of your mod")
        self.search_line_edit.returnPressed.connect(self.on_search)
        search_bar.addWidget(self.search_line_edit)

        search_button = QtWidgets.QToolButton()
        search_button.setIcon(icon_manager.load_icon("magnify.png", COLORS.PRIMARY))
        search_button.setToolTip("Find search text")
        search_button.setFixedSize(36, 36)
        search_button.clicked.connect(self.on_search)
        search_bar.addWidget(search_button)

        self.results_label = QtWidgets.QLabel()
        main_layout.addWidget(self.results_label)

        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_layout.setSpacing(0)
        self.list_layout.setAlignment(Qt.AlignTop)

        list_widget = QtWidgets.QWidget()
        list_widget.setLayout(self.list_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(list_widget)
        main_layout.addWidget(scroll_area)

        self.help_file_path = "Help_GlobalSearch.html"

    def on_search(self):
        # clear layout
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().setParent(None)

        search_text = self.search_line_edit.text()
        if search_text == "":
            self.results_label.setText("")
            return

        main_widget.instance.show_loading_screen("Searching...")

        results = []

        mod_path = main_widget.instance.get_loaded_mod_path()
        # go through all files
        for root, dirs, files in os.walk(mod_path):
            for file in files:
                if file.endswith(".ndf"):
                    # open ndf files
                    filepath = os.path.join(root, file)
                    with open(filepath) as f:
                        # check if they contain search text
                        if f.read().__contains__(search_text):
                            filepath = filepath.removeprefix(mod_path + "\\")
                            results.append(filepath)

        # create label
        if len(results) == 0:
            self.results_label.setText("No search results found for \"" + search_text + "\"")
        elif len(results) == 1:
            self.results_label.setText("1 file in your mod contains \"" + search_text + "\":")
        else:
            self.results_label.setText(str(len(results)) + " files in your mod contain \"" + search_text + "\":")

        for file in results:
            # pass reference to self
            self.list_layout.addWidget(SearchResultWidget(file, search_text, self))

        main_widget.instance.hide_loading_screen()

    def to_json(self) -> dict:
        page_json = {"currentSearch": self.search_line_edit.text()}
        return page_json

    def from_json(self, json_obj: dict):
        self.search_line_edit.setText(json_obj["currentSearch"])


class SearchResultWidget(QtWidgets.QFrame):
    def __init__(self, file_name: str, pattern: str, page: GlobalSearchPage):
        super().__init__()
        self.setObjectName("list_entry")
        self.file_name = file_name
        self.pattern = pattern
        self.page = page

        main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(main_layout)

        label = QtWidgets.QLabel(file_name)
        main_layout.addWidget(label)
        main_layout.addStretch(1)

        button = QtWidgets.QPushButton("Open in Text Editor")
        button.clicked.connect(self.on_button_pressed)
        main_layout.addWidget(button)

    def on_button_pressed(self):
        current_tab_widget = self.page.parent().parent()
        full_path = os.path.join(main_widget.instance.get_loaded_mod_path(), self.file_name)
        current_tab_widget.on_open_and_find_ndf_editor(full_path, self.pattern)