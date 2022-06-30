import logging

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

from wme_widgets import wme_menu_bar, wme_tab_widget
from utils import settings_manager, path_validator


def set_status_text(text: str):
    MainWidget.instance.status_set_text.emit(text)


class MainWidget(QtWidgets.QWidget):
    status_set_text = QtCore.Signal(str)
    mod_loaded = QtCore.Signal(str)
    instance = None

    def __init__(self, warno_path: str, title_bar):
        super().__init__()
        self.menu_bar = wme_menu_bar.WMEMainMenuBar(main_widget_ref=self)
        self.loaded_mod_path = ""
        self.loaded_mod_name = ""
        self.warno_path = warno_path
        self.status_label = QtWidgets.QLabel()
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(lambda: self.status_label.setText(""))
        self.title_bar = title_bar
        self.title_label = QtWidgets.QLabel("No mod loaded")
        self.setup_ui()
        MainWidget.instance = self
        last_open = settings_manager.get_settings_value(settings_manager.LAST_OPEN_KEY)
        if last_open is None:
            return
        if path_validator.validate_mod_path(str(last_open)):
            self.load_mod(str(last_open))

    def get_warno_path(self):
        return self.warno_path

    def get_loaded_mod_path(self):
        return self.loaded_mod_path

    def get_loaded_mod_name(self):
        return self.loaded_mod_name

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)

        self.title_label.setObjectName("title")
        self.title_bar.add_widget(self.title_label)
        self.title_bar.add_spacing(10)
        self.title_bar.add_widget(self.menu_bar)

        self.menu_bar.request_load_mod.connect(self.load_mod)

        tab_widget = wme_tab_widget.WMETabWidget()
        main_layout.addWidget(tab_widget)

        main_layout.addWidget(self.status_label)
        main_layout.setAlignment(self.status_label, Qt.AlignRight)

        self.status_set_text.connect(self.on_status_set_text)

    def on_status_set_text(self, text: str):
        self.status_label.setText(text)
        self.status_timer.setInterval(5000)
        self.status_timer.start()

    def load_mod(self, mod_path: str):
        mod_path = mod_path.replace("/", "\\")
        if mod_path == self.loaded_mod_path:
            return

        self.loaded_mod_path = mod_path
        self.loaded_mod_name = mod_path[mod_path.rindex('\\') + 1:]
        logging.info("loaded mod " + self.loaded_mod_name + " at " + mod_path)
        self.title_label.setText(self.loaded_mod_name)
        settings_manager.write_settings_value(settings_manager.LAST_OPEN_KEY, mod_path)
        self.mod_loaded.emit(mod_path)
        set_status_text(self.loaded_mod_name + " was loaded successfully")

    def ask_all_tabs_to_save(self):
        # TODO: ask all tabs if progress needs to be saved
        # TODO: open one dialog to save, discard, or cancel for each with unsaved progress
        # TODO: if all return save/discard, perform actions and return true
        # TODO: if one returns cancel, return false
        return True
