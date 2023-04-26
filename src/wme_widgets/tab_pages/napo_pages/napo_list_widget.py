from PySide6 import QtWidgets


class NapoListWidget(QtWidgets.QWidget):
    # TODO: signal on changed
    def __init__(self, title: str = ""):
        super().__init__()

        self.title_label = QtWidgets.QLabel(title)
        self.title_label.setHidden(title == "")
        self.list_widget = QtWidgets.QListWidget()
        # TODO: add button
        # TODO: input for add, with confirm button and input mask
        # TODO: delete button

        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.title_label)
        main_layout.addWidget(self.list_widget)

    def update_list(self, items: []):
        self.list_widget.clear()
        items = [str(i) for i in items]
        self.list_widget.addItems(items)
