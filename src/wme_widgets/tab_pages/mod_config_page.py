from pathlib import Path

from PySide6 import QtWidgets, QtCore

from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import wme_essentials, wme_steam_text_edit, main_widget
from src.dialogs import essential_dialogs

from src.utils import icon_manager
from src.utils.color_manager import *


class ModConfigPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()
        self.deck_format_version_spinbox = wme_essentials.WMESpinbox()
        self.mod_version_spinbox = wme_essentials.WMESpinbox()
        self.cosmetic_checkbox = QtWidgets.QCheckBox()
        self.name_line_edit = wme_essentials.WMELineEdit()
        self.warning_label = QtWidgets.QLabel("WARNING! Uploading this mod might fail if it's name does not match "
                                              "the name of the directory (" +
                                              main_widget.instance.get_loaded_mod_name() + ")")
        self.description_text_edit = wme_steam_text_edit.WMESteamTextEdit()
        self.icon_path_line_edit = wme_essentials.WMELineEdit()
        self.config_values = None

        self.setup_ui()
        self.load_config()

        # TODO: help page

    def reload_page(self):
        if self.unsaved_changes:
            dialog = essential_dialogs.ConfirmationDialog("Your changes will be discarded! Are you sure?", "Warning!")
            if not dialog.exec():
                return
        self.load_config()

    def load_config(self):
        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      main_widget.instance.get_loaded_mod_name() + "\\Config.ini"

        if not QtCore.QFile.exists(config_path):
            logging.error("Config file does not exist!")
            return

        config = QtCore.QSettings(config_path, QtCore.QSettings.IniFormat)
        self.config_values = {}
        for key in config.allKeys():
            if key == "Properties/Description" and not config.value(key).startswith("\""):
                self.config_values[key] = "\"" + config.value(key) + "\""
            else:
                self.config_values[key] = config.value(key)

        self.set_values()

    def _save_changes(self):
        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      main_widget.instance.get_loaded_mod_name() + "\\Config.ini"

        if not QtCore.QFile.exists(config_path):
            logging.error("Config file does not exist!")
            return False

        config = QtCore.QSettings(config_path, QtCore.QSettings.IniFormat)

        self.config_values = self.get_config_values()
        for key in config.allKeys():
            config.setValue(key, self.config_values[key])

        # delete QSettings object so file can be edited
        del config

        # replace to make the file readable for Eugen...
        with open(config_path, "r+") as f:
            f_content = f.read()
            f_content = f_content.replace("=", " = ")
            f_content = f_content.replace("url = ", "url=")
            f.seek(0)
            f.write(f_content)

        return True

    def get_config_values(self):
        config_values = self.config_values.copy()
        config_values["Properties/Name"] = self.name_line_edit.text()
        config_values["Properties/Description"] = self.description_text_edit.get_text()
        if not config_values["Properties/Description"].startswith("\""):
            text = config_values["Properties/Description"]
            config_values["Properties/Description"] = f"\"{text}\""
        config_values["Properties/PreviewImagePath"] = self.icon_path_line_edit.text()
        config_values["Properties/CosmeticOnly"] = "1" if self.cosmetic_checkbox.isChecked() else "0"
        config_values["Properties/Version"] = str(self.mod_version_spinbox.value())
        config_values["Properties/DeckFormatVersion"] = str(self.deck_format_version_spinbox.value())
        return config_values

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        save_action = tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        restore_action = tool_bar.addAction(icon_manager.load_icon("restore.png", COLORS.PRIMARY), "Reload Config (F5)")
        restore_action.setShortcut("F5")
        restore_action.triggered.connect(self.reload_page)

        stretch = QtWidgets.QWidget()
        stretch.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        tool_bar.addWidget(stretch)

        help_action = tool_bar.addAction(icon_manager.load_icon("help.png", COLORS.PRIMARY),
                                         "Open Page Help Popup (Alt + H)")
        help_action.triggered.connect(self.on_help)

        scroll_widget = QtWidgets.QWidget()
        form_layout = QtWidgets.QFormLayout()
        scroll_widget.setLayout(form_layout)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(scroll_widget)

        main_layout.addWidget(scroll_area)

        self.name_line_edit.textChanged.connect(self.on_name_changed)
        self.name_line_edit.textChanged.connect(self.check_unsaved_changes)
        name_label = QtWidgets.QLabel("Name")
        name_label.setToolTip("The name of the mod as it will be displayed in-game.")
        form_layout.addRow(name_label, self.name_line_edit)

        self.on_name_changed(self.name_line_edit.text())
        self.warning_label.setWordWrap(True)
        form_layout.addWidget(self.warning_label)

        self.description_text_edit.text_edit.textChanged.connect(self.check_unsaved_changes)
        description_label = QtWidgets.QLabel("Description")
        description_label.setToolTip("A short description of the mod that will be displayed on Steam Workshop.")
        form_layout.addRow(description_label, self.description_text_edit)

        self.icon_path_line_edit.textChanged.connect(self.check_unsaved_changes)
        browse_button = QtWidgets.QPushButton()
        browse_button.setText("Browse..")
        browse_button.clicked.connect(self.on_icon_browse)
        icon_path_layout = QtWidgets.QHBoxLayout()
        icon_path_layout.addWidget(self.icon_path_line_edit)
        icon_path_layout.addWidget(browse_button)
        icon_path_label = QtWidgets.QLabel("Preview Image Path")
        icon_path_label.setToolTip("Path to a file which will be the preview image of the mod on Steam Workshop.")
        form_layout.addRow(icon_path_label, icon_path_layout)

        self.cosmetic_checkbox.stateChanged.connect(self.check_unsaved_changes)
        cosmetic_label = QtWidgets.QLabel("Cosmetic only")
        cosmetic_label.setToolTip("Check this box if the mod does not affect gameplay.")
        form_layout.addRow(cosmetic_label, self.cosmetic_checkbox)

        self.mod_version_spinbox.setMinimum(0)
        self.mod_version_spinbox.valueChanged.connect(self.check_unsaved_changes)
        mod_version_label = QtWidgets.QLabel("Mod Version")
        mod_version_label.setToolTip("Increment this value to invalidate when an update of the mod is "
                                     "no longer compatible with older versions.")
        form_layout.addRow(mod_version_label, self.mod_version_spinbox)

        self.deck_format_version_spinbox.setMinimum(0)
        self.deck_format_version_spinbox.valueChanged.connect(self.check_unsaved_changes)
        deck_format_version_label = QtWidgets.QLabel("Deck Format Version")
        deck_format_version_label.setToolTip("Set this at least to 1 if the mod affects gameplay.\n"
                                             "Increment this value to invalidate decks of older versions of the mod.")
        form_layout.addRow(deck_format_version_label, self.deck_format_version_spinbox)

    def set_values(self):
        self.name_line_edit.setText(str(self.config_values["Properties/Name"]))
        self.description_text_edit.set_text(str(self.config_values["Properties/Description"]))
        self.icon_path_line_edit.setText(str(self.config_values["Properties/PreviewImagePath"]))
        self.cosmetic_checkbox.setChecked(True if int(self.config_values["Properties/CosmeticOnly"]) != 0 else False)
        self.mod_version_spinbox.setValue(int(self.config_values["Properties/Version"]))
        self.deck_format_version_spinbox.setValue(int(self.config_values["Properties/DeckFormatVersion"]))

    def on_name_changed(self, name):
        if not bool(name):
            self.warning_label.setHidden(True)
        else:
            self.warning_label.setHidden(name == main_widget.instance.get_loaded_mod_name())

    def on_icon_browse(self):
        path = QtWidgets.QFileDialog.getOpenFileName(self, "Select Icon", "", "Image Files (*.png *.jpg *.bmp)")[0]
        if path:
            self.icon_path_line_edit.setText(path)

    def check_unsaved_changes(self):
        self.unsaved_changes = self.config_values != self.get_config_values()
