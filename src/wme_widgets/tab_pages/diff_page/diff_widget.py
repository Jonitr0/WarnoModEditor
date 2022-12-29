from PySide6 import QtWidgets, QtCore

from src.wme_widgets.tab_pages.diff_page import diff_code_editor


# TODO: add colored icon for faster readability
class DiffWidget(QtWidgets.QFrame):
    request_open_in_text_editor = QtCore.Signal(str, int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # lines before and after each diff block
        self.buffer_lines = 3
        # max. number of identical lines between two diff blocks
        self.max_space_between_diff_blocks = 3

        self.open_in_editor_button = QtWidgets.QPushButton("Open in text editor")
        self.info_label = QtWidgets.QLabel()
        self.diff_layout = QtWidgets.QVBoxLayout()

        self.setObjectName("list_entry")
        self.setup_ui()

        self.buttons_to_file = {}

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        info_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(info_layout)

        info_layout.addWidget(self.info_label)
        info_layout.addStretch(1)
        info_layout.addWidget(self.open_in_editor_button)

        main_layout.addLayout(self.diff_layout)

    def left_only(self, diff_name: str, left_name: str):
        self.info_label.setText(diff_name + " only exists in " + left_name)
        if not diff_name.endswith(".ndf"):
            self.open_in_editor_button.setHidden(True)

        self.buttons_to_file[self.open_in_editor_button] = (diff_name, 0)
        self.open_in_editor_button.pressed.connect(self.on_open_in_editor)

    def right_only(self, diff_name: str, right_name: str):
        self.info_label.setText(diff_name + " only exists in " + right_name)
        self.open_in_editor_button.setHidden(True)

    def changed_text_file(self, diff_name: str, changed_lines: list, left_lines: list, right_lines: list):
        self.info_label.setText(diff_name + " contains " + str(len(changed_lines)) + " changed line(s):")
        self.open_in_editor_button.setHidden(True)
        # TODO: create diff blocks
        # TODO: add text edit per diff block
        # TODO: add open in editor button per diff block
        diff_blocks = self.create_diff_blocks(changed_lines)
        for diff_block in diff_blocks:
            self.create_diff_block_widget(diff_block, diff_name, left_lines, right_lines)

    def create_diff_blocks(self, changed_lines: list):
        diff_blocks = []
        current_block = []
        for i in range(len(changed_lines)):
            current_block.append(changed_lines[i])

            if i < len(changed_lines) - 1 and changed_lines[i + 1] - changed_lines[
                i] > self.max_space_between_diff_blocks:
                diff_blocks.append(current_block)
                current_block = []

        diff_blocks.append(current_block)
        return diff_blocks

    def create_diff_block_widget(self, diff_block: list, diff_name: str, left_lines: list, right_lines: list):
        # TODO: create header which allows opening the line in the text editor
        header_layout = QtWidgets.QHBoxLayout()
        header_label = QtWidgets.QLabel("line " + str(diff_block[0] + 1) + ":")
        header_layout.addWidget(header_label)
        header_layout.addStretch(1)
        header_button = QtWidgets.QPushButton("Open in text editor")
        header_layout.addWidget(header_button)
        header_button.pressed.connect(self.on_open_in_editor)

        self.buttons_to_file[header_button] = (diff_name, diff_block[0])

        self.diff_layout.addLayout(header_layout)

        start_line = max(diff_block[0] - self.buffer_lines, 0)
        end_line = min(diff_block[len(diff_block) - 1] + self.buffer_lines, len(left_lines) - 1)
        total_lines = end_line - start_line + 1

        text_edit = diff_code_editor.DiffCodeEditor()
        self.diff_layout.addWidget(text_edit)
        # index for diff_block
        j = 0
        for i in range(total_lines):
            line_index = start_line + i
            # the next line is not a changed line
            if line_index != diff_block[j]:
                text_edit.add_line(left_lines[line_index], 0)
            else:
                text_edit.add_line(left_lines[line_index], 1)
                text_edit.add_line(right_lines[line_index], 2)
                if j < len(diff_block) - 1:
                    j += 1

    def on_open_in_editor(self):
        data = self.buttons_to_file[self.sender()]
        self.request_open_in_text_editor.emit(data[0], data[1])
