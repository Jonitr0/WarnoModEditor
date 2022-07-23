from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from utils.color_manager import *
from utils import ndf_syntax_highlighter

# Based on: https://stackoverflow.com/questions/33243852/codeeditor-example-in-pyqt
# and https://stackoverflow.com/a/70881305


class LineNumberArea(QtWidgets.QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class WMECodeEditor(QtWidgets.QPlainTextEdit):
    search_complete = QtCore.Signal()

    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.setObjectName("code_editor")

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)

        self.updateLineNumberAreaWidth(0)
        self.find_results = []

        highlighter = ndf_syntax_highlighter.NdfSyntaxHighlighter(self.document())

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 4 + self.fontMetrics().width('9') * digits
        return max(32, space)

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, 0, 0)

    def updateLineNumberArea(self, rect, dy):

        if dy:
            self.lineNumberArea.scroll(0, dy)
        else:
            self.lineNumberArea.update(0, rect.y(), self.lineNumberArea.width(),
                                       rect.height())

        if rect.contains(self.viewport().rect()):
            self.updateLineNumberAreaWidth(0)

    def resizeEvent(self, event):
        super().resizeEvent(event)

        cr = self.contentsRect()
        self.lineNumberArea.setGeometry(QtCore.QRect(cr.left(), cr.top(),
                                                     self.lineNumberAreaWidth(), cr.height()))

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.lineNumberArea)

        line_number_area_color = get_color(COLORS.SECONDARY_DARK.value)
        painter.fillRect(event.rect(), line_number_area_color)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)
                line_number_text_color = get_color(COLORS.SECONDARY_TEXT.value)
                painter.setPen(line_number_text_color)
                painter.drawText(0, top, self.lineNumberArea.width(), height,
                                 Qt.AlignLeft, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def highlightCurrentLine(self):
        extra_selections = []

        if not self.isReadOnly():
            selection = QtWidgets.QTextEdit.ExtraSelection()

            line_color = QtGui.QColor(get_color(COLORS.SECONDARY_LIGHT.value))

            selection.format.setBackground(line_color)
            selection.format.setProperty(QtGui.QTextFormat.FullWidthSelection, True)
            selection.cursor = self.textCursor()
            selection.cursor.clearSelection()
            extra_selections.append(selection)
        self.setExtraSelections(extra_selections)

    def find_pattern(self, pattern):
        # TODO: maks sure pattern is not interpreted as regex
        self.reset_find()

        if pattern == "":
            return

        cursor = self.textCursor()
        # Setup the desired format for matches
        find_format = QtGui.QTextCharFormat()
        find_format.setBackground(Qt.darkGreen)

        # Setup the regex engine
        re = QtCore.QRegularExpression(pattern)
        i = re.globalMatch(self.toPlainText())  # QRegularExpressionMatchIterator

        # iterate through all the matches and highlight
        while i.hasNext():
            match = i.next()  # QRegularExpressionMatch

            self.find_results.append((match.capturedStart(), match.capturedEnd()))

            # Select the matched text and apply the desired format
            cursor.setPosition(match.capturedStart(), QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(match.capturedEnd(), QtGui.QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(find_format)

        self.search_complete.emit()

    def reset_find(self):
        cursor = self.textCursor()
        clear_format = QtGui.QTextCharFormat()
        clear_format.setBackground(Qt.transparent)

        for find in self.find_results:
            cursor.setPosition(find[0], QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(find[1], QtGui.QTextCursor.KeepAnchor)
            cursor.mergeCharFormat(clear_format)

        self.find_results = []

    def get_find_results(self):
        return self.find_results
