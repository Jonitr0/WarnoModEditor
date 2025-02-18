# tab page that allows for search in all .ndf files of the mod
import json
import os

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.wme_widgets import wme_essentials, main_widget
from src.wme_widgets.tab_pages import base_tab_page
from src.utils import icon_manager
from src.utils.color_manager import *


class GlobalSearchPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        self.last_search_case_sensitive = False

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        search_bar = QtWidgets.QToolBar()
        main_layout.addWidget(search_bar)

        self.search_line_edit = wme_essentials.WMELineEdit()
        self.search_line_edit.setPlaceholderText("Find text in all .ndf files of your mod")
        self.search_line_edit.returnPressed.connect(self.on_search)
        search_bar.addWidget(self.search_line_edit)

        self.case_action = search_bar.addAction("Toggle Case Sensitivity (Ctrl + E)")
        self.case_action.setIcon(icon_manager.load_icon("case_sensitivity.png", COLORS.PRIMARY))
        self.case_action.setCheckable(True)
        self.case_action.setChecked(False)
        self.case_action.setShortcut("Ctrl+E")

        search_action = search_bar.addAction("Search (Enter)")
        search_action.setIcon(icon_manager.load_icon("magnify.png", COLORS.PRIMARY))
        search_action.triggered.connect(self.on_search)

        search_bar.addSeparator()

        help_button = search_bar.addAction("Open Page Help Popup (Alt + H)")
        help_button.setIcon(icon_manager.load_icon("help.png", COLORS.PRIMARY))
        help_button.triggered.connect(self.on_help)

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

        self.help_file_path = "Help_GlobalSearch.md"

    def on_search(self):
        # clear layout
        for i in reversed(range(self.list_layout.count())):
            self.list_layout.itemAt(i).widget().setParent(None)

        search_text = self.search_line_edit.text()
        if search_text == "":
            self.results_label.setText("")
            return

        main_widget.instance.show_loading_screen("Searching...")

        self.last_search_case_sensitive = self.case_action.isChecked()

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
                        file_text = f.read()
                        if self.last_search_case_sensitive:
                            res = file_text.__contains__(search_text)
                        else:
                            file_text = file_text.lower()
                            res = file_text.__contains__(search_text.lower())
                        if res:
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
        current_tab_widget = self.page.get_current_tab_widget()
        full_path = os.path.join(main_widget.instance.get_loaded_mod_path(), self.file_name)
        current_tab_widget.on_open_and_find_ndf_editor(full_path, self.pattern, self.page.last_search_case_sensitive)
