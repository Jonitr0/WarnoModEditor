from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from diff_match_patch import diff_match_patch

from src.wme_widgets import main_widget
from src.utils.color_manager import *
from src.wme_widgets.tab_pages.base_tab_page import BaseTabPage
from src.wme_widgets.tab_pages.diff_page import diff_code_editor


class FileComparisonPage(BaseTabPage):
    # TODO: mod name labels
    # TODO: hide/show buttons
    # TODO: search bar
    # TODO: jump through diffs
    def __init__(self, left_text: str, right_text: str):
        super().__init__()
        self.prev_line_numbers_unequal = False
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)

        self.left_text_edit = diff_code_editor.DiffCodeEditor()
        self.right_text_edit = diff_code_editor.DiffCodeEditor()

        self.left_text = left_text
        self.right_text = right_text

        self.setup_ui()

        self.help_file_path = "Help_FileComparisonPage.html"

    def setup_ui(self):
        # add two text edits
        self.main_layout.addWidget(self.left_text_edit)
        self.main_layout.addWidget(self.right_text_edit)

        # connect slider slots
        self.left_text_edit.verticalScrollBar().valueChanged.connect(self.on_left_slider_moved)
        self.right_text_edit.verticalScrollBar().valueChanged.connect(self.on_right_slider_moved)

        # get the differences between the two texts and highlight them
        self.highlight_differences()

    def highlight_differences(self):
        main_widget.instance.show_loading_screen("Computing differences...")

        self.left_text_edit.setPlainText(self.left_text)
        self.right_text_edit.setPlainText(self.right_text)

        # calculate diffs with dmp
        dmp = diff_match_patch()
        a = dmp.diff_linesToChars(self.left_text, self.right_text)
        line_text_left = a[0]
        line_text_right = a[1]
        diffs = dmp.diff_main(line_text_left, line_text_right, False)

        left_line_number = 0
        right_line_number = 0

        for index, diff in enumerate(diffs):
            status = diff[0]
            length = int(len(diff[1].encode('utf-16-le')) / 2)

            if status == 0:
                left_line_number += length
                right_line_number += length
            # left
            elif status == -1:
                self.left_text_edit.highlight_lines(left_line_number, length, self.left_text_edit.left_marking_color)
                left_line_number += length
            # right
            elif status == 1:
                self.right_text_edit.highlight_lines(right_line_number, length,
                                                     self.right_text_edit.right_marking_color)
                right_line_number += length

            if self.prev_line_numbers_unequal and left_line_number != right_line_number:
                start_line = right_line_number - length
                if left_line_number > right_line_number:
                    num_lines = left_line_number - right_line_number
                    self.right_text_edit.add_empty_lines(start_line, num_lines)
                    right_line_number = left_line_number
                else:
                    num_lines = right_line_number - left_line_number
                    self.left_text_edit.add_empty_lines(start_line, num_lines)
                    left_line_number = right_line_number

            self.prev_line_numbers_unequal = left_line_number != right_line_number

        main_widget.instance.hide_loading_screen()

    def get_relative_diff(self, diffs: list, index: int, offset: int):
        if not 0 < index + offset < len(diffs):
            return None
        relative_diff = diffs[index + offset]
        return relative_diff[0], int(len(relative_diff[1].encode('utf-16-le')) / 2)

    def on_left_slider_moved(self, value: int):
        self.right_text_edit.verticalScrollBar().setValue(value)

    def on_right_slider_moved(self, value: int):
        if self.left_text_edit.verticalScrollBar().value() != value:
            self.left_text_edit.verticalScrollBar().setValue(value)


