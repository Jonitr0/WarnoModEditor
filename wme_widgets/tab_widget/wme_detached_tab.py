from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

from wme_widgets import wme_title_bar
from wme_widgets.tab_pages import tab_page_base


class WMEDetachedTab(QtWidgets.QDialog):
    close_pressed = QtCore.Signal(QtWidgets.QDialog)

    def __init__(self, widget: tab_page_base.TabPageBase, parent=None, title: str = ""):
        super().__init__(parent)

        self.setModal(False)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.bar_layout = QtWidgets.QVBoxLayout(self)
        self.bar_layout.setContentsMargins(1, 0, 1, 16)
        self.bar_layout.setSpacing(0)
        self.setLayout(self.bar_layout)

        self.title_bar = wme_title_bar.WMETitleBar(self)
        self.bar_layout.addWidget(self.title_bar)
        self.widget = widget
        self.bar_layout.addWidget(self.widget)

        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(16, 16)

        self.setWindowTitle(title)

    def resizeEvent(self, event):
        QtWidgets.QDialog.resizeEvent(self, event)
        rect = self.rect()
        self.grip.move(rect.right() - 16, rect.bottom() - 16)

    def close(self):
        # TODO: ask to save progress
        self.close_pressed.emit(self)
        return super().close()

    def setWindowTitle(self, title: str):
        super().setWindowTitle(title)
        self.title_bar.set_title(title)
