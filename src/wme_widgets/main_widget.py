import logging
import os.path

from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.wme_widgets import wme_menu_bar
from src.wme_widgets.project_explorer import wme_project_explorer
from src.wme_widgets.tab_widget import wme_tab_widget, wme_detached_tab
from src.dialogs import log_dialog
from src.utils import path_validator, icon_manager, resource_loader
from src.utils.color_manager import *

import json


class MainWidget(QtWidgets.QWidget):
    status_set_text = QtCore.Signal(str)
    mod_loaded = QtCore.Signal(str)
    instance = None

    def __init__(self, parent, warno_path: str, title_bar):
        super().__init__(parent=parent)
        self.explorer = wme_project_explorer.WMEProjectExplorer(self)
        self.load_screen = QtWidgets.QLabel("Open the \"File\" menu to create or load a mod.")
        self.splitter = QtWidgets.QSplitter(self)
        self.tab_widget = wme_tab_widget.WMETabWidget()
        self.menu_bar = wme_menu_bar.WMEMainMenuBar(main_widget_ref=self)
        self.loaded_mod_path = ""
        self.loaded_mod_name = ""
        self.explorer_width = 200
        self.warno_path = warno_path
        self.log_button = QtWidgets.QToolButton()
        self.status_timer = QtCore.QTimer()
        self.title_bar = title_bar
        self.title_label = QtWidgets.QLabel("")
        self.log_dialog = log_dialog.LogDialog()

        self.log_dialog.new_log.connect(self.on_new_log)
        self.log_dialog.error_log.connect(self.on_error_log)

        self.setup_ui()
        MainWidget.instance = self
        last_open = settings_manager.get_settings_value(settings_manager.LAST_OPEN_KEY)
        if last_open is None:
            return
        if path_validator.validate_mod_path(str(last_open)):
            self.load_mod(str(last_open))

        try:
            self.load_main_window_state()
        except Exception as e:
            logging.warning("Error while loading WME config: " + str(e))

    def get_warno_path(self):
        return self.warno_path

    def set_warno_path(self, warno_path):
        self.warno_path = warno_path

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
        self.menu_bar.request_quickstart.connect(self.tab_widget.on_open_quickstart)

        self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.mod_loaded.connect(self.explorer.update_model)
        self.splitter.addWidget(self.explorer)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.handle(1).installEventFilter(self)
        self.splitter.setCollapsible(1, False)
        self.splitter.setHidden(True)
        main_layout.addWidget(self.splitter)

        self.load_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.load_screen.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.load_screen)

        self.explorer.tree_view.open_ndf_editor.connect(self.tab_widget.on_open_ndf_editor)

        label_layout = QtWidgets.QHBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(label_layout)

        version_label = QtWidgets.QLabel("WME v" + settings_manager.get_settings_value(settings_manager.VERSION_KEY))
        label_layout.addWidget(version_label)
        label_layout.setAlignment(version_label, Qt.AlignLeft)

        self.log_button.setText("Event Log")
        self.log_button.setIcon(icon_manager.load_icon("message_empty.png", COLORS.SECONDARY_TEXT))
        self.log_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.log_button.setFixedHeight(36)
        self.log_button.setShortcut("Ctrl+L")
        self.log_button.setToolTip("Open the event log for the current session (Ctrl + L)")
        self.log_button.clicked.connect(self.on_log_button_clicked)

        label_layout.addWidget(self.log_button)
        label_layout.setAlignment(self.log_button, Qt.AlignRight)

    def load_mod(self, mod_path: str):
        self.unload_mod()

        mod_path = mod_path.replace("/", "\\")
        if mod_path == self.loaded_mod_path:
            return

        self.loaded_mod_path = mod_path
        self.loaded_mod_name = mod_path[mod_path.rindex('\\') + 1:]
        logging.info("loaded mod " + self.loaded_mod_name + " at " + mod_path)
        self.title_label.setText(" " + self.loaded_mod_name)
        settings_manager.write_settings_value(settings_manager.LAST_OPEN_KEY, mod_path)
        self.mod_loaded.emit(mod_path)
        self.tab_widget.close_all(all_windows=True)
        self.hide_loading_screen()

        # TODO: load open pages from config

    def unload_mod(self):
        # TODO: save mod specific config (tabs and detached)

        self.tab_widget.close_all(True)
        self.loaded_mod_path = ""
        self.loaded_mod_name = ""
        self.title_label.setText("")
        self.show_loading_screen("Open the \"File\" menu to create or load a mod.")

    def ask_all_tabs_to_save(self):
        # ask all tabs on all windows to save/discard, return False on cancel
        return self.tab_widget.ask_all_tabs_to_save(all_windows=True)

    def show_loading_screen(self, text: str = "loading..."):
        self.load_screen.setText(text)
        self.load_screen.setHidden(False)
        self.splitter.setHidden(True)

        for detached in wme_detached_tab.detached_list:
            detached.show_loading_screen(text)

        QtWidgets.QApplication.processEvents()

    def hide_loading_screen(self):
        self.load_screen.setHidden(True)
        self.splitter.setHidden(False)

        for detached in wme_detached_tab.detached_list:
            detached.hide_loading_screen()

        QtWidgets.QApplication.processEvents()

    def eventFilter(self, source, event) -> bool:
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if self.splitter.sizes()[0] > 0:
                self.explorer_width = self.explorer.width()
                self.splitter.setSizes([0, self.tab_widget.width() + self.explorer_width])
            else:
                self.splitter.setSizes([self.explorer_width, self.tab_widget.width() - self.explorer_width])
        return False

    def on_log_button_clicked(self):
        self.log_button.setIcon(icon_manager.load_icon("message_empty.png", COLORS.SECONDARY_TEXT))
        self.log_dialog.exec_()

    def on_new_log(self):
        self.log_button.setIcon(icon_manager.load_icon("new_log.png", COLORS.SECONDARY_TEXT))

    def on_error_log(self):
        self.log_button.setIcon(icon_manager.load_icon("error_log.png", COLORS.SECONDARY_TEXT))

    def on_quit(self):
        window_state = {
            "Maximized": self.window().isMaximized(),
            "Width": self.window().width(),
            "Height": self.window().height(),
            "X": self.window().pos().x(),
            "Y": self.window().pos().y(),
            "SplitterSizes": self.splitter.sizes(),
            "ExplorerWidth": self.explorer_width
        }

        self.tab_widget.to_json()

        json_str = json.dumps(window_state)
        file_path = resource_loader.get_persistant_path("wme_config.json")

        with open(file_path, "w+") as f:
            f.write(json_str)

    def load_main_window_state(self):
        file_path = resource_loader.get_persistant_path("wme_config.json")
        json_obj = None

        try:
            with open(file_path, "r") as f:
                json_obj = json.load(f)
        except Exception as e:
            logging.info("Config not found or could not be opened: " + str(e))
            return

        if json_obj["Maximized"]:
            self.parent().setWindowState(Qt.WindowMaximized)
            self.parent().title_bar.set_maximized(True)
        else:
            self.parent().move(json_obj["X"], json_obj["Y"])
            self.parent().resize(json_obj["Width"], json_obj["Height"])

        self.splitter.setSizes(json_obj["SplitterSizes"])
        self.explorer_width = json_obj["ExplorerWidth"]




