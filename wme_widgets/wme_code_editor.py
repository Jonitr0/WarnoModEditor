from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt
from utils.color_manager import *
from utils import ndf_syntax_highlighter


# Based on: https://stackoverflow.com/questions/33243852/codeeditor-example-in-pyqt

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
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.highlightCurrentLine)
        self.cursorPositionChanged.connect(self.mark_finds_in_viewport)

        self.updateLineNumberAreaWidth(0)
        self.pattern = ""
        self.change_length = 0
        self.change_pos = -1
        self.about_to_change_format = False
        self.find_results = []
        self.drawn_results = []

        self.find_format = QtGui.QTextCharFormat()
        self.find_format.setBackground(QtGui.QColor(get_color(COLORS.FIND_HIGHLIGHT.value)))

        self.verticalScrollBar().valueChanged.connect(self.mark_finds_in_viewport)
        self.document().contentsChange.connect(self.update_search)

        highlighter = ndf_syntax_highlighter.NdfSyntaxHighlighter(self.document())
        # TODO: update search on text changed

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

        self.mark_finds_in_viewport()

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

    def find_pattern(self, pattern, updating=False):
        self.reset_find()
        self.pattern = pattern

        if pattern == "":
            return

        start = 0
        text = self.toPlainText()

        while True:
            start = text.find(pattern, start)
            if start < 0:
                break

            self.find_results.append((start, start + len(pattern)))

            start += len(pattern)

        self.mark_finds_in_viewport()
        self.search_complete.emit()
        if not updating:
            self.goto_next_find()

    def reset_find(self):
        if len(self.find_results) == 0:
            return

        cursor = self.textCursor()
        clear_format = QtGui.QTextCharFormat()
        clear_format.setBackground(Qt.transparent)

        length = self.find_results[0][1] - self.find_results[0][0]

        for drawn in self.drawn_results:
            # if we changed an existing find, make the clear area longer
            if drawn <= self.change_pos <= drawn + length:
                length += self.change_length

            cursor.setPosition(drawn, QtGui.QTextCursor.MoveAnchor)
            cursor.setPosition(drawn + length, QtGui.QTextCursor.KeepAnchor)
            self.about_to_change_format = True
            cursor.mergeCharFormat(clear_format)

            # reset length
            if drawn <= self.change_pos <= drawn + length:
                length -= self.change_length

        self.find_results = []
        self.drawn_results = []

    def get_find_results(self):
        return self.find_results

    def mark_finds_in_viewport(self):
        # nothing to do if all results are drawn
        if len(self.find_results) == len(self.drawn_results):
            return

        cursor = self.cursorForPosition(QtCore.QPoint(0, 0))
        bottom_right = QtCore.QPoint(self.viewport().width() - 1, self.viewport().height() - 1)
        end_pos = self.cursorForPosition(bottom_right).position()
        cursor.setPosition(end_pos, QtGui.QTextCursor.KeepAnchor)

        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        # check all results
        for find in self.find_results:
            if find[0] > end:
                break
            # draw those in viewport that are not already drawn
            elif find[0] >= start and not self.drawn_results.__contains__(find[0]):
                cursor.setPosition(find[0], QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(find[1], QtGui.QTextCursor.KeepAnchor)
                self.about_to_change_format = True
                cursor.mergeCharFormat(self.find_format)

                self.drawn_results.append(find[0])

    def goto_next_find(self):
        if len(self.find_results) == 0:
            return

        cursor = self.textCursor()
        index = cursor.position()

        for find in self.find_results:
            if index < find[0]:
                cursor.setPosition(find[0], QtGui.QTextCursor.MoveAnchor)
                self.setTextCursor(cursor)
                self.setFocus()
                return

        # if no position was set yet, set it to the first find
        cursor.setPosition(self.find_results[0][0], QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)
        self.setFocus()

    def goto_prev_find(self):
        if len(self.find_results) == 0:
            return

        cursor = self.textCursor()
        index = cursor.position()

        # if index is lower than first find, set it to the last one
        if index <= self.find_results[0][1]:
            cursor.setPosition(self.find_results[len(self.find_results) - 1][0], QtGui.QTextCursor.MoveAnchor)
            self.setTextCursor(cursor)
            self.setFocus()
            return

        last_find = -1
        for find in self.find_results:
            if index <= find[1] and last_find > 0:
                cursor.setPosition(last_find, QtGui.QTextCursor.MoveAnchor)
                self.setTextCursor(cursor)
                self.setFocus()
                return
            last_find = find[0]

    def update_search(self, pos: int, _: int, added: int):
        if self.about_to_change_format:
            self.about_to_change_format = False
            return

        self.change_length = added
        self.change_pos = pos

        self.find_pattern(self.pattern, updating=True)
        self.mark_finds_in_viewport()
        self.about_to_change_format = False

        self.change_length = 0
        self.change_pos = -1
