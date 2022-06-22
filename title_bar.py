import os

from PySide2 import QtWidgets, QtCore, QtGui


class TitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None, window_title: str = "", only_close: bool = False):
        super().__init__(parent)
        self.title_label = QtWidgets.QLabel()
        self.parent = parent
        self.start = QtCore.QPoint(0, 0)
        self.pressing = False
        self.maximized = False
        self.lastPos = QtCore.QPoint(0, 0)
        self.lastSize = QtCore.QSize(0, 0)
        self.main_layout = QtWidgets.QHBoxLayout()

        self.setup_ui(window_title, only_close)

    def setup_ui(self, window_title, only_close):
        self.main_layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(self.main_layout)

        button_size = 32

        icon = QtWidgets.QLabel()
        icon.setFixedSize(32, 32)
        icon.setPixmap(QtGui.QPixmap("resources/img/icon32.png"))
        self.main_layout.addWidget(icon)

        self.title_label.setText(window_title)
        self.title_label.setVisible(window_title != "")
        self.main_layout.addWidget(self.title_label)

        self.main_layout.addStretch(1)

        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(0)
        self.main_layout.addLayout(button_layout)

        if not only_close:
            minimize_button = QtWidgets.QPushButton("_")
            minimize_button.setFixedSize(button_size, button_size)
            minimize_button.clicked.connect(self.on_min_clicked)
            button_layout.addWidget(minimize_button)

            self.maximize_button = QtWidgets.QPushButton("+")
            self.maximize_button.setFixedSize(button_size, button_size)
            self.maximize_button.clicked.connect(self.on_max_clicked)
            button_layout.addWidget(self.maximize_button)

        close_button = QtWidgets.QPushButton("x")
        close_button.setFixedSize(button_size, button_size)
        close_button.clicked.connect(self.on_close_clicked)
        close_button.setProperty('class', 'danger')
        button_layout.addWidget(close_button)

        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # TODO: button styles

    def add_widget(self, widget: QtWidgets.QWidget):
        self.main_layout.insertWidget(1, widget)

    def set_title(self, window_title: str):
        self.title_label.setText(window_title)
        self.title_label.setVisible(window_title != "")

    def mousePressEvent(self, event):
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
        self.pressing = False

    def on_min_clicked(self):
        self.parent.showMinimized()

    def on_max_clicked(self):
        if not self.maximized:
            self.parent.showMaximized()
            self.maximize_button.setText("#")
            self.maximized = True
        else:
            self.parent.showNormal()
            self.maximize_button.setText("+")
            self.maximized = False

    def on_close_clicked(self):
        self.parent.close()
