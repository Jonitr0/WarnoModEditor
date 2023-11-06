from PySide6 import QtWidgets, QtGui

import difflib

from src.wme_widgets.tab_pages.base_tab_page import BaseTabPage


class FileComparisonPage(BaseTabPage):
    def __init__(self, left_text: str, right_text: str):
        super().__init__()
        self.main_layout = QtWidgets.QVBoxLayout()
        self.left_text_edit = QtWidgets.QTextEdit()
        self.right_text_edit = QtWidgets.QTextEdit()

        self.left_text = left_text
        self.right_text = right_text

        self.setup_ui()

        self.help_file_path = "Help_FileComparisonPage.html"

    def setup_ui(self):
        compare_layout = QtWidgets.QVBoxLayout()

        # add two text edits
        compare_layout.addWidget(self.left_text_edit)
        compare_layout.addWidget(self.right_text_edit)

        # make them read-only
        self.left_text_edit.setReadOnly(True)
        self.right_text_edit.setReadOnly(True)

        # set the text
        self.left_text_edit.setText(self.left_text)
        self.right_text_edit.setText(self.right_text)

        # get the differences between the two texts and highlight them
        self.highlight_differences()

        # put compare layout in a vertical scroll area
        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setLayout(compare_layout)

        # add scroll area to the main layout
        self.setLayout(self.main_layout)
        self.main_layout.addWidget(scroll_area)

    def highlight_differences(self):
        # get the text from the text edits
        left_text = self.left_text_edit.toPlainText()
        right_text = self.right_text_edit.toPlainText()

        # get the differences between using difflib
        diff = difflib.ndiff(left_text.splitlines(), right_text.splitlines())

        # highlight the differences
        for line in diff:
            if line.startswith('+'):
                self.left_text_edit.setTextColor(QtGui.QColor("red"))
                self.left_text_edit.insertPlainText(line)
                self.left_text_edit.setTextColor(QtGui.QColor("black"))
            elif line.startswith('-'):
                self.right_text_edit.setTextColor(QtGui.QColor("red"))
                self.right_text_edit.insertPlainText(line)
                self.right_text_edit.setTextColor(QtGui.QColor("black"))
            else:
                self.left_text_edit.insertPlainText(line)
                self.right_text_edit.insertPlainText(line)


