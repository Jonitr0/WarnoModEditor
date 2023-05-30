# dialog base class for easier styling

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets import wme_title_bar, wme_essentials
from src.utils import icon_manager

SHADOW_WIDTH = 8


class BaseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None, ok_only: bool = False, urgent: bool = False):
        super().__init__(parent)
        self.shadow_layout = QtWidgets.QHBoxLayout()
        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()

        shadow_widget = QtWidgets.QWidget()
        self.shadow_layout.setContentsMargins(SHADOW_WIDTH, SHADOW_WIDTH, SHADOW_WIDTH, SHADOW_WIDTH)
        shadow_widget.setLayout(self.shadow_layout)

        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setBlurRadius(SHADOW_WIDTH)
        self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow_widget.setGraphicsEffect(self.shadow_effect)

        self.setAttribute(Qt.WA_TranslucentBackground)
        shadow_widget.setAttribute(Qt.WA_TranslucentBackground)

        self.widgetList = []

        self.setWindowFlags(Qt.FramelessWindowHint)

        self.bar_layout = QtWidgets.QVBoxLayout(self)
        self.bar_layout.setContentsMargins(0, 0, 0, 0)
        self.bar_layout.setSpacing(0)

        bar_widget = QtWidgets.QWidget()
        self.shadow_layout.addWidget(bar_widget)
        bar_widget.setLayout(self.bar_layout)

        dialog_layout = QtWidgets.QHBoxLayout()
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(shadow_widget)
        self.setLayout(dialog_layout)

        self.title_bar = wme_title_bar.WMETitleBar(self, only_close=True)
        self.bar_layout.addWidget(self.title_bar)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.setContentsMargins(10, 10, 10, 10)
        self.main_layout.setSpacing(10)
        self.bar_layout.addLayout(self.main_layout)

        self.setup_ui()

        layout_contents = (self.main_layout.itemAt(i) for i in range(self.main_layout.count()))
        self.createWidgetList(layout_contents)
        if len(self.widgetList) > 0:
            self.widgetList[0].setFocus()

        self.button_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(self.button_layout)
        self.main_layout.setAlignment(self.button_layout, Qt.AlignCenter)

        self.setWindowIcon(QtGui.QIcon(icon_manager.load_colored_icon("app_icon_colored")))

        # setup ok button
        self.ok_button = QtWidgets.QPushButton()
        self.ok_button.setText("OK")
        self.ok_button.setFixedWidth(120)
        self.ok_button.clicked.connect(self.accept)
        self.button_layout.addWidget(self.ok_button)

        # setup cancel button
        self.cancel_button = None
        if not ok_only:
            self.cancel_button = QtWidgets.QPushButton()
            self.cancel_button.setText("Cancel")
            self.cancel_button.setFixedWidth(120)
            self.cancel_button.clicked.connect(self.reject)
            self.button_layout.addWidget(self.cancel_button)

        if urgent:
            QtWidgets.QApplication.beep()

    def setup_ui(self):
        raise NotImplementedError("Please Implement this method")

    def setWindowTitle(self, title: str) -> None:
        super().setWindowTitle(title)
        self.title_bar.set_title(title)

    # put input wme_widgets in a list and make enter press iterate through them (like tab)
    # or accept dialog if it's the last
    def createWidgetList(self, layout_contents):
        for layout_item in layout_contents:
            if type(layout_item) == QtWidgets.QWidgetItem:
                if type(layout_item.widget()) == QtWidgets.QLineEdit \
                        or type(layout_item.widget()) == wme_essentials.WMESpinbox:
                    layout_item.widget().installEventFilter(self)
                    self.widgetList.append(layout_item.widget())
            elif layout_item.inherits("QLayout"):
                child_layout_contents = (layout_item.itemAt(i) for i in range(layout_item.count()))
                self.createWidgetList(child_layout_contents)

    def eventFilter(self, source, event) -> bool:
        if event.type() == QtCore.QEvent.KeyPress \
                and event.key() == Qt.Key_Return:
            index = self.widgetList.index(source)
            if index == len(self.widgetList) - 1:
                self.accept()
                return True
            else:
                self.widgetList[index + 1].setFocus()

        return False

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if (self.windowState() == (Qt.WindowMaximized or Qt.WindowFullScreen)) or int(self.windowState()) == 6:
                self.shadow_layout.setContentsMargins(0, 0, 0, 0)
                self.shadow_effect.setEnabled(False)
            else:
                self.shadow_layout.setContentsMargins(SHADOW_WIDTH, SHADOW_WIDTH, SHADOW_WIDTH, SHADOW_WIDTH)
                # stupid but needed to fix shadow effect
                self.resize(self.size().width() + 1, self.size().height() + 1)
                self.resize(self.size().width() - 1, self.size().height() - 1)
                self.shadow_effect.setEnabled(True)
        super().changeEvent(event)

    def set_button_texts(self, ok: str = "Ok", cancel: str = "Cancel"):
        self.ok_button.setText(ok)
        if self.cancel_button:
            self.cancel_button.setText(cancel)
