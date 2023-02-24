# a resizable window with title bar and shadow effect

from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt
from src.wme_widgets import wme_title_bar
from src.utils import icon_manager


class BaseWindow(QtWidgets.QWidget):
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
        self.setWindowFlags(Qt.FramelessWindowHint)

        outer_layout = QtWidgets.QHBoxLayout()
        outer_layout.setContentsMargins(0, 0, 0, 0)
        outer_layout.addWidget(shadow_widget)
        self.setLayout(outer_layout)

        self.bar_layout = QtWidgets.QVBoxLayout(self)
        self.bar_layout.setContentsMargins(0, 0, 0, 6)
        self.bar_layout.setSpacing(0)

        bar_widget = QtWidgets.QWidget()
        self.shadow_layout.addWidget(bar_widget)
        bar_widget.setLayout(self.bar_layout)

        self.title_bar = wme_title_bar.WMETitleBar(self)
        self.bar_layout.addWidget(self.title_bar)

        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(16, 16)

        self.setWindowIcon(QtGui.QIcon(icon_manager.load_colored_icon("app_icon_colored")))

    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = self.rect()
        self.grip.move(rect.right() - 16 - 4, rect.bottom() - 16 - 4)
        # TODO (0.1.1): add borders that allow resize, in shadow area

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