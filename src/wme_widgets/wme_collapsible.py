from PySide6 import QtWidgets

from src.utils import icon_manager
from src.utils.color_manager import *


class WMECollapsible(QtWidgets.QWidget):
    def __init__(self, parent = None, title: str = ""):
        super().__init__(parent)

        self.collapse_icon = icon_manager.load_icon("chevron_down.png", COLORS.PRIMARY)
        self.expand_icon = icon_manager.load_icon("chevron_right.png", COLORS.PRIMARY)
        self.collapsed = False

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 10, 0)
        self.setLayout(self.main_layout)

        self.header_layout = QtWidgets.QHBoxLayout()
        self.main_layout.addLayout(self.header_layout)

        self.collapse_button = QtWidgets.QToolButton()
        self.collapse_button.setFixedSize(32, 32)
        self.collapse_button.setIcon(self.collapse_icon)
        self.collapse_button.clicked.connect(self.on_collapse)
        self.header_layout.addWidget(self.collapse_button)

        self.header_label = QtWidgets.QLabel(title)
        self.header_label.setStyleSheet("font-size: 14px;")
        self.header_layout.addWidget(self.header_label)

        self.item_layout = QtWidgets.QVBoxLayout()
        self.item_layout.setContentsMargins(50, 0, 0, 0)
        self.item_layout.setSpacing(0)
        self.main_layout.addLayout(self.item_layout)

    def on_collapse(self):
        self.collapsed = not self.collapsed

        self.collapse_button.setIcon(self.expand_icon if self.collapsed else self.collapse_icon)

        for i in range(self.item_layout.count()):
            self.item_layout.itemAt(i).widget().setHidden(self.collapsed)

    def add_widget(self, w: QtWidgets.QWidget):
        self.item_layout.addWidget(w)

