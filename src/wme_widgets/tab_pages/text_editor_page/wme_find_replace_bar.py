from PySide6 import QtWidgets, QtCore, QtGui

from src.utils import icon_manager
from src.utils.color_manager import *
from src.wme_widgets import wme_essentials


class FindBar(QtWidgets.QWidget):
    request_find_pattern = QtCore.Signal(str)
    request_find_reset = QtCore.Signal()
    request_uncheck = QtCore.Signal(bool)
    case_sensitivity_changed = QtCore.Signal(bool)

    request_prev = QtCore.Signal()
    request_next = QtCore.Signal()

    tab_pressed = QtCore.Signal()

    def eventFilter(self, obj, event) -> bool:
        if obj == self.line_edit and \
                event.type() == QtCore.QEvent.KeyPress and \
                event.key() == QtCore.Qt.Key_Tab:
            self.tab_pressed.emit()
            return True

        return super().eventFilter(obj, event)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.enter_button = QtWidgets.QToolButton()
        self.close_button = QtWidgets.QToolButton()
        self.case_button = QtWidgets.QToolButton()
        self.next_button = QtWidgets.QToolButton()
        self.prev_button = QtWidgets.QToolButton()
        self.results_label = QtWidgets.QLabel()
        self.line_edit = wme_essentials.WMELineEdit()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.last_search = None
        self.last_case_sensitive = True
        self.setup_ui()
        self.line_edit.installEventFilter(self)

    def setup_ui(self):
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.on_next)
        self.line_edit.setPlaceholderText("Find...")
        self.line_edit.setMaximumWidth(800)

        # TODO: shortcut
        self.case_button.setIcon(icon_manager.load_pixmap("case_sensitivity.png", COLORS.PRIMARY))
        self.case_button.clicked.connect(self.on_case)
        self.case_button.setCheckable(True)
        self.case_button.setChecked(False)
        self.case_button.setToolTip("Toggle case-sensitive search. If the button is enabled, search is case-sensitive. "
                                    "(Ctrl + E)")
        self.case_button.setShortcut(QtCore.Qt.Key_Control + QtCore.Qt.Key_E)
        self.case_button.setFixedSize(36, 36)
        self.case_button.setIconSize(QtCore.QSize(36, 36))
        self.main_layout.addWidget(self.case_button)

        next_icon = QtGui.QIcon()
        next_icon.addPixmap(icon_manager.load_pixmap("arrow_down.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        next_icon.addPixmap(icon_manager.load_pixmap("arrow_down.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.next_button.setIcon(next_icon)
        self.next_button.clicked.connect(self.on_next)
        self.next_button.setToolTip("Next search result (F3)")
        self.next_button.setShortcut(QtCore.Qt.Key_F3)
        self.next_button.setFixedSize(36, 36)
        self.next_button.setIconSize(QtCore.QSize(36, 36))
        self.main_layout.addWidget(self.next_button)

        prev_icon = QtGui.QIcon()
        prev_icon.addPixmap(icon_manager.load_pixmap("arrow_up.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        prev_icon.addPixmap(icon_manager.load_pixmap("arrow_up.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.prev_button.setIcon(prev_icon)
        self.prev_button.clicked.connect(self.on_prev)
        self.prev_button.setToolTip("Previous search result (Ctrl + F3)")
        self.prev_button.setShortcut(QtCore.Qt.CTRL + QtCore.Qt.Key_F3)
        self.prev_button.setFixedSize(36, 36)
        self.prev_button.setIconSize(QtCore.QSize(36, 36))
        self.main_layout.addWidget(self.prev_button)

        self.main_layout.addWidget(self.results_label)
        self.results_label.setMinimumWidth(120)

        self.main_layout.addStretch(0)

        self.enable_find_buttons(False)

        self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.PRIMARY))
        self.close_button.clicked.connect(self.on_close)
        self.close_button.setToolTip("Close search bar")
        self.close_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.close_button)

    def on_search(self):
        self.last_search = self.line_edit.text()
        self.last_case_sensitive = self.case_button.isChecked()

        if self.line_edit.text() == "":
            self.request_find_reset.emit()
            self.results_label.setText("")
            self.enable_find_buttons(False)
            return

        self.results_label.setText("searching...")

        QtCore.QCoreApplication.processEvents()
        self.request_find_pattern.emit(self.line_edit.text())

    def on_close(self):
        self.reset()
        self.request_uncheck.emit(False)

    def on_case(self):
        self.case_sensitivity_changed.emit(self.case_button.isChecked())

    def on_next(self):
        if (self.last_search != self.line_edit.text()) or (self.last_case_sensitive != self.case_button.isChecked()) \
                or not self.last_search:
            self.on_search()
        else:
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
        self.prev_button.setDisabled(not enable)


class ReplaceBar(QtWidgets.QWidget):
    request_replace = QtCore.Signal(str)
    request_replace_all = QtCore.Signal(str)
    request_uncheck = QtCore.Signal(bool)

    tab_pressed = QtCore.Signal()

    def eventFilter(self, obj, event) -> bool:
        if obj == self.line_edit and \
                event.type() == QtCore.QEvent.KeyPress and \
                event.key() == QtCore.Qt.Key_Tab:
            self.tab_pressed.emit()
            return True

        return super().eventFilter(obj, event)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.close_button = QtWidgets.QToolButton()
        self.replace_button = QtWidgets.QPushButton("Replace")
        self.replace_all_button = QtWidgets.QPushButton("Replace All")
        self.line_edit = wme_essentials.WMELineEdit()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setup_ui()
        self.line_edit.installEventFilter(self)

    def setup_ui(self):
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.setSpacing(4)

        self.main_layout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.on_replace)
        self.line_edit.setPlaceholderText("Replace with...")
        self.line_edit.setMaximumWidth(800)

        self.main_layout.addWidget(self.replace_button)
        self.replace_button.clicked.connect(self.on_replace)

        self.main_layout.addWidget(self.replace_all_button)
        self.replace_all_button.clicked.connect(self.on_replace_all)

        self.main_layout.addStretch(0)

        self.main_layout.addWidget(self.close_button)
        self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.PRIMARY))
        self.close_button.clicked.connect(self.on_close)
        self.close_button.setToolTip("Close replace bar")
        self.close_button.setFixedSize(32, 32)

    def on_replace(self):
        self.request_replace.emit(self.line_edit.text())

    def on_replace_all(self):
        self.request_replace_all.emit(self.line_edit.text())

    def on_close(self):
        self.request_uncheck.emit(False)
