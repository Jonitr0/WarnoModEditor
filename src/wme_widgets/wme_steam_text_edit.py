from PySide6 import QtWidgets, QtGui

from src.utils import icon_manager
from src.utils.color_manager import *

import re


class WMESteamTextEdit(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super().__init__(parent)
        self.text_edit = QtWidgets.QTextEdit()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        text_type_layout = QtWidgets.QHBoxLayout()
        text_type_layout.setContentsMargins(8, 0, 8, 0)
        text_type_widget = QtWidgets.QWidget()
        text_type_widget.setLayout(text_type_layout)
        tool_bar.addWidget(text_type_widget)

        text_type_label = QtWidgets.QLabel("Text type:")
        text_type_layout.addWidget(text_type_label)

        self.text_type_selector = QtWidgets.QComboBox()
        self.text_type_selector.addItem("Normal")
        self.text_type_selector.addItem("Heading 1")
        self.text_type_selector.addItem("Heading 2")
        self.text_type_selector.addItem("Heading 3")
        self.text_type_selector.activated.connect(self.on_text_type_changed)
        text_type_layout.addWidget(self.text_type_selector)

        tool_bar.addSeparator()

        self.bold_action = tool_bar.addAction(icon_manager.load_icon("bold.png", COLORS.PRIMARY), "Bold (Ctrl + B)")
        self.bold_action.setCheckable(True)
        self.bold_action.setShortcut("Ctrl+B")
        self.bold_action.triggered.connect(lambda checked: self.text_edit.setFontWeight(QtGui.QFont.Bold if checked else
                                                                                        QtGui.QFont.Normal))

        self.italic_action = tool_bar.addAction(icon_manager.load_icon("italic.png", COLORS.PRIMARY),
                                                "Italic (Ctrl + I)")
        self.italic_action.setCheckable(True)
        self.italic_action.setShortcut("Ctrl+I")
        self.italic_action.triggered.connect(lambda checked: self.text_edit.setFontItalic(checked))

        self.underline_action = tool_bar.addAction(icon_manager.load_icon("underline.png", COLORS.PRIMARY),
                                                   "Underline (Ctrl + U)")
        self.underline_action.setCheckable(True)
        self.underline_action.setShortcut("Ctrl+U")
        self.underline_action.triggered.connect(lambda checked: self.text_edit.setFontUnderline(checked))

        self.strikethrough_action = tool_bar.addAction(icon_manager.load_icon("strikethrough.png", COLORS.PRIMARY),
                                                       "Strikethrough (Ctrl + Shift + T)")
        self.strikethrough_action.setCheckable(True)
        self.strikethrough_action.setShortcut("Ctrl+Shift+T")
        self.strikethrough_action.triggered.connect(self.on_strikethrough)

        tool_bar.addSeparator()

        self.link_action = tool_bar.addAction(icon_manager.load_icon("link.png", COLORS.PRIMARY), "Add Hyperlink")

        tool_bar.addSeparator()

        list_action = tool_bar.addAction(icon_manager.load_icon("bullet_list.png", COLORS.PRIMARY), "List")

        ordered_list_action = tool_bar.addAction(icon_manager.load_icon("ordered_list.png", COLORS.PRIMARY),
                                                 "Ordered List")

        tool_bar.addSeparator()

        undo_icon = QtGui.QIcon()
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.undo_action = tool_bar.addAction(undo_icon, "Undo (Ctrl + Z)")
        self.undo_action.setDisabled(True)
        self.undo_action.setShortcut("Ctrl+Z")

        redo_icon = QtGui.QIcon()
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.redo_action = tool_bar.addAction(redo_icon, "Redo (Ctrl + Y)")
        self.redo_action.setDisabled(True)
        self.redo_action.setShortcut("Ctrl+Y")

        main_layout.addWidget(self.text_edit)

        self.text_edit.selectionChanged.connect(self.on_new_selection)
        self.text_edit.cursorPositionChanged.connect(self.on_new_selection)

        self.text_edit.undoAvailable.connect(self.on_undo_available)
        self.text_edit.redoAvailable.connect(self.on_redo_available)

        self.text_edit.setFontPointSize(10.5)
        self.text_edit.setObjectName("steam_text_edit")

    def on_text_type_changed(self, index: int):
        # get selection
        cursor = self.text_edit.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        if start == end:
            # no selection, change the text type of the current block
            block = cursor.block()
            block_format, char_format = self.formats_for_heading(index)
            self.set_block_format(block, block_format, char_format)
        else:
            # get all the blocks in the selection
            block_count = self.text_edit.document().blockCount()
            blocks = []
            for i in range(block_count):
                block = self.text_edit.document().findBlockByNumber(i)
                if block.position() + block.length() > start and block.position() < end:
                    blocks.append(block)

            for block in blocks:
                block_format, char_format = self.formats_for_heading(index)
                self.set_block_format(block, block_format, char_format)

    def set_block_format(self, text_block: QtGui.QTextBlock, block_format: QtGui.QTextBlockFormat,
                         char_format: QtGui.QTextCharFormat = None):
        cursor = QtGui.QTextCursor(text_block)
        cursor.setBlockFormat(block_format)

        if char_format is not None:
            cursor.select(QtGui.QTextCursor.BlockUnderCursor)
            cursor.mergeCharFormat(char_format)

    def formats_for_heading(self, heading_level: int) -> (QtGui.QTextBlockFormat, QtGui.QTextCharFormat):
        block_format = QtGui.QTextBlockFormat()
        block_format.setHeadingLevel(heading_level)
        block_format.setBottomMargin(0 if heading_level == 0 else 8.0 - 2.0 * heading_level)
        text_char_format = QtGui.QTextCharFormat()
        text_char_format.setFontPointSize(10.5 if heading_level == 0 else 18 - 2 * heading_level)
        color = get_color_for_key(COLORS.SECONDARY_TEXT.value if heading_level == 0 else COLORS.PRIMARY.value)
        text_char_format.setForeground(QtGui.QBrush(color))
        return block_format, text_char_format

    def on_strikethrough(self, checked: bool):
        char_format = self.text_edit.currentCharFormat()
        char_format.setFontStrikeOut(checked)
        self.text_edit.setCurrentCharFormat(char_format)

    def get_text(self):
        plain_text = self.text_edit.toPlainText()
        block_count = self.text_edit.document().blockCount()
        format_tag_positions = {}
        # get all format tag positions
        for i in range(block_count):
            block = self.text_edit.document().findBlockByNumber(block_count - i - 1)
            block_start = block.position()
            block_end = block_start + block.length() - 1
            heading_level = block.blockFormat().headingLevel()
            # set heading end tag
            if block.blockFormat().headingLevel() != 0:
                if not block_start in format_tag_positions:
                    format_tag_positions[block_start] = []
                if not block_end in format_tag_positions:
                    format_tag_positions[block_end] = []
                format_tag_positions[block_end].append(f"[/h{heading_level}]")
            # set in-line format tags
            for format_range in reversed(block.textFormats()):
                start = block.position() + format_range.start
                end = start + format_range.length
                text_format = format_range.format
                format_tag_positions = self.mark_format_tags(start, end, text_format, format_tag_positions)
            # set heading start tag
            if block.blockFormat().headingLevel() != 0:
                format_tag_positions[block_start].append(f"[h{heading_level}]")

        # apply format tags
        for pos in reversed(sorted(format_tag_positions.keys())):
            for tag in format_tag_positions[pos]:
                plain_text = plain_text[:pos] + tag + plain_text[pos:]

        plain_text = "\"" + plain_text + "\""
        return plain_text

    def mark_format_tags(self, start: int, end: int, text_format: QtGui.QTextCharFormat, format_tag_positions: dict):
        if start not in format_tag_positions:
            format_tag_positions[start] = []
        if end not in format_tag_positions:
            format_tag_positions[end] = []
        if text_format.fontWeight() == QtGui.QFont.Bold:
            format_tag_positions[end].append("[/b]")
            format_tag_positions[start].append("[b]")
        if text_format.fontItalic():
            format_tag_positions[end].append("[/i]")
            format_tag_positions[start].append("[i]")
        if text_format.fontUnderline():
            format_tag_positions[end].append("[/u]")
            format_tag_positions[start].append("[u]")
        if text_format.fontStrikeOut():
            format_tag_positions[end].append("[/strike]")
            format_tag_positions[start].append("[strike]")
        return format_tag_positions

    def set_text(self, text: str):
        text = text.removeprefix("\"").removesuffix("\"")

        tags = {
            "[b]": "[/b]",
            "[i]": "[/i]",
            "[u]": "[/u]",
            "[strike]": "[/strike]",
            "[h1]": "[/h1]",
            "[h2]": "[/h2]",
            "[h3]": "[/h3]",
        }
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

            text_format = cursor.charFormat()
            block_format = cursor.blockFormat()

            match key:
                case "[b]":
                    text_format.setFontWeight(QtGui.QFont.Bold)
                case "[i]":
                    text_format.setFontItalic(True)
                case "[u]":
                    text_format.setFontUnderline(True)
                case "[strike]":
                    text_format.setFontStrikeOut(True)
                case "[h1]":
                    heading_block_format, heading_char_format = self.formats_for_heading(1)
                    block_format.merge(heading_block_format)
                    text_format.merge(heading_char_format)
                case "[h2]":
                    heading_block_format, heading_char_format = self.formats_for_heading(2)
                    block_format.merge(heading_block_format)
                    text_format.merge(heading_char_format)
                case "[h3]":
                    heading_block_format, heading_char_format = self.formats_for_heading(3)
                    block_format.merge(heading_block_format)
                    text_format.merge(heading_char_format)

            cursor.mergeBlockFormat(block_format)
            cursor.mergeCharFormat(text_format)

    def on_new_selection(self):
        # get selection text format
        cursor = self.text_edit.textCursor()
        start = cursor.selectionStart()
        end = cursor.selectionEnd()

        if start == end:
            # take cursor format
            text_format = cursor.charFormat()
            self.bold_action.setChecked(text_format.fontWeight() == QtGui.QFont.Bold)
            self.italic_action.setChecked(text_format.fontItalic())
            self.underline_action.setChecked(text_format.fontUnderline())
            self.strikethrough_action.setChecked(text_format.fontStrikeOut())
            self.text_type_selector.setCurrentIndex(cursor.blockFormat().headingLevel())
            return

        # get all blocks in selection
        block_count = self.text_edit.document().blockCount()
        blocks = []
        for i in range(block_count):
            block = self.text_edit.document().findBlockByNumber(i)
            if block.position() + block.length() > start and block.position() < end:
                blocks.append(block)

        bold = True
        italic = True
        underline = True
        strikethrough = True
        heading_level = blocks[0].blockFormat().headingLevel()

        for block in blocks:
            for format_range in block.textFormats():
                format_start = block.position() + format_range.start
                format_end = format_start + format_range.length
                if format_end >= start and format_start < end:
                    text_format = format_range.format
                    if text_format.fontWeight() != QtGui.QFont.Bold:
                        bold = False
                    if not text_format.fontItalic():
                        italic = False
                    if not text_format.fontUnderline():
                        underline = False
                    if not text_format.fontStrikeOut():
                        strikethrough = False
                if block.blockFormat().headingLevel() != heading_level:
                    heading_level = 0

        self.bold_action.setChecked(bold)
        self.italic_action.setChecked(italic)
        self.underline_action.setChecked(underline)
        self.strikethrough_action.setChecked(strikethrough)
        self.text_type_selector.setCurrentIndex(heading_level)

    def on_undo_available(self, available: bool):
        self.undo_action.setDisabled(not available)

    def on_redo_available(self, available: bool):
        self.redo_action.setDisabled(not available)

    def on_undo(self):
        self.text_edit.document().undo()

    def on_redo(self):
        self.text_edit.document().redo()
