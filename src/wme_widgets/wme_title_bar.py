# custom window title bar, includes own minimize/maximize/close buttons
# has a title that can be set, can be used to drag the window around etc.
# can take wme_widgets (e.g. the wme_menu_bar)

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.utils import icon_manager
from src.utils.color_manager import *


class WMETitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None, window_title: str = "", only_close: bool = False):
        super().__init__(parent)
        self.close_button = QtWidgets.QPushButton()
        self.maximize_button = QtWidgets.QPushButton()
        self.minimize_button = QtWidgets.QPushButton()
        self.title_label = QtWidgets.QLabel()
        self.parent = parent
        self.start = QtCore.QPoint(0, 0)
        self.pressing = False
        self.maximized = False
        self.lastPos = QtCore.QPoint(0, 0)
        self.lastSize = QtCore.QSize(0, 0)
        self.main_layout = QtWidgets.QHBoxLayout()
        self.min_hold = False
        self.max_hold = False
        self.close_hold = False
        self.button_height = 36
        self.button_width = 48

        self.background_color = COLORS.SECONDARY
        # change for light theme
        if theme_manager.is_light_theme():
            self.background_color = COLORS.SECONDARY_LIGHT
            self.setStyleSheet("WMETitleBar, QMenuBar { background-color: "
                               + get_color_for_key(COLORS.SECONDARY_LIGHT.value) + ";}")

        self.setup_ui(window_title, only_close)

    def setup_ui(self, window_title, only_close):
        self.main_layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(self.main_layout)

        icon = QtWidgets.QLabel()
        icon.setFixedSize(self.button_height, self.button_height)
        icon.setPixmap(icon_manager.load_colored_icon("app_icon_colored.png").pixmap(self.button_height))
        self.main_layout.addWidget(icon)

        self.title_label.setText(window_title)
        self.title_label.setHidden(window_title == "")
        self.main_layout.addWidget(self.title_label)

        self.main_layout.addStretch(1)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(0)
        self.main_layout.addLayout(button_layout)

        self.minimize_button.setHidden(only_close)
        self.minimize_button.installEventFilter(self)
        self.minimize_button.setProperty('class', 'titlebar')
        min_icon = icon_manager.load_icon("titlebar/showMin.png", COLORS.PRIMARY)
        self.minimize_button.setIcon(min_icon)
        self.minimize_button.setFixedSize(self.button_width, self.button_height)
        self.minimize_button.clicked.connect(self.on_min_clicked)
        button_layout.addWidget(self.minimize_button)

        self.maximize_button.setHidden(only_close)
        self.maximize_button.installEventFilter(self)
        self.maximize_button.setProperty('class', 'titlebar')
        max_icon = icon_manager.load_icon("titlebar/showMax.png", COLORS.PRIMARY)
        self.maximize_button.setIcon(max_icon)
        self.maximize_button.setFixedSize(self.button_width, self.button_height)
        self.maximize_button.clicked.connect(self.on_max_clicked)
        button_layout.addWidget(self.maximize_button)

        self.close_button.installEventFilter(self)
        close_icon = icon_manager.load_icon("titlebar/close.png", COLORS.DANGER)
        self.close_button.setIcon(close_icon)
        self.close_button.setFixedSize(self.button_width, self.button_height)
        self.close_button.clicked.connect(self.on_close_clicked)
        self.close_button.setProperty('class', 'danger')
        button_layout.addWidget(self.close_button)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def eventFilter(self, source, event):
        # only capture left click
        if event.type() is (QtCore.QEvent.MouseButtonPress or QtCore.QEvent.MouseButtonRelease) \
                and event.button() is not QtCore.Qt.MouseButton.LeftButton:
            return False

        # behaviour when mouse button is held down
        if event.type() is QtCore.QEvent.MouseMove:
            # Leave while pressed
            if event.pos().x() > self.button_width or event.pos().x() < 0 \
                    or event.pos().y() > self.button_height or event.pos().y() < 0:
                if source is self.minimize_button and not self.min_hold:
                    self.minimize_button.setIcon(icon_manager.load_icon("titlebar/showMin.png", COLORS.PRIMARY))
                    self.min_hold = True
                if source is self.maximize_button and not self.max_hold:
                    if self.maximized:
                        self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showNormal.png", COLORS.PRIMARY))
                    else:
                        self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showMax.png", COLORS.PRIMARY))
                    self.max_hold = True
                if source is self.close_button and not self.close_hold:
                    self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.DANGER))
                    self.close_hold = True
            # Enter while pressed
            else:
                if source is self.minimize_button and self.min_hold:
                    self.minimize_button.setIcon(
                        icon_manager.load_icon("titlebar/showMin.png", self.background_color))
                    self.min_hold = False
                if source is self.maximize_button and self.max_hold:
                    if self.maximized:
                        self.maximize_button.setIcon(
                            icon_manager.load_icon("titlebar/showNormal.png", self.background_color))
                    else:
                        self.maximize_button.setIcon(
                            icon_manager.load_icon("titlebar/showMax.png", self.background_color))
                    self.max_hold = False
                if source is self.close_button and self.close_hold:
                    self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", self.background_color))
                    self.close_hold = False

        # min button
        if source is self.minimize_button and event.type() is QtCore.QEvent.MouseButtonPress:
            self.minimize_button.setIcon(icon_manager.load_icon("titlebar/showMin.png", self.background_color))
        elif source is self.minimize_button and event.type() is QtCore.QEvent.MouseButtonRelease:
            self.minimize_button.setIcon(icon_manager.load_icon("titlebar/showMin.png", COLORS.PRIMARY))
        # max button
        elif source is self.maximize_button and event.type() is QtCore.QEvent.MouseButtonPress:
            if self.maximized:
                self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showNormal.png", self.background_color))
            else:
                self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showMax.png", self.background_color))
        elif source is self.maximize_button and event.type() is QtCore.QEvent.MouseButtonRelease:
            if self.maximized:
                self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showNormal.png", COLORS.PRIMARY))
            else:
                self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showMax.png", COLORS.PRIMARY))
        # close button
        elif source is self.close_button and event.type() is QtCore.QEvent.MouseButtonPress:
            self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", self.background_color))
        elif source is self.close_button and event.type() is QtCore.QEvent.MouseButtonRelease:
            self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.DANGER))
        return False

    def setup_button(self, button: QtWidgets.QPushButton, default_icon_name: str, pressed_icon_name: str):
        pass

    def add_widget(self, widget: QtWidgets.QWidget):
        self.main_layout.insertWidget(1, widget)

    def add_spacing(self, spacing: int):
        self.main_layout.insertSpacing(1, spacing)

    def set_title(self, window_title: str):
        self.title_label.setText(window_title)
        self.title_label.setVisible(window_title != "")

    def mousePressEvent(self, event):
        if event.button() is not QtCore.Qt.MouseButton.LeftButton:
            return
        self.start = self.mapToGlobal(event.pos())
        self.pressing = True

    def mouseMoveEvent(self, event):
        if self.pressing and not self.maximized:
            end = self.mapToGlobal(event.pos())
            movement = end - self.start
            self.parent.setGeometry(self.parent.mapToGlobal(movement).x(),
                                    self.parent.mapToGlobal(movement).y(),
                                    self.parent.width(),
                                    self.parent.height())
            self.start = end

    def mouseReleaseEvent(self, event):
        if event.button() is not QtCore.Qt.MouseButton.LeftButton:
            return
        self.pressing = False

        self.max_hold = False
        self.min_hold = False
        self.close_hold = False

    def on_min_clicked(self):
        self.parent.showMinimized()

    def on_max_clicked(self):
        if not self.maximized:
            self.parent.showMaximized()
            self.maximized = True
            self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showNormal.png", COLORS.PRIMARY))
        else:
            self.parent.showNormal()
            self.maximized = False
            self.maximize_button.setIcon(icon_manager.load_icon("titlebar/showMax.png", COLORS.PRIMARY))

    def set_maximized(self, max: bool):
        self.maximized = True
        self.maximize_button.setIcon(
            icon_manager.load_icon("titlebar/showNormal.png" if max else "titlebar/showMax.png", COLORS.PRIMARY))

    def on_close_clicked(self):
        self.parent.close()

    def mouseDoubleClickEvent(self, event):
        super().mouseDoubleClickEvent(event)
        if self.maximize_button.isVisible() and event.button() == Qt.LeftButton:
            self.on_max_clicked()
