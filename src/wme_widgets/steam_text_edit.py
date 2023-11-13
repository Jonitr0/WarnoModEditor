from PySide6 import QtWidgets, QtGui

from src.utils import icon_manager
from src.utils.color_manager import *

import re


class SteamTextEdit(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.text_edit = QtWidgets.QTextEdit()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        text_type_selector = QtWidgets.QComboBox()
        text_type_selector.addItem("Text")
        text_type_selector.addItem("Heading 1")
        text_type_selector.addItem("Heading 2")
        text_type_selector.addItem("Heading 3")

        tool_bar.addWidget(text_type_selector)

        tool_bar.addSeparator()

        bold_action = tool_bar.addAction(icon_manager.load_icon("bold.png", COLORS.PRIMARY), "Bold (Ctrl + B)")
        bold_action.setCheckable(True)
        bold_action.setShortcut("Ctrl+B")

        italic_action = tool_bar.addAction(icon_manager.load_icon("italic.png", COLORS.PRIMARY), "Italic (Ctrl + I)")
        italic_action.setCheckable(True)
        italic_action.setShortcut("Ctrl+I")

        underline_action = tool_bar.addAction(icon_manager.load_icon("underline.png", COLORS.PRIMARY),
                                              "Underline (Ctrl + U)")
        underline_action.setCheckable(True)
        underline_action.setShortcut("Ctrl+U")

        strikethrough_action = tool_bar.addAction(icon_manager.load_icon("strikethrough.png", COLORS.PRIMARY),
                                                  "Strikethrough (Ctrl + Shift + T)")
        strikethrough_action.setCheckable(True)
        strikethrough_action.setShortcut("Ctrl+Shift+T")

        tool_bar.addSeparator()

        list_action = tool_bar.addAction(icon_manager.load_icon("bullet_list.png", COLORS.PRIMARY), "List")

        ordered_list_action = tool_bar.addAction(icon_manager.load_icon("ordered_list.png", COLORS.PRIMARY),
                                                 "Ordered List")

        link_action = tool_bar.addAction(icon_manager.load_icon("link.png", COLORS.PRIMARY), "Link")

        tool_bar.addSeparator()

        undo_icon = QtGui.QIcon()
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        undo_action = tool_bar.addAction(undo_icon, "Undo (Ctrl + Z)")
        undo_action.setDisabled(True)
        undo_action.setShortcut("Ctrl+Z")

        redo_icon = QtGui.QIcon()
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        redo_action = tool_bar.addAction(redo_icon, "Redo (Ctrl + Y)")
        redo_action.setDisabled(True)
        redo_action.setShortcut("Ctrl+Y")

        main_layout.addWidget(self.text_edit)

    def get_text(self):
        plain_text = self.text_edit.toPlainText()
        block_count = self.text_edit.document().blockCount()
        format_tag_positions = {}
        # get all format tag positions
        for i in range(block_count):
            block = self.text_edit.document().findBlockByNumber(block_count - i - 1)
            # TODO: apply block format
            for format_range in reversed(block.textFormats()):
                start = format_range.start
                end = start + format_range.length
                text_format = format_range.format
                format_tag_positions = self.mark_format_tags(start, end, text_format, format_tag_positions)

        # apply format tags
        for pos in reversed(sorted(format_tag_positions.keys())):
            plain_text = plain_text[:pos] + format_tag_positions[pos] + plain_text[pos:]

        return plain_text

    def mark_format_tags(self, start: int, end: int, text_format: QtGui.QTextCharFormat, format_tag_positions: dict):
        if text_format.fontWeight() == QtGui.QFont.Bold:
            format_tag_positions[end] = "[/b]"
            format_tag_positions[start] = "[b]"
        return format_tag_positions

    def set_text(self, text: str):
        tags = {"[b]": "[/b]"}
        plain_text = text

        # create plain text
        for key, val in tags.items():
            plain_text = plain_text.replace(key, "")
            plain_text = plain_text.replace(val, "")

        # create regex
        escaped_keys = map(re.escape, tags.keys())
        escaped_values = map(re.escape, tags.values())
        escaped_keys = '|'.join(sorted(escaped_keys, key=len, reverse=True))
        escaped_values = '|'.join(sorted(escaped_values, key=len, reverse=True))
        regex = escaped_keys + '|' + escaped_values

        # create index mapping for original text to plain text
        index_in_plain = [i for i in range(len(text))]
        for match in re.finditer(regex, text):
            start = match.start()
            end = match.end()
            length = end - start

            for i in range(length):
                index_in_plain[start + i] = index_in_plain[start]

            for i in range(len(index_in_plain[start + length:])):
                index_in_plain[start + length + i] -= length

        # apply formatting
        self.text_edit.setPlainText(plain_text)
        for match in re.finditer(escaped_keys, text):
            start = index_in_plain[match.start()]
            key = match.group()
            end_index = text.find(tags[match.group()], match.end())
            if end_index == -1:
                continue
            end = index_in_plain[end_index]

            cursor = QtGui.QTextCursor(self.text_edit.document())
            cursor.setPosition(start)
            cursor.setPosition(end, QtGui.QTextCursor.KeepAnchor)

            text_format = QtGui.QTextCharFormat()

            match key:
                case "[b]":
                    text_format.setFontWeight(QtGui.QFont.Bold)
                    cursor.mergeCharFormat(text_format)
