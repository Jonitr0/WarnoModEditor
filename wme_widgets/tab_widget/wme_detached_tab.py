from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from wme_widgets import wme_title_bar
from wme_widgets.tab_widget import wme_tab_widget

detached_list = []


class WMEDetachedTab(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shadow_layout = QtWidgets.QHBoxLayout()
        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()

        shadow_widget = QtWidgets.QWidget()
        self.shadow_layout.setContentsMargins(4, 4, 4, 4)
        shadow_widget.setLayout(self.shadow_layout)

        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setBlurRadius(4)
        self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow_widget.setGraphicsEffect(self.shadow_effect)

        self.setAttribute(Qt.WA_TranslucentBackground)
        shadow_widget.setAttribute(Qt.WA_TranslucentBackground)

        self.setModal(False)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.bar_layout = QtWidgets.QVBoxLayout(self)
        self.bar_layout.setContentsMargins(0, 0, 0, 6)
        self.bar_layout.setSpacing(0)

        bar_widget = QtWidgets.QWidget()
        self.shadow_layout.addWidget(bar_widget)
        bar_widget.setLayout(self.bar_layout)

        dialog_layout = QtWidgets.QHBoxLayout()
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(shadow_widget)
        self.setLayout(dialog_layout)

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
        super().resizeEvent(event)
        rect = self.rect()
        self.grip.move(rect.right() - 16 - 4, rect.bottom() - 16 - 4)

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

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if (self.windowState() == (Qt.WindowMaximized or Qt.WindowFullScreen)) or int(self.windowState()) == 6:
                self.shadow_layout.setContentsMargins(0, 0, 0, 0)
                self.shadow_effect.setEnabled(False)
            else:
                self.shadow_layout.setContentsMargins(4, 4, 4, 4)
                # stupid but needed to fix shadow effect
                self.resize(self.size().width() + 1, self.size().height() + 1)
                self.resize(self.size().width() - 1, self.size().height() - 1)
                self.shadow_effect.setEnabled(True)
        super().changeEvent(event)
