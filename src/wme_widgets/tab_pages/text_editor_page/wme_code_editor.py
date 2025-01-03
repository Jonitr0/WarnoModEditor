from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.utils.color_manager import *
from src.wme_widgets import wme_essentials
from src.wme_widgets.tab_pages.text_editor_page import ndf_syntax_highlighter
from src.dialogs import insert_string_dialog

import uuid


# Based on: https://stackoverflow.com/questions/33243852/codeeditor-example-in-pyqt

class LineNumberArea(QtWidgets.QWidget):

    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QtCore.QSize(self.editor.lineNumberAreaWidth(), 0)

    def paintEvent(self, event):
        self.editor.lineNumberAreaPaintEvent(event)


class MarkingArea(QtWidgets.QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor
        self.w = 16
        self.lines_to_marking_colors = {}

    def sizeHint(self):
        width = self.w
        if self.editor.verticalScrollBar().isVisible():
            width += self.editor.verticalScrollBar().width()
        return QtCore.QSize(width, 0)

    def paintEvent(self, event):
        self.editor.markingAreaPaintEvent(event)


class WMECodeEditor(QtWidgets.QPlainTextEdit):
    search_complete = QtCore.Signal()
    unsaved_changes = QtCore.Signal(bool)
    zoom_changed = QtCore.Signal(float)

    def __init__(self):
        super().__init__()
        self.lineNumberArea = LineNumberArea(self)
        self.marking_area = MarkingArea(self)
        self.setObjectName("code_editor")
        self.setWordWrapMode(QtGui.QTextOption.NoWrap)

        self.current_font_size = 11

        self.blockCountChanged.connect(self.updateLineNumberAreaWidth)
        self.updateRequest.connect(self.updateLineNumberArea)
        self.cursorPositionChanged.connect(self.update)
        self.cursorPositionChanged.connect(self.mark_finds_in_viewport)
        self.cursorPositionChanged.connect(self.syntax_highlight_in_viewport)

        self.updateLineNumberAreaWidth(0)

        # variables needed for search management
        self.pattern = ""
        self.case_sensitive_search = False
        self.find_results = []
        self.drawn_results = []

        self.find_format = QtGui.QTextCharFormat()
        self.find_format.setBackground(QtGui.QColor(get_color_for_key(COLORS.FIND_HIGHLIGHT.value)))
        self.find_format.setForeground(QtGui.QColor(get_color_for_key(COLORS.PRIMARY_TEXT.value)))

        self.setVerticalScrollBar(wme_essentials.WMEScrollBar(self))
        self.setHorizontalScrollBar(wme_essentials.WMEScrollBar(self))

        self.verticalScrollBar().valueChanged.connect(self.mark_finds_in_viewport)
        self.verticalScrollBar().valueChanged.connect(self.syntax_highlight_in_viewport)
        self.verticalScrollBar().sliderMoved.connect(self.mark_finds_in_viewport)
        self.verticalScrollBar().sliderMoved.connect(self.syntax_highlight_in_viewport)
        self.document().contentsChange.connect(self.update_search)
        self.zoom_changed.connect(self.mark_finds_in_viewport)
        self.zoom_changed.connect(self.syntax_highlight_in_viewport)

        self.highlighter = ndf_syntax_highlighter.NdfSyntaxHighlighter(self.document())

        # set tab size
        font = QtGui.QFont('Courier New', 11)
        self.setTabStopDistance(4 * QtGui.QFontMetrics(font).horizontalAdvance(" "))

        # shortcuts to work outside of context menu
        self.shortcuts = [
            QtGui.QShortcut("Ctrl+D", self, self.on_duplicate),
            QtGui.QShortcut("Ctrl+U", self, self.on_guid),
            QtGui.QShortcut("Ctrl+K", self, self.on_string_token),
        ]

        # marking colors
        self.cursor_marking_color = COLORS.SECONDARY_LIGHT
        self.find_marking_color = COLORS.FIND_HIGHLIGHT

    def lineNumberAreaWidth(self):
        digits = 1
        count = max(1, self.blockCount())
        while count >= 10:
            count /= 10
            digits += 1
        space = 4 + QtGui.QFontMetrics(self.font()).boundingRect('9').width() * digits
        return max(32, space)

    def updateLineNumberAreaWidth(self, _):
        self.setViewportMargins(self.lineNumberAreaWidth(), 0, self.marking_area.sizeHint().width(), 0)

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

        # set geometry of marking area right of text editor
        self.marking_area.setGeometry(QtCore.QRect(cr.right() - self.marking_area.sizeHint().width() + 1, cr.top(),
                                                   self.marking_area.sizeHint().width(), cr.height()))

        self.mark_finds_in_viewport()
        self.syntax_highlight_in_viewport()

    def showEvent(self, event) -> None:
        super().showEvent(event)

        self.updateLineNumberAreaWidth(None)

    def lineNumberAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.lineNumberArea)

        line_number_area_color = get_color_for_key(COLORS.SECONDARY_DARK.value)
        painter.fillRect(event.rect(), line_number_area_color)

        block = self.firstVisibleBlock()
        block_number = block.blockNumber()
        top = self.blockBoundingGeometry(block).translated(self.contentOffset()).top()
        bottom = top + self.blockBoundingRect(block).height()

        # Just to make sure I use the right font
        height = self.fontMetrics().height()
        font = painter.font()
        font.setPointSize(self.current_font_size - 1)
        painter.setFont(font)
        while block.isValid() and (top <= event.rect().bottom()):
            if block.isVisible() and (bottom >= event.rect().top()):
                number = str(block_number + 1)
                line_number_text_color = get_color_for_key(COLORS.SECONDARY_TEXT.value)
                painter.setPen(line_number_text_color)
                painter.drawText(0, top, self.lineNumberArea.width(), height,
                                 Qt.AlignLeft, number)

            block = block.next()
            top = bottom
            bottom = top + self.blockBoundingRect(block).height()
            block_number += 1

    def markingAreaPaintEvent(self, event):
        painter = QtGui.QPainter(self.marking_area)

        marking_area_color = get_color_for_key(COLORS.SECONDARY_DARK.value)
        painter.fillRect(event.rect(), marking_area_color)

        area_top = event.rect().top() + 2
        document_height = self.document().size().height()
        line_height = self.fontMetrics().height()
        document_height *= line_height
        area_bottom = min(document_height, event.rect().bottom()) - 2
        if self.horizontalScrollBar().isVisible():
            area_bottom -= self.horizontalScrollBar().height()

        area_height = area_bottom - area_top
        total_lines = self.blockCount()

        for line_number, line_colors in self.marking_area.lines_to_marking_colors.items():
            # calculate at which y position to draw the marking
            line_height = area_height * line_number / total_lines
            y = area_top + line_height
            # draw the marking
            color = get_color_for_key(line_colors[len(line_colors) - 1].value)
            painter.fillRect(0, y, self.marking_area.w, 2, color)

    def paintEvent(self, event):
        if abs(self.current_font_size - self.font().pointSizeF()) > 1.0:
            self.set_font_size(self.current_font_size)

        painter = QtGui.QPainter(self.viewport())
        rect = self.cursorRect()
        rect.setLeft(0)
        rect.setRight(self.width() - 1)
        painter.setPen(Qt.NoPen)
        painter.setBrush(QtGui.QColor(get_color_for_key(COLORS.SECONDARY_LIGHT.value)))
        painter.drawRect(rect)

        # get current cursor line number
        cursor_line_number = self.textCursor().blockNumber()
        # add marking
        self.clear_markings_for_color(self.cursor_marking_color)
        self.add_marking(cursor_line_number, self.cursor_marking_color)

        super().paintEvent(event)

    def add_marking(self, line: int, color: COLORS):
        if line not in self.marking_area.lines_to_marking_colors:
            self.marking_area.lines_to_marking_colors[line] = []
        self.marking_area.lines_to_marking_colors[line].append(color)

    def clear_markings_for_color(self, color: COLORS):
        new_markings = {}
        for line, line_colors in self.marking_area.lines_to_marking_colors.items():
            new_colors = [c for c in line_colors if c != color]
            if len(new_colors) > 0:
                new_markings[line] = new_colors
        self.marking_area.lines_to_marking_colors = new_markings

    def find_pattern(self, pattern, updating=False):
        self.reset_find()
        self.pattern = pattern

        if pattern == "":
            return

        start = 0
        text = self.toPlainText()

        if not self.case_sensitive_search:
            text = text.lower()
            pattern = pattern.lower()

        while True:
            start = text.find(pattern, start)
            if start < 0:
                break

            self.find_results.append((start, start + len(pattern)))

            line_number = self.document().findBlock(start).blockNumber()
            self.add_marking(line_number, self.find_marking_color)

            start += len(pattern)

        self.mark_finds_in_viewport()
        self.search_complete.emit()
        if not updating:
            self.goto_next_find()

    def reset_find(self):
        if len(self.find_results) == 0:
            return

        extra_selections = self.extraSelections()
        new_selections = []
        for selection in extra_selections:
            if selection.format.background() != self.find_format.background():
                new_selections.append(selection)
        self.setExtraSelections(new_selections)
        self.clear_markings_for_color(self.find_marking_color)

        self.find_results = []
        self.drawn_results = []
        self.pattern = ""

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

        extra_selections = self.extraSelections()

        # check all results
        for find in self.find_results:
            if find[0] > end:
                break
            # draw those in viewport that are not already drawn
            elif find[0] >= start and not self.drawn_results.__contains__(find[0]):
                selection = QtWidgets.QTextEdit.ExtraSelection()

                selection.format = self.find_format
                selection.cursor = self.textCursor()
                selection.cursor.setPosition(find[0], QtGui.QTextCursor.MoveAnchor)
                selection.cursor.setPosition(find[1], QtGui.QTextCursor.KeepAnchor)
                extra_selections.append(selection)

                self.drawn_results.append(find[0])

        self.setExtraSelections(extra_selections)

    def goto_next_find(self):
        if len(self.find_results) == 0:
            return

        cursor = self.textCursor()
        index = cursor.position()

        for find in self.find_results:
            if index < find[0]:
                cursor.setPosition(find[0], QtGui.QTextCursor.MoveAnchor)
                self.setFocus()
                self.setTextCursor(cursor)
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
        self.find_pattern(self.pattern, updating=True)
        self.mark_finds_in_viewport()

        self.unsaved_changes.emit(True)

    def replace_next(self, search_pattern: str, replace_pattern: str):
        if search_pattern == "" or replace_pattern == "" or search_pattern == replace_pattern:
            return
        if search_pattern != self.pattern:
            self.find_pattern(search_pattern)
        # replace next find after cursor
        cursor = self.textCursor()
        index = cursor.position()
        for find in self.find_results:
            if find[0] >= index:
                cursor.clearSelection()
                cursor.setPosition(find[0], QtGui.QTextCursor.MoveAnchor)
                cursor.setPosition(find[1], QtGui.QTextCursor.KeepAnchor)
                cursor.insertText(replace_pattern)
                break

        self.goto_next_find()

    def replace_all(self, search_pattern: str, replace_pattern: str):
        if search_pattern == "" or replace_pattern == "" or search_pattern == replace_pattern:
            return
        if search_pattern != self.pattern:
            self.find_pattern(search_pattern)
        initial_pos = self.textCursor().position()
        text = self.toPlainText()
        text = text.replace(search_pattern, replace_pattern)
        self.setPlainText(text)

        # move cursor to initial position
        cursor = self.textCursor()
        cursor.setPosition(initial_pos, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def get_selected_text(self):
        return self.textCursor().selectedText()

    # apply syntax highlighting to all visible lines
    def syntax_highlight_in_viewport(self):
        cursor = self.cursorForPosition(QtCore.QPoint(0, 0))
        start = cursor.blockNumber()
        bottom_right = QtCore.QPoint(self.viewport().width() - 1, self.viewport().height() - 1)
        end_pos = self.cursorForPosition(bottom_right).position()
        cursor.setPosition(end_pos, QtGui.QTextCursor.MoveAnchor)
        end = cursor.blockNumber()

        for i in range(end - start + 1):
            block = self.document().findBlockByNumber(start + i)
            self.highlighter.rehighlightBlock(block)

    def contextMenuEvent(self, event):
        menu = self.createStandardContextMenu()

        if not self.isReadOnly():
            duplicate_action = menu.addAction("Duplicate Selection/Line", "Ctrl+D")
            duplicate_action.triggered.connect(self.on_duplicate)

            menu.addSeparator()
            guid_action = menu.addAction("Insert GUID", "Ctrl+U")
            guid_action.triggered.connect(self.on_guid)

            string_token_action = menu.addAction("Insert String Token", "Ctrl+K")
            string_token_action.triggered.connect(self.on_string_token)

        menu.exec(event.globalPos())
        del menu

    def on_duplicate(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        selection = cursor.selectedText()
        if selection == "":
            # select current line
            cursor.select(QtGui.QTextCursor.LineUnderCursor)
            selection = cursor.selectedText()
            cursor.movePosition(QtGui.QTextCursor.EndOfLine, QtGui.QTextCursor.MoveAnchor)
            cursor.clearSelection()
            # create new block and paste
            cursor.insertBlock()
            cursor.insertText(selection)
            # move cursor down
            cursor = self.textCursor()
            cursor.movePosition(QtGui.QTextCursor.Down, QtGui.QTextCursor.MoveAnchor)
            self.setTextCursor(cursor)
        else:
            cursor.clearSelection()
            cursor.insertText(selection)
        cursor.endEditBlock()

    def on_guid(self):
        cursor = self.textCursor()
        cursor.beginEditBlock()
        guid_str = "GUID:{" + str(uuid.uuid4()) + "}"
        cursor.insertText(guid_str)
        cursor.endEditBlock()

    def on_string_token(self):
        dialog = insert_string_dialog.InsertStringDialog()
        if not dialog.exec():
            return

        cursor = self.textCursor()
        cursor.beginEditBlock()
        token_str = f"\"{dialog.get_result()}\""
        cursor.insertText(token_str)
        cursor.endEditBlock()

    def get_cursor_pos(self):
        return self.textCursor().position()

    def set_cursor_pos(self, pos: int):
        cursor = self.textCursor()
        cursor.setPosition(pos, QtGui.QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)
        self.setFocus()

    def set_case_sensitive_search(self, case_sensitive: bool):
        self.case_sensitive_search = case_sensitive

        self.find_pattern(self.pattern, updating=True)
        self.mark_finds_in_viewport()

    def keyPressEvent(self, event: QtGui.QKeyEvent) -> None:
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Left:
                self.goto_prev_find()
                return
            elif event.key() == Qt.Key_Right:
                self.goto_next_find()
                return

        super().keyPressEvent(event)

    def zoomInF(self, range=1.0):
        if self.current_font_size + range > 22:
            if self.current_font_size == 22:
                return
            range = 22 - self.current_font_size
        super().zoomInF(range)
        self.current_font_size += range
        self.zoom_changed.emit(self.current_font_size)

    def zoomOutF(self, range=1.0):
        if self.current_font_size - range < 5.5:
            if self.current_font_size == 5.5:
                return
            range = self.current_font_size - 5.5
        super().zoomInF(-range)
        self.current_font_size -= range
        self.zoom_changed.emit(self.current_font_size)

    def set_font_size(self, size: float):
        size = max(5.5, min(size, 22.0))
        font = self.font()
        font.setPointSizeF(size)
        self.setFont(font)
        self.current_font_size = size
        self.zoom_changed.emit(size)

    def wheelEvent(self, e: QtGui.QWheelEvent) -> None:
        if e.modifiers() == Qt.ControlModifier:
            if e.angleDelta().y() > 0:
                self.zoomInF(1.0)
            else:
                self.zoomOutF(1.0)
            return
        super(WMECodeEditor, self).wheelEvent(e)
