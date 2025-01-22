from PySide6 import QtWidgets, QtGui

from src.utils import icon_manager
from src.utils.color_manager import *


class WMECollapsible(QtWidgets.QWidget):
    def __init__(self, parent=None, title: str = "", margin: int = 50, expand_on_adding: bool = True):
        super().__init__(parent)

        self.collapse_icon = icon_manager.load_icon("chevron_down.png", COLORS.PRIMARY)
        self.expand_icon = icon_manager.load_icon("chevron_right.png", COLORS.PRIMARY)
        self.expand_icon.addPixmap(icon_manager.load_pixmap("chevron_right.png", COLORS.SECONDARY_LIGHT),
                                   QtGui.QIcon.Disabled)
        self.collapsed = False
        self.expand_on_adding = expand_on_adding

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

        self.header_layout.addStretch(1)
        self.corner_widget = QtWidgets.QWidget()
        self.header_layout.addWidget(self.corner_widget)

        self.item_layout = QtWidgets.QVBoxLayout()
        self.item_layout.setContentsMargins(margin, 0, 0, 0)
        self.item_layout.setSpacing(0)
        self.main_layout.addLayout(self.item_layout)

        self.set_collapsed(True)

    def on_collapse(self):
        self.set_collapsed(not self.collapsed)

    def set_collapsed(self, collapsed: bool):
        self.collapsed = collapsed

        self.collapse_button.setIcon(self.expand_icon if self.collapsed else self.collapse_icon)

        for i in range(self.item_layout.count()):
            if not self.item_layout.itemAt(i).widget():
                continue
            self.item_layout.itemAt(i).widget().setHidden(self.collapsed)

        if collapsed and self.item_layout.count() == 0:
            self.collapse_button.setDisabled(True)

    def add_widget(self, w: QtWidgets.QWidget):
        self.item_layout.addWidget(w)
        self.collapse_button.setDisabled(False)
        if self.collapsed:
            w.setHidden(True)
        if self.expand_on_adding:
            self.set_collapsed(False)

    def remove_widget(self, w: QtWidgets.QWidget):
        self.item_layout.removeWidget(w)
        w.setParent(None)
        if self.item_layout.count() == 0:
            self.set_collapsed(True)
            self.collapse_button.setDisabled(True)

    def add_spacing(self, size: int):
        self.item_layout.addSpacing(size)

    def set_spacing(self, size: int):
        self.item_layout.setSpacing(size)

    def set_title(self, title: str):
        self.header_label.setText(title)

    def set_corner_widget(self, widget: QtWidgets.QWidget):
        self.header_layout.removeWidget(self.corner_widget)
        self.corner_widget.setParent(None)
        self.header_layout.addWidget(widget)
        self.corner_widget = widget

    def widgets(self):
        return [self.item_layout.itemAt(i).widget() for i in range(self.item_layout.count())]
