from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

import main_menu_bar
import ndf_editor_widget
from utils import icon_loader, settings_manager, path_validator


def set_status_text(text: str):
    MainWidget.instance.status_set_text.emit(text)


class MainWidget(QtWidgets.QWidget):
    status_set_text = QtCore.Signal(str)
    mod_loaded = QtCore.Signal(str)
    instance = None

    def __init__(self, warno_path: str, title_bar):
        super().__init__()
        self.menu_bar = main_menu_bar.MainMenuBar(main_widget_ref=self)
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

        tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(tab_widget)

        ndf_editor = ndf_editor_widget.NdfEditorWidget()
        tab_widget.addTab(ndf_editor, ".ndf Editor")
        cheat_sheet = QtWidgets.QWidget()
        tab_widget.addTab(cheat_sheet, "Modding Cheat Sheet")

        # TODO: add menu to select new tabs
        # TODO: style button
        new_tab_button = QtWidgets.QPushButton("Add Tab")
        new_tab_button.setIcon(icon_loader.load_icon("plusIcon.png"))
        tab_widget.setCornerWidget(new_tab_button)

        tab_widget.setTabsClosable(True)
        tab_widget.setMovable(True)
        # TODO: run save check
        tab_widget.tabCloseRequested.connect(tab_widget.removeTab)

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
        print("loaded mod " + self.loaded_mod_name + " at " + mod_path)
        self.title_label.setText(self.loaded_mod_name)
        settings_manager.write_settings_value(settings_manager.LAST_OPEN_KEY, mod_path)
        self.mod_loaded.emit(mod_path)
        set_status_text(self.loaded_mod_name + " was loaded successfully")

    def active_tab_ask_to_save(self):
        # TODO: ask the current tab if progress needs to be saved
        # TODO: open dialog to save, discard, or cancel
        # TODO: on save/discard perform action and return true
        # TODO: on cancel return false
        return True
