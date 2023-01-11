from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from enum import Enum

from src.utils.color_manager import *
from src.wme_widgets.tab_pages.text_editor_page import ndf_syntax_highlighter


class LineMode(Enum):
    UNCHANGED = 0
    LEFT = 1
    RIGHT = 2


class DiffCodeEditor(QtWidgets.QPlainTextEdit):
    def __init__(self):
        super().__init__()
        self.setObjectName("code_editor")
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)
        self.setReadOnly(True)

        highlighter = ndf_syntax_highlighter.NdfSyntaxHighlighter(self.document())

        self.textChanged.connect(self.on_text_changed)

    def on_text_changed(self):
        s = self.document().size().toSize()
        font_height = self.fontMetrics().height() - 1
        self.setFixedHeight((s.height() + 1) * font_height)

    def add_line(self, text: str, mode: LineMode):
        text = text.removesuffix("\n")
        text = text.removesuffix("\r")
        if mode == 0:
            text = "  " + text
        elif mode == 1:
            text = "+ " + text
        elif mode == 2:
            text = "- " + text

        self.appendPlainText(text)
        # TODO: add line number to widget

        # no extra selections
        if mode == 0:
            return

        extra_selections = self.extraSelections()
        # prepare selection format
        selection_format = QtGui.QTextCharFormat()
        selection_format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
        # prepare selection cursor
        selection_cursor = self.textCursor()
        selection_cursor.movePosition(QtGui.QTextCursor.StartOfBlock)
        selection_cursor.clearSelection()
        # left
        if mode == 1:
            left_color = get_color_for_key(COLORS.LEFT_HIGHLIGHT.value)
            selection_format.setBackground(QtGui.QColor(left_color))
        # right
        elif mode == 2:
            right_color = get_color_for_key(COLORS.RIGHT_HIGHLIGHT.value)
            selection_format.setBackground(QtGui.QColor(right_color))

        selection = QtWidgets.QTextEdit.ExtraSelection()
        selection.format = selection_format
        selection.cursor = selection_cursor
        extra_selections.append(selection)

        self.setExtraSelections(extra_selections)

