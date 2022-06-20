# dialog base class for easier styling
from PySide2 import QtWidgets
from PySide2.QtCore import Qt


class BaseDialog(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowFlags(Qt.MSWindowsFixedSizeDialogHint | Qt.Dialog)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(self.main_layout)

        self.setup_ui()

        button_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(button_layout)
        self.main_layout.setAlignment(button_layout, Qt.AlignCenter)

        # setup ok button
        ok_button = QtWidgets.QPushButton()
        ok_button.setText("OK")
        ok_button.setFixedWidth(120)
        ok_button.clicked.connect(self.accept)
        button_layout.addWidget(ok_button)

        # setup cancel button
        cancel_button = QtWidgets.QPushButton()
        cancel_button.setText("Cancel")
        cancel_button.setFixedWidth(120)
        cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(cancel_button)

    def setup_ui(self):
        raise NotImplementedError("Please Implement this method")
