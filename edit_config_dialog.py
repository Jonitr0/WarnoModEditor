from PySide2 import QtWidgets, QtCore

class WarnoPathDialog(QtWidgets.QDialog):
    def __init__(self, config: QtCore.QSettings):
        super().__init__()

    def setup_ui(self, config: QtCore.QSettings):
        main_layout = QtWidgets.QVBoxLayout(self)
        form_layout = QtWidgets.QFormLayout(self)