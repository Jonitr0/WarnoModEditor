# dialog asking user to select an item from a combobox

from PySide2 import QtWidgets

from dialogs import base_dialog


class SelectionDialog(base_dialog.BaseDialog):
    def __init__(self, text: str, title: str, item_list: []):
        self.label = QtWidgets.QLabel(text)
        self.combobox = QtWidgets.QComboBox()
        self.combobox.addItems(item_list)

        super().__init__()
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.combobox)

    def get_selection(self):
        return self.combobox.currentText()
