from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from diff_match_patch import diff_match_patch

from src.utils import icon_manager
from src.utils.color_manager import *

from src.wme_widgets import main_widget
from src.wme_widgets.tab_pages.base_tab_page import BaseTabPage
from src.wme_widgets.tab_pages.diff_page import diff_code_editor
from src.wme_widgets.tab_pages.text_editor_page import wme_find_replace_bar


class FileComparisonPage(BaseTabPage):
    def __init__(self):
        super().__init__()
        self.find_bar = wme_find_replace_bar.FindBar(self)
        self.prev_line_numbers_unequal = False
        self.first_find_finished = False

        self.left_text_edit = diff_code_editor.DiffCodeEditor()
        self.right_text_edit = diff_code_editor.DiffCodeEditor()

        self.setup_ui()

        # TODO: write this
        self.help_file_path = "Help_FileComparisonPage.html"

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar_layout = QtWidgets.QHBoxLayout()
        tool_bar_layout.setContentsMargins(0, 0, 0, 0)
        tool_bar_layout.setSpacing(0)
        main_layout.addLayout(tool_bar_layout)

        named_tool_bar = QtWidgets.QToolBar()
        named_tool_bar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        tool_bar_layout.addWidget(named_tool_bar)

        self.display_left_action = named_tool_bar.addAction(icon_manager.load_icon("text_file.png", COLORS.PRIMARY),
                                                            "Toggle left file")
        self.display_left_action.setText("left mod")
        self.display_left_action.setCheckable(True)
        self.display_left_action.setChecked(True)
        self.display_left_action.setToolTip("Toggle Left File")
        self.display_left_action.triggered.connect(self.toggle_left)

        self.display_right_action = named_tool_bar.addAction(icon_manager.load_icon("text_file.png", COLORS.PRIMARY),
                                                             "Toggle right file")
        self.display_right_action.setText("right mod")
        self.display_right_action.setCheckable(True)
        self.display_right_action.setChecked(True)
        self.display_right_action.setToolTip("Toggle Right File")
        self.display_right_action.triggered.connect(self.toggle_right)

        named_tool_bar.addSeparator()

        icon_tool_bar = QtWidgets.QToolBar()
        tool_bar_layout.addWidget(icon_tool_bar)

        self.find_action = icon_tool_bar.addAction(icon_manager.load_icon("magnify.png", COLORS.PRIMARY),
                                                   "Find (Ctrl + F)")
        self.find_action.setShortcut("Ctrl+F")
        self.find_action.setCheckable(True)
        self.find_action.toggled.connect(self.on_find)

        icon_tool_bar.addSeparator()

        next_diff_action = icon_tool_bar.addAction(icon_manager.load_icon("arrow_down.png", COLORS.PRIMARY),
                                                   "Next diff (Ctrl + Arrow Down)")
        next_diff_action.setShortcut("Ctrl+Down")
        next_diff_action.triggered.connect(self.on_next_diff)

        prev_diff_action = icon_tool_bar.addAction(icon_manager.load_icon("arrow_up.png", COLORS.PRIMARY),
                                                   "Previous diff (Ctrl + Arrow Up)")
        prev_diff_action.setShortcut("Ctrl+Up")
        prev_diff_action.triggered.connect(self.on_prev_diff)

        self.link_cursor_action = icon_tool_bar.addAction(icon_manager.load_icon("link_cursor.png", COLORS.PRIMARY),
                                                          "Link text cursors")
        self.link_cursor_action.setCheckable(True)
        self.link_cursor_action.setChecked(True)
        self.link_cursor_action.triggered.connect(lambda checked: self.synchronize_cursors() if checked else None)

        stretch = QtWidgets.QWidget()
        stretch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        icon_tool_bar.addWidget(stretch)

        help_action = icon_tool_bar.addAction(icon_manager.load_icon("help.png", COLORS.PRIMARY),
                                              "Open Page Help Popup (Alt + H)")
        help_action.triggered.connect(self.on_help)

        main_layout.addWidget(self.find_bar)
        self.find_bar.setVisible(False)
        self.find_bar.request_find_pattern.connect(self.find_pattern)
        self.find_bar.request_find_reset.connect(self.reset_find)
        self.find_bar.case_sensitivity_changed.connect(self.set_case_sensitive_search)
        self.find_bar.request_uncheck.connect(self.on_find_bar_close)
        self.find_bar.request_next.connect(self.on_find_bar_next)
        self.find_bar.request_prev.connect(self.on_find_bar_prev)

        text_edit_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(text_edit_layout)

        # add two text edits
        text_edit_layout.addWidget(self.left_text_edit)
        text_edit_layout.addWidget(self.right_text_edit)

        self.left_text_edit.search_complete.connect(self.on_search_complete)
        self.right_text_edit.search_complete.connect(self.on_search_complete)

        self.left_text_edit.cursorPositionChanged.connect(lambda: self.synchronize_cursors()
            if self.link_cursor_action.isChecked() else None)
        self.right_text_edit.cursorPositionChanged.connect(lambda: self.synchronize_cursors(False)
            if self.link_cursor_action.isChecked() else None)

        # connect slider slots
        self.left_text_edit.verticalScrollBar().valueChanged.connect(self.on_left_slider_moved)
        self.right_text_edit.verticalScrollBar().valueChanged.connect(self.on_right_slider_moved)
        self.left_text_edit.verticalScrollBar().sliderMoved.connect(self.on_left_slider_moved)
        self.right_text_edit.verticalScrollBar().sliderMoved.connect(self.on_right_slider_moved)

    def highlight_differences(self, left_text: str, right_text: str, left_mod: str, right_mod: str):
        main_widget.instance.show_loading_screen("Computing differences...")

        self.left_text_edit.setPlainText(left_text)
        self.right_text_edit.setPlainText(right_text)

        self.display_left_action.setText(left_mod)
        self.display_right_action.setText(right_mod)

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
        # TODO: make sure sliders only both move when cursors are synchronized
        self.right_text_edit.verticalScrollBar().setValue(value)

    def on_right_slider_moved(self, value: int):
        if self.left_text_edit.verticalScrollBar().value() != value:
            self.left_text_edit.verticalScrollBar().setValue(value)

    def toggle_left(self):
        self.left_text_edit.setVisible(self.display_left_action.isChecked())

        if (not self.left_text_edit.isVisible()) and (not self.right_text_edit.isVisible()):
            self.display_right_action.setChecked(True)
            self.toggle_right()

    def toggle_right(self):
        self.right_text_edit.setVisible(self.display_right_action.isChecked())

        if (not self.left_text_edit.isVisible()) and (not self.right_text_edit.isVisible()):
            self.display_left_action.setChecked(True)
            self.toggle_left()

    def on_find(self, checked: bool):
        selection = ""
        if self.left_text_edit.isVisible() and self.left_text_edit.get_selected_text() != "":
            selection = self.left_text_edit.get_selected_text()
        elif self.right_text_edit.isVisible() and self.right_text_edit.get_selected_text() != "":
            selection = self.right_text_edit.get_selected_text()

        if checked:
            self.find_bar.setHidden(False)
            self.find_bar.line_edit.setFocus()
            # if editor has selection, search for it
            self.find_bar.line_edit.setText(selection)
            self.left_text_edit.find_pattern(selection)
            self.right_text_edit.find_pattern(selection)
            if len(self.left_text_edit.find_results) > 0:
                self.left_text_edit.goto_prev_find()
            if len(self.right_text_edit.find_results) > 0:
                self.right_text_edit.goto_prev_find()
        elif len(selection) > 0:
            self.find_action.setChecked(True)
        else:
            self.find_bar.reset()

    def find_pattern(self, pattern: str):
        self.first_find_finished = False
        self.left_text_edit.find_pattern(pattern, True)
        self.right_text_edit.find_pattern(pattern, True)

    def reset_find(self):
        self.left_text_edit.reset_find()
        self.right_text_edit.reset_find()

    def set_case_sensitive_search(self, case_sensitive: bool):
        self.left_text_edit.set_case_sensitive_search(case_sensitive)
        self.right_text_edit.set_case_sensitive_search(case_sensitive)

    def on_find_bar_close(self):
        self.find_action.setChecked(False)
        self.find_bar.setHidden(True)
        self.reset_find()

    def on_find_bar_next(self):
        if self.left_text_edit.isVisible() and self.left_text_edit.next_find_after_cursor() > 0:
            self.left_text_edit.goto_next_find()
            self.on_left_slider_moved(self.left_text_edit.verticalScrollBar().value())
        elif self.right_text_edit.isVisible() and self.right_text_edit.next_find_after_cursor() > 0:
            self.right_text_edit.goto_next_find()
            self.on_right_slider_moved(self.right_text_edit.verticalScrollBar().value())
        elif self.left_text_edit.isVisible() and len(self.left_text_edit.find_results) > 0:
            self.left_text_edit.goto_next_find()
            self.on_left_slider_moved(self.left_text_edit.verticalScrollBar().value())
        elif self.right_text_edit.isVisible() and len(self.right_text_edit.find_results) > 0:
            self.right_text_edit.goto_next_find()
            self.on_right_slider_moved(self.right_text_edit.verticalScrollBar().value())

    def on_find_bar_prev(self):
        if self.left_text_edit.isVisible() and self.left_text_edit.prev_find_before_cursor() > 0:
            self.left_text_edit.goto_prev_find()
            self.on_left_slider_moved(self.left_text_edit.verticalScrollBar().value())
        elif self.right_text_edit.isVisible() and self.right_text_edit.prev_find_before_cursor() > 0:
            self.right_text_edit.goto_prev_find()
            self.on_right_slider_moved(self.right_text_edit.verticalScrollBar().value())
        elif self.left_text_edit.isVisible() and len(self.left_text_edit.find_results) > 0:
            self.left_text_edit.goto_prev_find()
            self.on_left_slider_moved(self.left_text_edit.verticalScrollBar().value())
        elif self.right_text_edit.isVisible() and len(self.right_text_edit.find_results) > 0:
            self.right_text_edit.goto_prev_find()
            self.on_right_slider_moved(self.right_text_edit.verticalScrollBar().value())

    def on_search_complete(self):
        if not self.first_find_finished:
            self.first_find_finished = True
            return

        results = len(self.left_text_edit.get_find_results() + self.right_text_edit.get_find_results())
        if results == 0:
            self.find_bar.set_label_text("0 results for \"" + self.find_bar.line_edit.text() + "\" in both files")
            self.find_bar.enable_find_buttons(False)
        else:
            self.find_bar.set_label_text(str(results) + " results for \"" + self.find_bar.line_edit.text() +
                                         "\" in both files")
            self.find_bar.enable_find_buttons(True)
            if self.left_text_edit.isVisible():
                self.left_text_edit.setFocus()
            elif self.right_text_edit.isVisible():
                self.right_text_edit.setFocus()

    def on_next_diff(self):
        # take left cursor line as starting point
        if self.left_text_edit.isVisible():
            start = self.left_text_edit.textCursor().blockNumber()
        else:
            start = self.right_text_edit.textCursor().blockNumber()

        # get next diff for both editors
        left_diff = -1
        right_diff = -1
        if self.left_text_edit.isVisible():
            left_diff = self.left_text_edit.get_next_diff_line(start)
        if self.right_text_edit.isVisible():
            right_diff = self.right_text_edit.get_next_diff_line(start)

        while True:
            if left_diff > -1 ^ right_diff > -1:
                target = max(left_diff, right_diff)
                break
            elif left_diff > -1 and right_diff > -1:
                target = min(left_diff, right_diff)
                break
            else:
                if self.left_text_edit.isVisible():
                    left_diff = self.left_text_edit.get_next_diff_line(0)
                if self.right_text_edit.isVisible():
                    right_diff = self.right_text_edit.get_next_diff_line(0)
                if left_diff == -1 and right_diff == -1:
                    return

        if self.left_text_edit.isVisible():
            self.left_text_edit.set_cursor_line(target)
        if self.right_text_edit.isVisible():
            self.right_text_edit.set_cursor_line(target)

    def on_prev_diff(self):
        # take left cursor line as starting point
        if self.left_text_edit.isVisible():
            start = self.left_text_edit.textCursor().blockNumber()
        else:
            start = self.right_text_edit.textCursor().blockNumber()

        # get prev diff for both editors
        left_diff = -1
        right_diff = -1
        if self.left_text_edit.isVisible():
            left_diff = self.left_text_edit.get_prev_diff_line(start)
        if self.right_text_edit.isVisible():
            right_diff = self.right_text_edit.get_prev_diff_line(start)

        while True:
            if left_diff > -1 or right_diff > -1:
                target = max(left_diff, right_diff)
                break
            else:
                if self.left_text_edit.isVisible():
                    left_diff = self.left_text_edit.get_prev_diff_line(self.left_text_edit.document().blockCount())
                if self.right_text_edit.isVisible():
                    right_diff = self.right_text_edit.get_prev_diff_line(self.left_text_edit.document().blockCount())
                if left_diff == -1 and right_diff == -1:
                    return

        if self.left_text_edit.isVisible():
            self.left_text_edit.set_cursor_line(target)
        if self.right_text_edit.isVisible():
            self.right_text_edit.set_cursor_line(target)

    def synchronize_cursors(self, ref_left: bool = True):
        if self.left_text_edit.get_cursor_pos() == self.right_text_edit.get_cursor_pos():
            return

        if ref_left:
            target_pos = self.left_text_edit.get_cursor_pos()
        else:
            target_pos = self.right_text_edit.get_cursor_pos()

        # check if lines for target position are equal
        left_target_line = self.left_text_edit.document().findBlock(target_pos).blockNumber()
        right_target_line = self.right_text_edit.document().findBlock(target_pos).blockNumber()

        if left_target_line == right_target_line:
            self.left_text_edit.set_cursor_pos(target_pos)
            self.right_text_edit.set_cursor_pos(target_pos)
        else:
            if self.left_text_edit.get_cursor_line() == self.right_text_edit.get_cursor_line():
                return
            if ref_left:
                self.left_text_edit.set_cursor_pos(target_pos)
                self.right_text_edit.set_cursor_line(left_target_line)
            else:
                self.left_text_edit.set_cursor_line(right_target_line)
                self.right_text_edit.set_cursor_pos(target_pos)

    def to_json(self) -> dict:
        return {"do_not_restore": True}
