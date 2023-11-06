import os

from PySide6 import QtWidgets, QtCore

from src.wme_widgets import main_widget
from src.utils import icon_manager
from src.utils.color_manager import *


class DIFF_ROLE(Enum):
    # only in target mod
    LEFT = 0
    # only in source mod
    RIGHT = 2
    # in both mods, but different
    CHANGED = 2


icon_colors_for_diff_role = {
    DIFF_ROLE.LEFT: COLORS.LEFT_ICON,
    DIFF_ROLE.RIGHT: COLORS.RIGHT_ICON,
    DIFF_ROLE.CHANGED: COLORS.CHANGED_ICON,
}


# widget representing a single entry on the diff page
class DiffWidget(QtWidgets.QFrame):
    open_in_text_editor = QtCore.Signal(str)
    open_comparison_page = QtCore.Signal(str, str)

    def __init__(self, file_name: str, left_text: str, right_text: str, is_text: bool = True):
        super().__init__()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setObjectName("list_entry")
        self.file_name = file_name
        self.left_text = left_text
        self.right_text = right_text
        self.is_text = is_text

        self.setup_ui()

    def setup_ui(self):
        # add icon
        icon_label = QtWidgets.QLabel()
        icon_type = "file.png"
        # if it is a directory, use the directory icon
        if os.path.isdir(self.file_name):
            icon_type = "folder.png"
        # if it is a text file, use the text file icon
        elif self.is_text:
            icon_type = "text_file.png"
        icon = icon_manager.load_icon(icon_type, icon_colors_for_diff_role[self.get_role()])
        icon_label.setPixmap(icon)
        # add a label with the file name
        file_name_label = QtWidgets.QLabel(self.file_name)
        # add to the main layout
        self.main_layout.addWidget(file_name_label)
        self.main_layout.addStretch()

        if self.get_role() is not DIFF_ROLE.RIGHT and self.is_text:
            # add button to open file in text editor
            open_left_button = QtWidgets.QPushButton("Open in Text Editor")
            open_left_button.clicked.connect(lambda: self.open_in_text_editor.emit(os.path.join(
                main_widget.instance.get_loaded_mod_path(), self.file_name)))
            self.main_layout.addWidget(open_left_button)

        if self.get_role() is DIFF_ROLE.CHANGED and self.is_text:
            # add button to open file comparison page
            open_diff_button = QtWidgets.QPushButton("Show Differences")
            open_diff_button.clicked.connect(lambda: self.open_comparison_page.emit(
                self.left_text, self.right_text))
            self.main_layout.addWidget(open_diff_button)

    def get_role(self) -> DIFF_ROLE:
        if self.left_text is None:
            return DIFF_ROLE.RIGHT
        elif self.right_text is None:
            return DIFF_ROLE.LEFT
        else:
            return DIFF_ROLE.CHANGED
