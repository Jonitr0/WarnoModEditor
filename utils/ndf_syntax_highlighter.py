from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt


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

    # NDF Reference claims {} are comment delimiters, yet they are used in GUID
    multiline_comment_starts = ["(*", "/*"]
    multiline_comment_ends = ["*)", "*/"]
    multiline_comment_format = QtGui.QTextCharFormat()

    keywords = ["export", "is", "template", "unnamed", "nil", "private", "int", "string", "true", "false", "div", "map"]

    def __init__(self, parent=None):
        super().__init__(parent)

        # keywords
        for keyword in self.keywords:
            self.add_rule("\\b" + keyword + "\\b", Qt.red, case_insensitive=True)

        # single line comment
        self.add_rule("//[^\n]*", Qt.lightGray, italic=True, single_line_comment=True)

        # integers
        self.add_rule("\\b[0-9]+\\b", Qt.blue)

        # strings
        self.add_rule("'.*?'", Qt.green)

        self.multiline_comment_format.setFontItalic(True)
        self.multiline_comment_format.setForeground(Qt.green)

    def add_rule(self, pattern: str, color: QtGui.QColor, italic: bool = False, single_line_comment: bool = False,
                 case_insensitive: bool = False):
        rule = HighlightingRule()
        rule.format.setFontItalic(italic)
        rule.format.setForeground(color)
        rule.pattern = QtCore.QRegularExpression(pattern)
        if case_insensitive:
            rule.pattern.setPatternOptions(QtCore.QRegularExpression.CaseInsensitiveOption)
        rule.single_line_comment = single_line_comment
        self.highlighting_rules.append(rule)

    def highlightBlock(self, text: str):
        # save potential single line comment start
        single_line_comment_start = -1
        # apply basic rules
        for rule in self.highlighting_rules:
            iterator = rule.pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)
                if rule.single_line_comment:
                    single_line_comment_start = match.capturedStart()

        # set block state to 0, "not in comment"
        self.setCurrentBlockState(0)

        # search for a possible comment start
        start_index = -1
        if self.previousBlockState() != 1:
            for start in self.multiline_comment_starts:
                try:
                    start_index = max(text.index(start), start_index)
                except ValueError:
                    pass
            # ignore if it's in a single line comment
            if start_index > -1 and start_index > single_line_comment_start >= 0:
                start_index = -1
        else:
            start_index = 0

        while start_index >= 0:

            end_index = -1
            cap_size = 0
            for end in self.multiline_comment_ends:
                try:
                    cap = text.index(end, start_index)
                    if cap > end_index:
                        cap_size = len(end)
                    end_index = max(cap, end_index)
                except ValueError:
                    pass
            # if no comment end is found
            if end_index == -1:
                self.setCurrentBlockState(1)
                comment_length = len(text) - start_index
            else:
                comment_length = end_index - start_index + cap_size
            self.setFormat(start_index, comment_length, self.multiline_comment_format)
            start_index = -1
            for start in self.multiline_comment_starts:
                try:
                    start_index = text.index(start, start_index + comment_length)
                except ValueError:
                    pass
