from PySide2 import QtWidgets
from PySide2.QtCore import Qt


class WarnoPathDialog(QtWidgets.QDialog):
    def __init__(self, warno_path):
        super().__init__()

        self.line_edit = QtWidgets.QLineEdit()
        self.setup_ui(warno_path)
        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.Dialog)
        self.setWindowTitle("Set WARNO path")

    def setup_ui(self, warno_path):
        # setup layouts
        main_layout = QtWidgets.QVBoxLayout(self)
        text_layout = QtWidgets.QHBoxLayout(self)
        button_layout = QtWidgets.QHBoxLayout(self)

        # setup label
        info_label = QtWidgets.QLabel()
        info_label.setText("Please enter the path to your WARNO installation.\nIt could look like this: "
                           "\"C:/Program Files (x86)/Steam/steamapps/common/WARNO\"")
        main_layout.addWidget(info_label)
        main_layout.addLayout(text_layout)

        # setup line edit
        self.line_edit.setText(warno_path)
        text_layout.addWidget(self.line_edit)

        # setup "browse" button
        browse_button = QtWidgets.QPushButton()
        browse_button.setText("Browse..")
        # TODO: remove lambda
        browse_button.clicked.connect(lambda: self.open_warno_path_dialog(self.line_edit.text()))
        text_layout.addWidget(browse_button)

        main_layout.addLayout(button_layout)
        main_layout.setAlignment(button_layout, Qt.AlignCenter)

        # setup ok button
        ok_button = QtWidgets.QPushButton()
        ok_button.setText("OK")
        ok_button.setFixedWidth(80)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        # setup cancel button
        cancel_button = QtWidgets.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.setFixedWidth(80)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

        # set main widget
        self.setLayout(main_layout)

    def open_warno_path_dialog(self, warno_path):
        warno_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter WARNO path", warno_path)

        self.line_edit.setText(warno_path)

    def get_path(self):
        return self.line_edit.text().removesuffix("/")