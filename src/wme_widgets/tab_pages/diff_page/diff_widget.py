import os.path

from PySide6 import QtWidgets, QtCore

from src.wme_widgets.tab_pages.diff_page import diff_code_editor, diff_creator
from src.utils.color_manager import *
from src.utils import icon_manager


class DiffWidget(QtWidgets.QFrame):
    request_open_in_text_editor = QtCore.Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # lines before and after each diff block
        self.icon = QtWidgets.QLabel()
        self.buffer_lines = 3
        # max. number of identical lines between two diff blocks
        self.max_space_between_diff_blocks = 6

        self.open_in_editor_button = QtWidgets.QPushButton("Open in text editor")
        self.info_label = QtWidgets.QLabel()
        self.diff_layout = QtWidgets.QVBoxLayout()

        self.setObjectName("list_entry")
        self.setup_ui()

        self.buttons_to_file = {}
        self.buttons_to_textedits = {}

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        info_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(info_layout)

        self.icon.setFixedSize(24, 24)
        self.icon.setPixmap(icon_manager.load_icon("file_question.png", COLORS.PRIMARY).pixmap(24))
        info_layout.addWidget(self.icon)

        info_layout.addWidget(self.info_label)
        info_layout.addStretch(1)
        info_layout.addWidget(self.open_in_editor_button)

        main_layout.addLayout(self.diff_layout)

    def left_only(self, diff_name: str, left_name: str, left_path: str):
        self.set_icon(diff_name, left_path, COLORS.LEFT_ICON)

        self.info_label.setText(diff_name + " only exists in " + left_name)
        if not diff_name.endswith(".ndf"):
            self.open_in_editor_button.setHidden(True)

        self.buttons_to_file[self.open_in_editor_button] = (diff_name, 0)
        self.open_in_editor_button.clicked.connect(self.on_open_in_editor)

    def right_only(self, diff_name: str, right_name: str, right_path: str):
        self.set_icon(diff_name, right_path, COLORS.RIGHT_ICON)

        self.info_label.setText(diff_name + " only exists in " + right_name)
        self.open_in_editor_button.setHidden(True)

    def changed_text_file(self, diff_name: str, diff_blocks: list, left_lines: list, right_lines: list):
        self.set_icon(diff_name, "", COLORS.CHANGED_ICON)

        self.info_label.setText(diff_name + " contains changes:")
        self.open_in_editor_button.setHidden(True)
        for diff_block in diff_blocks:
            self.create_diff_block_widget(diff_block, diff_name, left_lines, right_lines)

    def create_diff_block_widget(self, diff_block: diff_creator.DiffBlockData, diff_name: str, left_lines: list,
                                 right_lines: list):
        text_edit = diff_code_editor.DiffCodeEditor()
        text_edit.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        self.create_diff_block_header(diff_name, diff_block, text_edit)

        self.diff_layout.addWidget(text_edit)

        for line in diff_block.lines:
            line_number = line[0]
            op = line[1]
            if op == "=":
                text_edit.add_line(left_lines[line_number], 0)
            elif op == "+":
                text_edit.add_line(left_lines[line_number], 1)
            elif op == "-":
                text_edit.add_line(right_lines[line_number], 2)

    def create_diff_block_header(self, diff_name: str, diff_block: diff_creator.DiffBlockData, text_edit):
        header_layout = QtWidgets.QHBoxLayout()

        header_minimize_button = QtWidgets.QToolButton()
        header_minimize_button.setIcon(icon_manager.load_icon("chevron_down.png", COLORS.SECONDARY_TEXT))
        header_minimize_button.setToolTip("Minimize")
        header_minimize_button.clicked.connect(self.on_minimize)
        header_layout.addWidget(header_minimize_button)

        header_label = QtWidgets.QLabel("line " + str(diff_block.start + 1) + ":")
        header_layout.addWidget(header_label)
        header_layout.addStretch(1)
        header_open_in_editor_button = QtWidgets.QPushButton("Open in text editor")
        header_layout.addWidget(header_open_in_editor_button)
        header_open_in_editor_button.clicked.connect(self.on_open_in_editor)

        self.buttons_to_file[header_open_in_editor_button] = (diff_name, diff_block.start)

        self.diff_layout.addLayout(header_layout)
        self.buttons_to_textedits[header_minimize_button] = (text_edit, True)

    def on_open_in_editor(self):
        data = self.buttons_to_file[self.sender()]
        self.request_open_in_text_editor.emit(data[0], data[1])

    def on_minimize(self):
        text_edit, expanded = self.buttons_to_textedits[self.sender()]
        # is expanded
        if expanded:
            text_edit.setHidden(True)
            expanded = False
            self.sender().setIcon(icon_manager.load_icon("chevron_right.png", COLORS.SECONDARY_TEXT))
            self.sender().setToolTip("Expand")
        else:
            text_edit.setHidden(False)
            expanded = True
            self.sender().setIcon(icon_manager.load_icon("chevron_down.png", COLORS.SECONDARY_TEXT))
            self.sender().setToolTip("Minimize")
        self.buttons_to_textedits[self.sender()] = (text_edit, expanded)

    def set_icon(self, diff_name: str, diff_path: str, color: COLORS):
        # changed file
        if diff_path == "":
            if diff_name.endswith(".ndf"):
                self.icon.setPixmap(icon_manager.load_icon("text_file.png", color).pixmap(24))
        # dir
        elif os.path.isdir(os.path.join(diff_path, diff_name)):
            self.icon.setPixmap(icon_manager.load_icon("dir.png", color).pixmap(24))
        # unknown
        else:
            self.icon.setPixmap(icon_manager.load_icon("file_question.png", color).pixmap(24))
