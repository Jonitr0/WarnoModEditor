from PySide2 import QtWidgets
from PySide2.QtCore import Qt

from wme_widgets import wme_title_bar
from wme_widgets.tab_widget import wme_tab_widget

detached_list = []


class WMEDetachedTab(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setModal(False)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.bar_layout = QtWidgets.QVBoxLayout(self)
        self.bar_layout.setContentsMargins(0, 0, 0, 0)
        self.bar_layout.setSpacing(0)
        self.setLayout(self.bar_layout)

        self.title_bar = wme_title_bar.WMETitleBar(self)
        self.bar_layout.addWidget(self.title_bar)

        content_layout = QtWidgets.QVBoxLayout(self)
        content_layout.setContentsMargins(10, 10, 10, 10)
        self.bar_layout.addLayout(content_layout)
        self.tab_widget = wme_tab_widget.WMETabWidget(self)
        self.tab_widget.tabBar().tab_removed.connect(self.on_tab_removed)
        content_layout.addWidget(self.tab_widget)

        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(16, 16)

    def add_tab(self, widget, title: str):
        self.tab_widget.addTab(widget, title)

    def resizeEvent(self, event):
        QtWidgets.QDialog.resizeEvent(self, event)
        rect = self.rect()
        self.grip.move(rect.right() - 16, rect.bottom() - 16)

    def close(self):
        # TODO: ask to save progress
        detached_list.remove(self)
        return super().close()

    def on_tab_removed(self):
        if self.tab_widget.tabBar().count() < 1:
            self.close()

    def setWindowTitle(self, title: str):
        super().setWindowTitle(title)
        self.title_bar.set_title(title)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            event.ignore()
        else:
            super().keyPressEvent(event)
            