from PySide6 import QtGui, QtCore
from PySide6.QtCore import Qt

from src.utils.color_manager import *


# Based on: https://doc.qt.io/qt-6/qtwidgets-richtext-syntaxhighlighter-example.html

class HighlightingRule:
    pattern = None
    format = None
    single_line_comment = False

    def __init__(self):
        self.pattern = QtCore.QRegularExpression()
        self.format = QtGui.QTextCharFormat()


class NdfSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    highlighting_rules = []

    keywords = ["export", "is", "template", "unnamed", "nil", "private", "div"]
    types = ["vector", "map", "list", "int", "string", "true", "false", "bool", "rgba", "float"]

    def __init__(self, parent=None):
        super().__init__(parent)

        # L-value
        self.add_rule("\\w+\\s+(?=(is|=|\\:))", COLORS.L_VALUE)
        self.add_rule("(?<=template)\\s+\\w+", COLORS.L_VALUE)

        # keywords
        keyword_pattern = "\\b(" + self.keywords[0]
        for i in range(len(self.keywords)-1):
            keyword_pattern += "|" + self.keywords[i + 1]
        keyword_pattern += ")\\b"
        self.add_rule("\\b" + keyword_pattern + "\\b", COLORS.KEYWORDS, case_insensitive=True)

        # types
        type_pattern = "\\b(" + self.types[0]
        for i in range(len(self.types) - 1):
            type_pattern += "|" + self.types[i + 1]
        type_pattern += ")\\b"
        self.add_rule("\\b" + type_pattern + "\\b", COLORS.TYPES, case_insensitive=True)

        # integers
        self.add_rule("\\b[0-9]+\\b", COLORS.NUMBERS)

        # GUID
        self.add_rule("GUID:{[\\w-]+}", COLORS.NUMBERS)

        # strings
        self.add_rule("'.*?'", COLORS.STRINGS)
        self.add_rule("\".*?\"", COLORS.STRINGS)

        # single line comment
        self.add_rule("//[^\n]*", COLORS.SINGLE_COMMENT, italic=True, single_line_comment=True)

    def add_rule(self, pattern: str, color: COLORS, italic: bool = False, single_line_comment: bool = False,
                 case_insensitive: bool = False):
        rule = HighlightingRule()
        rule.format.setFontItalic(italic)
        rule.format.setForeground(QtGui.QColor(get_color_for_key(color.value)))
        rule.pattern = QtCore.QRegularExpression(pattern)
        if case_insensitive:
            rule.pattern.setPatternOptions(QtCore.QRegularExpression.CaseInsensitiveOption)
        rule.single_line_comment = single_line_comment
        self.highlighting_rules.append(rule)

    def highlightBlock(self, text: str):
        # apply basic rules
        for rule in self.highlighting_rules:
            iterator = rule.pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)

