from PySide6 import QtWidgets

from src.wme_widgets.tab_pages import base_tab_page


class CsvEditorPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        table_widget = QtWidgets.QTableWidget()
        main_layout.addWidget(table_widget)

        table_widget.setColumnCount(5)
        table_widget.setRowCount(10)

        # TODO: open files
        # TODO: to/from json
        # TODO: help page
