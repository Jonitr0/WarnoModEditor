from pathlib import Path

from PySide6 import QtWidgets, QtCore
from src.dialogs.base_dialog import BaseDialog
from src.dialogs import essential_dialogs
from src.wme_widgets import wme_essentials, main_widget


class WarnoPathDialog(BaseDialog):
    def __init__(self, config_values: dict):
        self.warning_label = QtWidgets.QLabel("WARNING! Uploading this mod might fail if it's name does not match "
                                              "the name of the directory (" +
                                              main_widget.instance.get_loaded_mod_name() + ")")
        self.description_text_edit = QtWidgets.QTextEdit()
        self.icon_path_line_edit = wme_essentials.WMELineEdit()
        self.config_values = config_values
        # copy for warning on cancel
        self.orig_config_values = config_values.copy()

        super().__init__()
        self.setWindowTitle("Edit mod configuration")

    def setup_ui(self):
        form_layout = QtWidgets.QFormLayout(self)
        self.main_layout.addLayout(form_layout)

        name_line_edit = wme_essentials.WMELineEdit()
        name_line_edit.setText(str(self.config_values["Properties/Name"]))
        name_line_edit.textChanged.connect(self.on_name_changed)
        name_label = QtWidgets.QLabel("Name")
        name_label.setToolTip("The name of the mod as it will be displayed in-game.")
        form_layout.addRow(name_label, name_line_edit)

        if not bool(name_line_edit.text()):
            self.warning_label.setHidden(True)
        else:
            self.warning_label.setHidden(name_line_edit.text() == main_widget.instance.get_loaded_mod_name())
        self.warning_label.setWordWrap(True)
        form_layout.addWidget(self.warning_label)

        self.description_text_edit.setPlainText(str(self.config_values["Properties/Description"]))
        self.description_text_edit.textChanged.connect(self.on_description_changed)
        description_label = QtWidgets.QLabel("Description")
        description_label.setToolTip("A short description of the mod that will be displayed on Steam Workshop.")
        form_layout.addRow(description_label, self.description_text_edit)

        self.icon_path_line_edit.setText(str(self.config_values["Properties/PreviewImagePath"]))
        self.icon_path_line_edit.textChanged.connect(self.on_icon_path_changed)
        browse_button = QtWidgets.QPushButton()
        browse_button.setText("Browse..")
        browse_button.clicked.connect(self.on_icon_browse)
        icon_path_layout = QtWidgets.QHBoxLayout()
        icon_path_layout.addWidget(self.icon_path_line_edit)
        icon_path_layout.addWidget(browse_button)
        icon_path_label = QtWidgets.QLabel("Preview Image Path")
        icon_path_label.setToolTip("Path to a file which will be the preview image of the mod on Steam Workshop.")
        form_layout.addRow(icon_path_label, icon_path_layout)

        cosmetic_checkbox = QtWidgets.QCheckBox()
        cosmetic_checkbox.setChecked(int(self.config_values["Properties/CosmeticOnly"]))
        cosmetic_checkbox.stateChanged.connect(self.on_cosmetic_changed)
        cosmetic_label = QtWidgets.QLabel("Cosmetic only")
        cosmetic_label.setToolTip("Check this box if the mod does not affect gameplay.")
        form_layout.addRow(cosmetic_label, cosmetic_checkbox)

        mod_version_spinbox = wme_essentials.WMESpinbox()
        mod_version_spinbox.setMinimum(0)
        mod_version_spinbox.setValue(int(self.config_values["Properties/Version"]))
        mod_version_spinbox.valueChanged.connect(self.on_mod_version_changed)
        mod_version_label = QtWidgets.QLabel("Mod Version")
        mod_version_label.setToolTip("Increment this value to invalidate when an update of the mod is "
                                     "no longer compatible with older versions.")
        form_layout.addRow(mod_version_label, mod_version_spinbox)

        deck_format_version_spinbox = wme_essentials.WMESpinbox()
        deck_format_version_spinbox.setMinimum(0)
        deck_format_version_spinbox.setValue(int(self.config_values["Properties/DeckFormatVersion"]))
        deck_format_version_spinbox.valueChanged.connect(self.on_deck_format_version_changed)
        deck_format_version_label = QtWidgets.QLabel("Deck Format Version")
        deck_format_version_label.setToolTip("Set this at least to 1 if the mod affects gameplay.\n"
                                             "Increment this value to invalidate decks of older versions of the mod.")
        form_layout.addRow(deck_format_version_label, deck_format_version_spinbox)

    def on_name_changed(self, name: str):
        self.config_values["Properties/Name"] = name
        if not bool(name):
            self.warning_label.setHidden(True)
        else:
            self.warning_label.setHidden(name == main_widget.instance.get_loaded_mod_name())

    def on_description_changed(self):
        self.config_values["Properties/Description"] = self.description_text_edit.toPlainText()

    def on_icon_path_changed(self, icon_path: str):
        self.config_values["Properties/PreviewImagePath"] = icon_path

    def on_icon_browse(self):
        icon_path = self.icon_path_line_edit.text()
        if not QtCore.QDir(icon_path).exists():
            icon_path = str(Path.home())
        icon_path, _ = QtWidgets.QFileDialog().getOpenFileName(self, "Select preview image", icon_path,
                                                               options=QtWidgets.QFileDialog.ReadOnly)
        self.icon_path_line_edit.setText(icon_path)

    def on_cosmetic_changed(self, state):
        self.config_values["Properties/CosmeticOnly"] = state

    def on_mod_version_changed(self, version):
        self.config_values["Properties/Version"] = version

    def on_deck_format_version_changed(self, version):
        self.config_values["Properties/DeckFormatVersion"] = version

    def get_config_values(self):
        return self.config_values

    def reject(self) -> None:
        if self.config_values != self.orig_config_values:
            dialog = essential_dialogs.ConfirmationDialog("All changes will be lost. Do you want to continue?",
                                                          "Warning!")
            if not dialog.exec_():
                return
        return super().reject()
