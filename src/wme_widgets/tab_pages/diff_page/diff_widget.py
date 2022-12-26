from PySide6 import QtWidgets

from src.wme_widgets.tab_pages.diff_page import diff_code_editor


# TODO: add colored icon for faster readability
class DiffWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # lines before and after each diff block
        self.buffer_lines = 1
        # max. number of identical lines between two diff blocks
        self.max_space_between_diff_blocks = 3
        # max. number of adjacent changed lines until break
        self.max_diff_display_length = 10

        # TODO: make this a layout to list multiple potential diffs
        self.open_in_editor_button = QtWidgets.QPushButton("Open in text editor")
        self.info_label = QtWidgets.QLabel()
        self.diff_layout = QtWidgets.QVBoxLayout()

        self.setObjectName("list_entry")
        self.setup_ui()

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
        # TODO: only show button if file

    def right_only(self, diff_name: str, right_name: str):
        self.info_label.setText(diff_name + " only exists in " + right_name)
        self.open_in_editor_button.setHidden(True)

    def changed_text_file(self, diff_name: str, changed_lines: list, left_lines: list, right_lines: list):
        self.info_label.setText(diff_name + " contains " + str(len(changed_lines)) + " changed line(s):")
        # TODO: create diff blocks
        # TODO: add text edit per diff block
        # TODO: add open in editor button per diff block
        for line in changed_lines:
            text_edit = diff_code_editor.DiffCodeEditor()
            text_edit.appendPlainText(left_lines[line])
            self.diff_layout.addWidget(text_edit)
