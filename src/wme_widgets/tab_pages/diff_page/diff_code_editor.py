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

    def add_line(self, text: str, mode: LineMode):
        # TODO: add line to editor
        # TODO: add line number to widget
        # TODO: add background color (extra selection)
        pass
