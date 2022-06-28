# dialog base class for easier styling

from PySide2 import QtWidgets
from PySide2.QtCore import Qt

import wme_title_bar

# TODO: Ok on Enter if last widget in layout is selected

class BaseDialog(QtWidgets.QDialog):
    def __init__(self, parent = None, ok_only: bool = False):
        super().__init__(parent)

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.bar_layout = QtWidgets.QVBoxLayout(self)
        self.bar_layout.setContentsMargins(0, 0, 0, 0)
        self.bar_layout.setSpacing(0)
        self.setLayout(self.bar_layout)

        self.title_bar = wme_title_bar.TitleBar(self, only_close=True)
        self.bar_layout.addWidget(self.title_bar)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)

        self.setup_ui()

        button_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(button_layout)
        self.main_layout.setAlignment(button_layout, Qt.AlignCenter)

        # setup ok button
        ok_button = QtWidgets.QPushButton()
        ok_button.setText("OK")
        ok_button.setFixedWidth(120)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        # setup cancel button
        if not ok_only:
            cancel_button = QtWidgets.QPushButton()
            cancel_button.setText("Cancel")
            cancel_button.setFixedWidth(120)
            cancel_button.clicked.connect(self.reject)
            button_layout.addWidget(cancel_button)

    def setup_ui(self):
        raise NotImplementedError("Please Implement this method")

    def setWindowTitle(self, arg__1: str) -> None:
        super().setWindowTitle(arg__1)
        self.title_bar.set_title(arg__1)
