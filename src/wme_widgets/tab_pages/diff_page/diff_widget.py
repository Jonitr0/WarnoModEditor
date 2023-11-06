# widget representing a single entry on the diff page

from PySide6 import QtWidgets


class DiffWidget(QtWidgets.QFrame):
    def __init__(self, file_name: str, left_text: str, right_text: str):
        super().__init__()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setObjectName("list_entry")
        self.file_name = file_name
        self.left_text = left_text
        self.right_text = right_text

        self.setup_ui()

    def setup_ui(self):
        # add icon
        icon_label = QtWidgets.QLabel()
        # TODO: add icon in left/right/changed color
        # add a label with the file name
        file_name_label = QtWidgets.QLabel(self.file_name)
        # add to the main layout
        self.main_layout.addWidget(file_name_label)
        self.main_layout.addStretch()
