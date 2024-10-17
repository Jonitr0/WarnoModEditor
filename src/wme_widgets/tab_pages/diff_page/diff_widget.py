import os

from PySide6 import QtWidgets, QtCore

from src.wme_widgets import main_widget
from src.utils import icon_manager
from src.utils.color_manager import *


class DIFF_ROLE(Enum):
    # only in target mod
    LEFT = 0
    # only in source mod
    RIGHT = 1
    # in both mods, but different
    CHANGED = 2


class FILE_TYPE(Enum):
    DIR = 0
    TEXT = 1
    OTHER = 2


icon_colors_for_diff_role = {
    DIFF_ROLE.LEFT: COLORS.LEFT_ICON,
    DIFF_ROLE.RIGHT: COLORS.RIGHT_ICON,
    DIFF_ROLE.CHANGED: COLORS.CHANGED_ICON,
}

icon_type_for_file_type = {
    FILE_TYPE.DIR: "dir.png",
    FILE_TYPE.TEXT: "text_file.png",
    FILE_TYPE.OTHER: "file.png",
}


# widget representing a single entry on the diff page
class DiffWidget(QtWidgets.QFrame):
    open_in_text_editor = QtCore.Signal(str)
    open_comparison_page = QtCore.Signal(str, str, str, str, str, bool)

    def __init__(self, file_name: str, left_text: str, right_text: str, left_mod: str, right_mod: str,
                 file_type: FILE_TYPE = FILE_TYPE.OTHER, parent: QtWidgets.QWidget = None):
        super().__init__(parent)

        self.main_layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.main_layout)
        self.setObjectName("list_entry")
        self.file_name = file_name
        self.left_text = left_text
        self.right_text = right_text
        self.left_mod = left_mod
        self.right_mod = right_mod
        self.file_type = file_type

        self.setup_ui()

    def setup_ui(self):
        # add icon
        icon_label = QtWidgets.QLabel()
        icon = icon_manager.load_icon(icon_type_for_file_type[self.file_type],
                                      icon_colors_for_diff_role[self.get_role()])
        icon_label.setPixmap(icon.pixmap(24, 24))
        # add a label with the file name
        file_name_label = QtWidgets.QLabel(self.file_name)
        # add to the main layout
        self.main_layout.addWidget(icon_label)
        self.main_layout.addWidget(file_name_label)
        self.main_layout.addStretch(1)

        if self.get_role() is not DIFF_ROLE.RIGHT and self.file_type == FILE_TYPE.TEXT:
            # add button to open file in text editor
            open_left_button = QtWidgets.QToolButton()
            open_left_button.setFixedSize(32, 32)
            open_left_button.setIconSize(QtCore.QSize(32, 32))
            open_left_button.setToolTip("Open in Text Editor")
            open_left_button.setIcon(icon_manager.load_icon("text_editor.png", COLORS.PRIMARY))
            open_left_button.clicked.connect(lambda: self.open_in_text_editor.emit(os.path.join(
                main_widget.instance.get_loaded_mod_path(), self.file_name)))
            self.main_layout.addWidget(open_left_button)

        if self.get_role() is DIFF_ROLE.CHANGED and self.file_type == FILE_TYPE.TEXT:
            # if file name ends with .ndf, add parser based comparison button
            if self.file_name.endswith(".ndf"):
                open_compiler_diff_button = QtWidgets.QToolButton()
                open_compiler_diff_button.setFixedSize(32, 32)
                open_compiler_diff_button.setIconSize(QtCore.QSize(32, 32))
                open_compiler_diff_button.setToolTip("Show Differences (Parser Based)")
                open_compiler_diff_button.setIcon(icon_manager.load_icon("parser_compare.png", COLORS.PRIMARY))
                open_compiler_diff_button.clicked.connect(lambda: self.open_comparison_page.emit(
                    self.file_name[self.file_name.rindex('/') + 1:], self.left_text, self.right_text,
                    self.left_mod, self.right_mod, True))
                self.main_layout.addWidget(open_compiler_diff_button)
            # add button to open file comparison page
            open_diff_button = QtWidgets.QToolButton()
            open_diff_button.setFixedSize(32, 32)
            open_diff_button.setIconSize(QtCore.QSize(32, 32))
            open_diff_button.setToolTip("Show Differences (Plain Text)")
            open_diff_button.setIcon(icon_manager.load_icon("file_compare.png", COLORS.PRIMARY))
            open_diff_button.clicked.connect(lambda: self.open_comparison_page.emit(
                self.file_name[self.file_name.rindex('/') + 1:], self.left_text, self.right_text,
                self.left_mod, self.right_mod, False))
            self.main_layout.addWidget(open_diff_button)

    def get_role(self) -> DIFF_ROLE:
        if self.left_text is None:
            return DIFF_ROLE.RIGHT
        elif self.right_text is None:
            return DIFF_ROLE.LEFT
        else:
            return DIFF_ROLE.CHANGED
