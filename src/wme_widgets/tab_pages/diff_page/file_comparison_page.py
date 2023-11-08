from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

import difflib

from src.wme_widgets.tab_pages.base_tab_page import BaseTabPage


class FileComparisonPage(BaseTabPage):
    def __init__(self, left_text: str, right_text: str):
        super().__init__()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self.left_text_edit = QtWidgets.QPlainTextEdit()
        self.right_text_edit = QtWidgets.QPlainTextEdit()

        self.left_text = left_text
        self.right_text = right_text

        self.setup_ui()

        self.help_file_path = "Help_FileComparisonPage.html"

    def setup_ui(self):
        # add two text edits
        self.main_layout.addWidget(self.left_text_edit)
        self.main_layout.addWidget(self.right_text_edit)
        
        # disable scroll bars on the text edits
        self.left_text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.right_text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # connect slider slots
        self.left_text_edit.verticalScrollBar().valueChanged.connect(self.on_left_slider_moved)
        self.right_text_edit.verticalScrollBar().valueChanged.connect(self.on_right_slider_moved)

        # make them read-only
        self.left_text_edit.setReadOnly(True)
        self.right_text_edit.setReadOnly(True)

        # set the text
        self.left_text_edit.setPlainText(self.left_text)
        self.right_text_edit.setPlainText(self.right_text)

        # get the differences between the two texts and highlight them
        self.highlight_differences()

    def highlight_differences(self):
        # get the text from the text edits
        left_text = self.left_text_edit.toPlainText()
        right_text = self.right_text_edit.toPlainText()

        # get the differences between using difflib
        diff = difflib.ndiff(left_text.splitlines(), right_text.splitlines())

        # highlight the differences
        # TODO: review this
        last_sign = ""
        for index, line in enumerate(diff):
            if line.startswith("+"):
                self.left_text_edit.appendPlainText(line[2:])
                if next(diff, "").startswith("-"):
                    self.right_text_edit.appendPlainText("\n")
                last_sign = "+"
            elif line.startswith("-"):
                self.right_text_edit.appendPlainText(line[2:])
                if last_sign == "+":
                    self.left_text_edit.appendPlainText("\n")
                last_sign = "-"
            else:
                last_sign = " "
                self.left_text_edit.appendPlainText(line[2:])
                self.right_text_edit.appendPlainText(line[2:])

    def on_left_slider_moved(self, value: int):
        self.right_text_edit.verticalScrollBar().setValue(value)

    def on_right_slider_moved(self, value: int):
        if self.left_text_edit.verticalScrollBar().value() != value:
            self.left_text_edit.verticalScrollBar().setValue(value)


