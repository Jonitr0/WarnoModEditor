from PySide6 import QtWidgets, QtCore, QtGui

from src.utils import icon_manager
from src.utils.color_manager import *


class FindBar(QtWidgets.QWidget):
    request_find_pattern = QtCore.Signal(str)
    request_find_reset = QtCore.Signal()
    request_uncheck = QtCore.Signal(bool)

    request_prev = QtCore.Signal()
    request_next = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        self.enter_button = QtWidgets.QToolButton()
        self.close_button = QtWidgets.QToolButton()
        self.next_button = QtWidgets.QToolButton()
        self.prev_button = QtWidgets.QToolButton()
        self.results_label = QtWidgets.QLabel()
        self.line_edit = QtWidgets.QLineEdit()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.current_search = ""
        self.setup_ui()

    def setup_ui(self):
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.on_search)

        self.enter_button.setIcon(icon_manager.load_icon("magnify.png", COLORS.PRIMARY))
        self.enter_button.setToolTip("Start search")
        self.enter_button.clicked.connect(self.on_search)
        self.enter_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.enter_button)

        self.main_layout.addWidget(self.results_label)
        self.results_label.setMinimumWidth(120)

        prev_icon = QtGui.QIcon()
        prev_icon.addPixmap(icon_manager.load_pixmap("arrowUp.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        prev_icon.addPixmap(icon_manager.load_pixmap("arrowUp.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.prev_button.setIcon(prev_icon)
        self.prev_button.clicked.connect(self.on_prev)
        self.prev_button.setToolTip("Previous search result")
        self.prev_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.prev_button)

        next_icon = QtGui.QIcon()
        next_icon.addPixmap(icon_manager.load_pixmap("arrowDown.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        next_icon.addPixmap(icon_manager.load_pixmap("arrowDown.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.next_button.setIcon(next_icon)
        self.next_button.clicked.connect(self.on_next)
        self.next_button.setToolTip("Next search result")
        self.next_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.next_button)

        self.enable_find_buttons(False)

        self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.PRIMARY))
        self.close_button.clicked.connect(self.on_close)
        self.close_button.setToolTip("Close search")
        self.close_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.close_button)

    def on_search(self):
        if self.line_edit.text() == "":
            self.request_find_reset.emit()
            self.results_label.setText("")
            self.enable_find_buttons(False)
            return

        self.results_label.setText("searching...")

        QtCore.QCoreApplication.processEvents()
        self.current_search = self.line_edit.text()
        self.request_find_pattern.emit(self.current_search)

    def on_close(self):
        self.reset()
        self.request_uncheck.emit(False)

    def on_next(self):
        self.request_next.emit()

    def on_prev(self):
        self.request_prev.emit()

    def reset(self):
        self.request_find_reset.emit()
        self.line_edit.setText("")
        self.results_label.setText("")
        self.setHidden(True)
        self.enable_find_buttons(False)

    def set_label_text(self, text: str):
        self.results_label.setText(text)

    def enable_find_buttons(self, enable: bool = True):
        self.next_button.setDisabled(not enable)
        self.prev_button.setDisabled(not enable)

# TODO: add replace bar
