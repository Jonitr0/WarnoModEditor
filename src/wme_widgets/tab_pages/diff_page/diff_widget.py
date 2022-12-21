from PySide6 import QtWidgets


# TODO: add colored icon for faster readability
class DiffWidget(QtWidgets.QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO: make this a layout to list multiple potential diffs
        self.text_edit = QtWidgets.QTextEdit()
        self.open_in_editor_button = QtWidgets.QPushButton("Open in text editor")
        self.info_label = QtWidgets.QLabel()
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

        main_layout.addWidget(self.text_edit)

    def left_only(self, diff_name: str, left_name: str):
        self.info_label.setText(diff_name + " only exists in " + left_name)
        self.text_edit.setHidden(True)

    def right_only(self, diff_name: str, right_name: str):
        self.info_label.setText(diff_name + " only exists in " + right_name)
        self.open_in_editor_button.setHidden(True)
        self.text_edit.setHidden(True)

    def changed_text_file(self, diff_name: str, changed_lines: list, left_lines: list, right_lines: list):
        self.info_label.setText(diff_name + " contains " + str(len(changed_lines)) + " changed line(s):")
