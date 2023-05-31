from src.dialogs.base_dialog import BaseDialog
from src.utils import icon_manager
from src.utils.color_manager import *
from src.wme_widgets import main_widget

import traceback

from PySide6 import QtWidgets
from PySide6.QtCore import Qt


class ExceptionHandlerDialog(BaseDialog):
    def __init__(self):
        self.error_description_label = QtWidgets.QLabel()

        super().__init__(ok_only=True)

        self.setWindowTitle("WME has encountered a problem")

    def setup_ui(self):
        hyperlink_color = get_color_for_key(COLORS.PRIMARY.value)

        info_label = QtWidgets.QLabel("It seems like WARNO mod editor has run into an unhandled exception. Please "
                                      "open an issue on the <a style=\"color: " + hyperlink_color + "\" "
                                      "href=\"https://github.com/Jonitr0/WarnoModEditor/issues\"> WME Github page</a> "
                                      "if this error has not been reported yet.")
        info_label.setTextFormat(Qt.RichText)
        info_label.setTextInteractionFlags(Qt.TextBrowserInteraction)
        info_label.setOpenExternalLinks(True)
        info_label.setMaximumWidth(800)
        info_label.setWordWrap(True)

        self.main_layout.addWidget(info_label)

        self.error_description_label.setFixedWidth(800)
        self.error_description_label.setWordWrap(True)
        self.error_description_label.setAlignment(Qt.AlignTop)
        self.error_description_label.setObjectName("log")
        self.error_description_label.setTextInteractionFlags(Qt.TextSelectableByMouse)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFixedSize(800, 500)
        scroll_area.setWidget(self.error_description_label)

        self.main_layout.addWidget(scroll_area)

        copy_button = QtWidgets.QToolButton()
        copy_button.setIcon(icon_manager.load_icon("copy.png", COLORS.SECONDARY_TEXT))
        copy_button.setText("Copy error report to clipboard")
        copy_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        copy_button.setFixedHeight(36)
        copy_button.clicked.connect(self.on_clipboard)

        self.main_layout.addWidget(copy_button)

    def exceptHook(self, exceptionType, exceptionValue, exceptionTraceback):
        exception_summary = str(exceptionType) + ": " + str(exceptionValue) + "\n"
        stack_trace = "".join(traceback.extract_tb(exceptionTraceback).format())
        exception_summary += "Stacktrace:\n" + stack_trace

        logging.error(exception_summary)
        self.error_description_label.setText(exception_summary)

        if main_widget.instance:
            main_widget.instance.hide_loading_screen()

        self.exec_()

    def on_clipboard(self):
        cb = QtWidgets.QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(str(self.error_description_label.text()), mode=cb.Clipboard)
