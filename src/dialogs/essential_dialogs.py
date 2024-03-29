# basic dialogs that are often used

from PySide6 import QtWidgets
from PySide6.QtCore import Qt

from src.dialogs import base_dialog
from src.wme_widgets import wme_essentials


# dialog asking user to select an item from a combobox
class SelectionDialog(base_dialog.BaseDialog):
    def __init__(self, text: str, title: str, item_list: []):
        self.label = QtWidgets.QLabel(text)
        self.combobox = wme_essentials.WMECombobox()
        self.combobox.addItems(item_list)

        super().__init__()
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)
        self.main_layout.addWidget(self.combobox)

    def get_selection(self):
        return self.combobox.currentText()


# dialog asking user to confirm or cancel something
class ConfirmationDialog(base_dialog.BaseDialog):
    def __init__(self, text: str, title: str, urgent=True):
        self.label = QtWidgets.QLabel(text)

        super().__init__(urgent=urgent)
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)


# dialog that informs the user of something
class MessageDialog(base_dialog.BaseDialog):
    def __init__(self, title: str, text: str, rich_text: bool = False):
        self.label = QtWidgets.QLabel(text)
        if rich_text:
            self.label.setTextFormat(Qt.RichText)
            self.label.setTextInteractionFlags(Qt.TextBrowserInteraction)
            self.label.setOpenExternalLinks(True)

        super().__init__(ok_only=True, urgent=True)
        self.setWindowTitle(title)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)


# dialog that asks user to save/discard unsaved changes or to cancel
class AskToSaveDialog(base_dialog.BaseDialog):
    def __init__(self, file_name: str, title: str = "Unsaved Changes"):
        self.label = QtWidgets.QLabel(file_name + " has unsaved changes. Would you like to save them?")
        self.discard_button = QtWidgets.QPushButton("Discard")
        self.save_changes = True

        super().__init__(urgent=True)
        self.setWindowTitle(title)

        self.ok_button.setText("Save")

        self.discard_button.setFixedWidth(120)
        self.discard_button.clicked.connect(self.on_discard)
        self.button_layout.insertWidget(1, self.discard_button)

    def setup_ui(self):
        self.main_layout.addWidget(self.label)

    def on_discard(self):
        self.save_changes = False
        self.accept()
