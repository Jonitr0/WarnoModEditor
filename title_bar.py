from PySide2 import QtWidgets


class TitleBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QHBoxLayout()
        main_layout.setContentsMargins(10, 0, 0, 0)
        self.setLayout(main_layout)

        button_size = 32

        title_label = QtWidgets.QLabel("Window Title")
        main_layout.addWidget(title_label)

        main_layout.addStretch(1)

        minimize_button = QtWidgets.QPushButton("_")
        minimize_button.setFixedSize(button_size, button_size)
        minimize_button.clicked.connect(self.on_min_clicked)
        main_layout.addWidget(minimize_button)

        maximize_button = QtWidgets.QPushButton("+")
        maximize_button.setFixedSize(button_size, button_size)
        maximize_button.clicked.connect(self.on_max_clicked)
        main_layout.addWidget(maximize_button)

        close_button = QtWidgets.QPushButton("x")
        close_button.setFixedSize(button_size, button_size)
        close_button.clicked.connect(self.on_close_clicked)
        main_layout.addWidget(close_button)

    def on_min_clicked(self):
        self.parent.showMinimized()

    def on_max_clicked(self):
        # TODO: save previous size, change button to restore
        self.parent.showMaximized()

    def on_close_clicked(self):
        self.parent.close()
