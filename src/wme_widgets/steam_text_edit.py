from PySide6 import QtWidgets, QtGui

from src.utils import icon_manager
from src.utils.color_manager import *


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
        return self.text_edit.toPlainText()

    def set_text(self, text: str):
        self.text_edit.setPlainText(text)
