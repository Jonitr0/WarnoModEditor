from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from diff_match_patch import diff_match_patch

from src.utils import icon_manager
from src.utils.color_manager import *

from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages.base_tab_page import BaseTabPage
from src.wme_widgets.tab_pages.diff_page import diff_code_editor


class FileComparisonPage(BaseTabPage):
    def __init__(self):
        super().__init__()
        self.prev_line_numbers_unequal = False

        self.left_text_edit = diff_code_editor.DiffCodeEditor()
        self.right_text_edit = diff_code_editor.DiffCodeEditor()

        self.setup_ui()

        self.help_file_path = "Help_FileComparisonPage.html"

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        self.find_action = tool_bar.addAction(icon_manager.load_icon("magnify.png", COLORS.PRIMARY), "Find (Ctrl + F)")
        self.find_action.setShortcut("Ctrl+F")
        self.find_action.setCheckable(True)
        # TODO: implement find
        #self.find_action.toggled.connect(self.on_find)

        # TODO: show left/right file actions with mod names

        # TODO: jump to previous/next diff actions

        text_edit_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(text_edit_layout)

        # add two text edits
        text_edit_layout.addWidget(self.left_text_edit)
        text_edit_layout.addWidget(self.right_text_edit)

        # connect slider slots
        self.left_text_edit.verticalScrollBar().valueChanged.connect(self.on_left_slider_moved)
        self.right_text_edit.verticalScrollBar().valueChanged.connect(self.on_right_slider_moved)

    def highlight_differences(self, left_text: str, right_text: str):
        main_widget.instance.show_loading_screen("Computing differences...")

        self.left_text_edit.setPlainText(left_text)
        self.right_text_edit.setPlainText(right_text)

        # calculate diffs with dmp
        dmp = diff_match_patch()
        a = dmp.diff_linesToChars(left_text, right_text)
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
                self.left_text_edit.highlight_lines(left_line_number, length, True)
                left_line_number += length
            # right
            elif status == 1:
                self.right_text_edit.highlight_lines(right_line_number, length, False)
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


