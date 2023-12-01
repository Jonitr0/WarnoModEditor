from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from src.utils.color_manager import *

from src.wme_widgets.tab_pages.text_editor_page import wme_code_editor


class DiffCodeEditor(wme_code_editor.WMECodeEditor):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)
        self.setLineWrapMode(QtWidgets.QPlainTextEdit.WidgetWidth)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.left_marking_color = COLORS.LEFT_ICON
        self.right_marking_color = COLORS.RIGHT_ICON

        self.left_highlight_color = COLORS.LEFT_HIGHLIGHT
        self.right_highlight_color = COLORS.RIGHT_HIGHLIGHT

    def add_empty_lines(self, pos: int, num: int):
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor, pos)
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.MoveAnchor)
        cursor.insertText("\n" * num)

    def highlight_lines(self, pos: int, num: int, left: bool):
        # add extra selections to the given lines
        extra_selections = self.extraSelections()

        if left:
            marking_color = self.left_marking_color
            highlight_color = self.left_highlight_color
        else:
            marking_color = self.right_marking_color
            highlight_color = self.right_highlight_color

        cursor = self.textCursor()
        block = self.document().findBlockByLineNumber(pos)
        cursor.setPosition(block.position())
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)
        # move cursor for length lines
        for i in range(num):
            cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.KeepAnchor)
            cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)
            self.add_marking(pos + i, marking_color)

        extra_selection = QtWidgets.QTextEdit.ExtraSelection()
        extra_selection.cursor = cursor
        extra_selection.format.setBackground(QtGui.QColor(get_color_for_key(highlight_color.value)))
        extra_selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        extra_selection.format.setForeground(QtGui.QColor(get_color_for_key(COLORS.SECONDARY_TEXT.value)))
        extra_selections.append(extra_selection)

        self.setExtraSelections(extra_selections)

    def next_find_after_cursor(self) -> int:
        # get current cursor position
        pos = self.textCursor().position()
        for find, _ in self.find_results:
            if find > pos:
                return find
        return -1

    def prev_find_before_cursor(self) -> int:
        # get current cursor position
        pos = self.textCursor().position()
        for find, _ in reversed(self.find_results):
            if find < pos:
                return find
        return -1

    def get_next_diff_line(self, start_pos: int = 0):
        target = -1
        for line, color_list in self.marking_area.lines_to_marking_colors.items():
            if line > start_pos and (self.left_marking_color in color_list or self.right_marking_color in color_list) \
                    and (line < target or target == -1):
                target = line
        return target

    def get_prev_diff_line(self, start_pos: int = 0):
        target = -1
        for line, color_list in reversed(self.marking_area.lines_to_marking_colors.items()):
            if line < start_pos and (self.left_marking_color in color_list or self.right_marking_color in color_list) \
                    and (line > target or target == -1):
                target = line
        return target

    def set_cursor_line(self, line: int):
        cursor = self.textCursor()
        line_pos = self.document().findBlockByLineNumber(line).position()
        cursor.setPosition(line_pos, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def get_cursor_line(self):
        return self.textCursor().blockNumber()

