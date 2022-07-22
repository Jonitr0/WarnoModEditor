from PySide2 import QtGui, QtCore
from PySide2.QtCore import Qt

# Based on: https://doc.qt.io/qt-6/qtwidgets-richtext-syntaxhighlighter-example.html

class HighlightingRule:
    pattern = QtCore.QRegularExpression()
    format = QtGui.QTextCharFormat()


class NdfSyntaxHighlighter(QtGui.QSyntaxHighlighter):
    highlighting_rules = []

    multiline_comment_starts = ["{", "(*", "/*"]
    multiline_comment_ends = ["}", "*)", "*/"]
    multiline_comment_format = QtGui.QTextCharFormat()

    def __init__(self, parent=None):
        super().__init__(parent)

        single_comment_rule = HighlightingRule()
        single_comment_rule.format.setFontItalic(True)
        single_comment_rule.format.setForeground(Qt.lightGray)
        single_comment_rule.pattern = QtCore.QRegularExpression("//[^\n]*")
        self.highlighting_rules.append(single_comment_rule)

        self.multiline_comment_format.setFontItalic(True)
        self.multiline_comment_format.setForeground(Qt.green)

    def highlightBlock(self, text: str):
        # apply basic rules
        for rule in self.highlighting_rules:
            iterator = rule.pattern.globalMatch(text)
            while iterator.hasNext():
                match = iterator.next()
                self.setFormat(match.capturedStart(), match.capturedLength(), rule.format)

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

        while start_index >= 0:
            end_index = -1
            cap_size = 0
            for end in self.multiline_comment_ends:
                try:
                    cap = text.index(end, start_index)
                    end_index = max(cap, end_index)
                    if cap > end_index:
                        cap_size = len(end)
                except ValueError:
                    pass
            comment_length = 0
            # if no comment is found
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



