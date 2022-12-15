import logging

from src.dialogs import base_dialog
from src.utils import icon_manager
from src.utils.color_manager import *

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt


class LogDialog(base_dialog.BaseDialog):
    new_log = QtCore.Signal()
    error_log = QtCore.Signal()

    def __init__(self):
        self.log_label = QtWidgets.QLabel()

        super().__init__(ok_only=True)
        self.set_button_texts(ok="Close")
        self.setWindowTitle("Event Log")

        self.log_stream = LogStream(self)

        stream_logger = logging.StreamHandler(stream=self.log_stream)
        stream_logger.setLevel(logging.WARN)
        stream_logger.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
        logging.getLogger().addHandler(stream_logger)

    def setup_ui(self):
        self.log_label.setFixedWidth(800)
        self.log_label.setWordWrap(True)
        self.log_label.setAlignment(Qt.AlignTop)
        self.log_label.setObjectName("log")
        self.log_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedSize(800, 500)
        scroll_area.setWidget(self.log_label)

        self.main_layout.addWidget(scroll_area)

        copy_button = QtWidgets.QToolButton()
        copy_button.setIcon(icon_manager.load_icon("copy.png", COLORS.SECONDARY_TEXT))
        copy_button.setText("Copy session log to clipboard")
        copy_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        copy_button.setFixedHeight(36)
        copy_button.clicked.connect(self.on_clipboard)

        self.main_layout.addWidget(copy_button)

    def exec_(self):
        self.log_label.setText(str(self.log_stream))

        return super().exec_()

    def on_clipboard(self):
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(str(self.log_stream), mode=cb.Clipboard)


class LogStream(object):
    def __init__(self, dialog: LogDialog):
        self.logs = ''
        self.dialog = dialog

    def write(self, msg):
        if msg.startswith("ERROR"):
            self.dialog.error_log.emit()
        else:
            self.dialog.new_log.emit()

        self.logs += msg

    def flush(self):
        pass

    def __str__(self):
        return self.logs
