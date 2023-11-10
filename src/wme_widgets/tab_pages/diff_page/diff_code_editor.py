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

    def add_empty_lines(self, pos: int, num: int):
        cursor = self.textCursor()
        cursor.movePosition(QtGui.QTextCursor.Start)
        cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor, pos)
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.MoveAnchor)
        cursor.insertText("\n" * num)

    def highlight_lines(self, pos: int, num: int, color: COLORS):
        # add extra selections to the given lines
        extra_selections = self.extraSelections()

        cursor = self.textCursor()
        block = self.document().findBlockByLineNumber(pos)
        cursor.setPosition(block.position())
        cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.KeepAnchor)
        # move cursor for length lines
        for i in range(num):
            cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.KeepAnchor)
            cursor.movePosition(QtGui.QTextCursor.StartOfLine, QtGui.QTextCursor.KeepAnchor)
            self.add_marking(pos + i, color)

        extra_selection = QtWidgets.QTextEdit.ExtraSelection()
        extra_selection.cursor = cursor
        extra_selection.format.setBackground(QtGui.QColor(get_color_for_key(color.value)))
        extra_selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        extra_selections.append(extra_selection)

        self.setExtraSelections(extra_selections)
