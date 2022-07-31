import logging

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from wme_widgets import wme_menu_bar, wme_project_explorer
from wme_widgets.tab_widget import wme_tab_widget
from utils import settings_manager, path_validator


def set_status_text(text: str):
    MainWidget.instance.status_set_text.emit(text)


class MainWidget(QtWidgets.QWidget):
    status_set_text = QtCore.Signal(str)
    mod_loaded = QtCore.Signal(str)
    instance = None

    def __init__(self, warno_path: str, title_bar):
        super().__init__()
        self.explorer = wme_project_explorer.WMEProjectExplorer(self)
        self.load_screen = QtWidgets.QLabel("Open the \"File\" menu to create or load a mod.")
        self.splitter = QtWidgets.QSplitter(self)
        self.tab_widget = wme_tab_widget.WMETabWidget()
        self.menu_bar = wme_menu_bar.WMEMainMenuBar(main_widget_ref=self)
        self.loaded_mod_path = ""
        self.loaded_mod_name = ""
        self.explorer_width = 0
        self.warno_path = warno_path
        self.status_label = QtWidgets.QLabel()
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(self.on_status_timeout)
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

        self.explorer.open_ndf_editor.connect(self.tab_widget.on_open_ndf_editor)

        label_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(label_layout)

        # TODO: set version in settings/as variable somewhere
        version_label = QtWidgets.QLabel("WME v0.1.0")
        label_layout.addWidget(version_label)
        label_layout.setAlignment(version_label, Qt.AlignLeft)
        label_layout.addWidget(self.status_label)
        label_layout.setAlignment(self.status_label, Qt.AlignRight)

        self.status_set_text.connect(self.on_status_set_text)

    def on_status_set_text(self, text: str):
        self.status_label.setText(text)
        self.status_timer.setInterval(5000)
        self.status_timer.start()

    def on_status_timeout(self):
        self.status_label.setText("")
        self.status_timer.stop()

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
        self.hide_loading_screen()

    def ask_all_tabs_to_save(self):
        if not self.tab_widget.ask_all_tabs_to_save(all_windows=True):
            return False
        # TODO: ask all tabs if progress needs to be saved
        # TODO: open one dialog to save, discard, or cancel for each with unsaved progress
        # TODO: if all return save/discard, perform actions and return true
        # TODO: if one returns cancel, return false
        return True

    def show_loading_screen(self, text: str = "loading..."):
        self.load_screen.setText(text)
        self.load_screen.setHidden(False)
        self.splitter.setHidden(True)
        QtWidgets.QApplication.processEvents()

    def hide_loading_screen(self):
        self.load_screen.setHidden(True)
        self.splitter.setHidden(False)
        QtWidgets.QApplication.processEvents()

    def eventFilter(self, source, event) -> bool:
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if self.splitter.sizes()[0] > 0:
                self.explorer_width = self.explorer.width()
                self.splitter.setSizes([0, self.tab_widget.width() + self.explorer_width])
            else:
                self.splitter.setSizes([self.explorer_width, self.tab_widget.width() - self.explorer_width])
        return False




