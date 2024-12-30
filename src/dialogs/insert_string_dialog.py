from PySide6 import QtWidgets

from src.wme_widgets import wme_essentials, main_widget
from src.dialogs import base_dialog


class InsertStringDialog(base_dialog.BaseDialog):
    def __init__(self):
        self.file_combobox = wme_essentials.WMECombobox()
        self.token_combobox = wme_essentials.WMECombobox()
        self.value_combobox = wme_essentials.WMECombobox()

        super(InsertStringDialog, self).__init__()
        self.setWindowTitle("Insert String Token")

        self.on_file_selected(self.file_combobox.currentText())

    def setup_ui(self):
        form_layout = QtWidgets.QFormLayout()
        form_layout.setContentsMargins(0, 0, 0, 0)
        self.main_layout.addLayout(form_layout)

        self.file_combobox.addItems([
            "COMPANIES.csv",
            "INTERFACE_INGAME.csv",
            "INTERFACE_OUTGAME.csv",
            "PLATOONS.csv",
            "UNITS.csv"
        ])

        self.file_combobox.currentTextChanged.connect(self.on_file_selected)
        form_layout.addRow("File:", self.file_combobox)
        self.token_combobox.currentIndexChanged.connect(self.on_token_selected)
        form_layout.addRow("Token:", self.token_combobox)
        self.value_combobox.currentIndexChanged.connect(self.on_value_selected)
        form_layout.addRow("Value:", self.value_combobox)

    def on_file_selected(self, file: str):
        self.token_combobox.clear()
        keys = main_widget.instance.asset_string_manager.asset_strings[file].keys()
        self.token_combobox.addItems(keys)
        self.token_combobox.setDisabled(len(keys) == 0)

        self.value_combobox.clear()
        vals = main_widget.instance.asset_string_manager.asset_strings[file].values()
        self.value_combobox.addItems(vals)
        self.value_combobox.setDisabled(len(vals) == 0)

        self.ok_button.setDisabled(len(keys) == 0)

    def on_token_selected(self, index: int):
        self.value_combobox.setCurrentIndex(index)

    def on_value_selected(self, index: int):
        self.token_combobox.setCurrentIndex(index)

    def get_result(self):
        return self.token_combobox.currentText()

    def accept(self) -> None:
        if self.token_combobox.currentText() == "":
            return
        super(InsertStringDialog, self).accept()
