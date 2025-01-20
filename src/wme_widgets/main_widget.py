import logging
import threading
import time
import requests

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets import wme_menu_bar, base_window
from src.wme_widgets.project_explorer import wme_project_explorer
from src.wme_widgets.tab_widget import wme_tab_widget, wme_detached_tab
from src.dialogs import log_dialog, essential_dialogs
from src.utils import path_validator, icon_manager, auto_backup_manager, mod_settings_loader
from src.utils.color_manager import *
from src.assets import asset_string_manager, asset_icon_manager
from src.ndf import unit_loader

from pydoc import locate


class ThreadWithReturnValue(threading.Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        threading.Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)
        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self, *args):
        threading.Thread.join(self, *args)
        return self._return

    def get_return(self):
        return self._return


def restore_window(window_obj: dict, window: base_window.BaseWindow):
    window.move(window_obj["x"], window_obj["y"])
    if window_obj["maximized"]:
        window.setWindowState(Qt.WindowMaximized)
        window.title_bar.set_maximized(True)
    else:
        window.resize(window_obj["width"], window_obj["height"])


class MainWidget(QtWidgets.QWidget):
    status_set_text = QtCore.Signal(str)
    mod_loaded = QtCore.Signal(str)
    mod_unloaded = QtCore.Signal()

    def __init__(self, parent, warno_path: str, title_bar):
        super().__init__(parent=parent)
        self.explorer = wme_project_explorer.WMEProjectExplorer(self)
        self.no_mod_loaded_msg = "Open the \"File\" menu (Alt + F) to create a new mod (Ctrl + Alt + N) or open an" \
                                 " existing one (Ctrl + Alt + O)."
        self.load_screen = QtWidgets.QLabel(self.no_mod_loaded_msg)
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
        self.progress_label = QtWidgets.QLabel("")
        self.progress_bar = QtWidgets.QProgressBar()
        self.log_dialog = log_dialog.LogDialog()
        self.auto_backup_manager = auto_backup_manager.AutoBackupManager(self)
        self.unit_loader = unit_loader.UnitLoader(parent=self)
        self.unit_loader.request_update_progress.connect(self.set_progress)
        self.running_threads = []

        self.auto_backup_manager.request_backup.connect(self.menu_bar.create_named_backup)
        self.mod_loaded.connect(self.auto_backup_manager.update_settings)

        self.asset_string_manager = asset_string_manager.AssetStringManager(self)
        self.mod_loaded.connect(self.asset_string_manager.load_asset_strings)
        self.asset_icon_manager = asset_icon_manager.AssetIconManager()
        self.mod_loaded.connect(self.asset_icon_manager.load_asset_icons)

        self.log_dialog.new_log.connect(self.on_new_log)
        self.log_dialog.error_log.connect(self.on_error_log)

        self.setup_ui()

        global instance
        instance = self

        last_open = settings_manager.get_settings_value(settings_manager.LAST_OPEN_KEY)
        if last_open is None:
            return
        if path_validator.validate_mod_path(str(last_open)):
            self.load_mod(str(last_open))

        try:
            self.load_main_window_state()
        except Exception as e:
            logging.warning("Error while loading WME config: " + str(e))

        try:
            response = requests.get("https://api.github.com/repos/Jonitr0/WarnoModEditor/releases/latest")
        except Exception as e:
            logging.warning("Error while fetching version data from GitHub: " + str(e))
            return

        version = settings_manager.get_settings_value(settings_manager.VERSION_KEY)
        last_reported_version = settings_manager.get_settings_value(settings_manager.LAST_REPORTED_VERSION_KEY)
        new_version = response.json()["tag_name"]

        if version == new_version or new_version == last_reported_version:
            return

        hyperlink_color = get_color_for_key(COLORS.PRIMARY.value)
        download_url = response.json()["html_url"]
        text = "WME version " + new_version + " is available! You can download it <a style=\"color: " + \
               hyperlink_color + "\" href=\"" + download_url + "\">here</a>. It includes the following changes:<br>"
        for change in response.json()["body"].split("\r\n"):
            text += "<br>" + change

        essential_dialogs.MessageDialog("Update Available", text, rich_text=True).exec()

        settings_manager.write_settings_value(settings_manager.LAST_REPORTED_VERSION_KEY, new_version)

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

        self.mod_loaded.connect(self.explorer.update_model)
        self.explorer.request_open_explorer.connect(self.on_open_explorer)

        self.splitter.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.splitter.addWidget(self.explorer)
        self.splitter.addWidget(self.tab_widget)
        self.splitter.handle(1).installEventFilter(self)
        self.splitter.setCollapsible(1, False)
        self.splitter.setHidden(True)
        main_layout.addWidget(self.splitter)

        self.load_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.load_screen.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.load_screen)

        self.explorer.tree_view.open_text_editor.connect(self.tab_widget.on_open_ndf_editor)
        self.explorer.tree_view.open_csv_editor.connect(self.tab_widget.on_open_csv_editor)
        self.explorer.tree_view.image_preview.connect(self.tab_widget.on_open_image_preview)
        self.explorer.tree_view.restore_backup.connect(self.menu_bar.retrieve_backup)

        separator = QtWidgets.QWidget()
        separator.setObjectName("separator")
        separator.setFixedHeight(1)
        main_layout.addWidget(separator)

        label_layout = QtWidgets.QHBoxLayout()
        label_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addLayout(label_layout)

        version_label = QtWidgets.QLabel("WME v" + settings_manager.get_settings_value(settings_manager.VERSION_KEY))
        label_layout.addWidget(version_label)

        self.progress_label.setFixedWidth(150)
        self.progress_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        label_layout.addWidget(self.progress_label)
        self.progress_label.setHidden(True)

        self.progress_bar.setRange(1, 100)
        self.progress_bar.setFixedHeight(20)
        self.progress_bar.setAlignment(Qt.AlignVCenter)
        self.progress_bar.setHidden(True)
        label_layout.addWidget(self.progress_bar)
        label_layout.addStretch(1)

        self.log_button.setText("Event Log")
        self.log_button.setIcon(icon_manager.load_icon("message_empty.png", COLORS.SECONDARY_TEXT))
        self.log_button.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.log_button.setFixedHeight(36)
        self.log_button.setToolTip("Open the event log for the current session (Ctrl + L)")
        self.log_button.clicked.connect(self.on_log_button_clicked)

        log_shortcut = QtGui.QShortcut("Ctrl+L", self.log_button, self.on_log_button_clicked)
        log_shortcut.setContext(Qt.ApplicationShortcut)

        label_layout.addWidget(self.log_button)

    def load_mod(self, mod_path: str):
        self.unload_mod()

        mod_path = mod_path.replace("/", "\\")
        if mod_path == self.loaded_mod_path:
            return

        self.loaded_mod_path = mod_path
        self.loaded_mod_name = mod_path[mod_path.rindex('\\') + 1:]
        logging.info("loaded mod " + self.loaded_mod_name + " at " + mod_path)

        self.unit_loader.mod_path = mod_path
        self.unit_loader.load_units()

        self.title_label.setText(" " + self.loaded_mod_name)
        settings_manager.write_settings_value(settings_manager.LAST_OPEN_KEY, mod_path)
        self.mod_loaded.emit(mod_path)
        self.tab_widget.close_all(all_windows=True)
        self.window().setWindowTitle(self.loaded_mod_name)
        self.hide_loading_screen()

        try:
            self.load_mod_state()
        except Exception as e:
            logging.info("Project state could not be restored: " + str(e))

    def unload_mod(self):
        if self.loaded_mod_name != "":
            self.save_mod_state()

        self.tab_widget.close_all(True)
        self.unit_loader.terminate()
        self.loaded_mod_path = ""
        self.loaded_mod_name = ""
        self.title_label.setText("")
        self.show_loading_screen(self.no_mod_loaded_msg, disable_menu=False)
        settings_manager.write_settings_value(settings_manager.MOD_STATE_CHANGED_KEY, 0)
        self.mod_unloaded.emit()

    def ask_all_tabs_to_save(self):
        # ask all tabs on all windows to save/discard, return False on cancel
        return self.tab_widget.ask_all_tabs_to_save(all_windows=True)

    def show_loading_screen(self, text: str = "loading...", disable_menu: bool = True):
        self.load_screen.setText(text)
        self.load_screen.setHidden(False)
        self.splitter.setHidden(True)
        if disable_menu:
            self.menu_bar.setEnabled(False)
            self.window().title_bar.close_button.setEnabled(False)

        for detached in wme_detached_tab.detached_list:
            detached.show_loading_screen(text)

        QtWidgets.QApplication.processEvents()

    def hide_loading_screen(self):
        QtWidgets.QApplication.processEvents()

        self.menu_bar.setEnabled(True)
        self.window().title_bar.close_button.setEnabled(True)
        self.load_screen.setHidden(True)
        self.splitter.setHidden(False)

        for detached in wme_detached_tab.detached_list:
            detached.hide_loading_screen()

    def eventFilter(self, source, event) -> bool:
        if event.type() == QtCore.QEvent.MouseButtonDblClick:
            if self.splitter.sizes()[0] > 0:
                self.explorer_width = self.explorer.width()
                self.splitter.setSizes([0, self.tab_widget.width() + self.explorer_width])
            else:
                self.splitter.setSizes([self.explorer_width, self.tab_widget.width() - self.explorer_width])
        return False

    def on_open_explorer(self):
        if self.loaded_mod_name == "":
            return

        if self.splitter.sizes()[0] == 0:
            self.splitter.setSizes([self.explorer_width, self.tab_widget.width() - self.explorer_width])

    def on_log_button_clicked(self):
        self.log_button.setIcon(icon_manager.load_icon("message_empty.png", COLORS.SECONDARY_TEXT))
        self.log_dialog.exec_()

    def on_new_log(self):
        self.log_button.setIcon(icon_manager.load_icon("new_log.png", COLORS.SECONDARY_TEXT))

    def on_error_log(self):
        self.log_button.setIcon(icon_manager.load_icon("error_log.png", COLORS.SECONDARY_TEXT))

    def on_quit(self):
        self.unload_mod()

        next_theme = settings_manager.get_settings_value(settings_manager.NEXT_THEME_KEY)
        if next_theme:
            settings_manager.write_settings_value(settings_manager.THEME_KEY, next_theme)

        try:
            json_obj = settings_manager.get_settings_value(settings_manager.APP_STATE, default={})

            main_window_state = self.window().get_window_state()
            main_window_state["splitterSizes"] = self.splitter.sizes()
            main_window_state["explorerWidth"] = self.explorer_width
            json_obj["mainWindowState"] = main_window_state

            settings_manager.write_settings_value(settings_manager.APP_STATE, json_obj)
        except Exception as e:
            logging.error("Could not save workspace state: " + str(e))

    def load_main_window_state(self):
        json_obj = settings_manager.get_settings_value(settings_manager.APP_STATE)
        if not json_obj:
            return

        main_window_obj = json_obj["mainWindowState"]

        # restore main window state
        restore_window(main_window_obj, self.parent())

        self.splitter.setSizes(main_window_obj["splitterSizes"])
        self.explorer_width = main_window_obj["explorerWidth"]

    def save_mod_state(self):
        mod_state = mod_settings_loader.get_mod_settings()

        main_window_tabs = self.tab_widget.to_json()
        mod_state["mainWindowTabs"] = main_window_tabs

        detached_objs = []
        for detached in wme_detached_tab.detached_list:
            detached_obj = {
                "detachedState": detached.get_window_state(),
                "detachedTabs": detached.tab_widget.to_json(),
            }
            detached_objs.append(detached_obj)

        mod_state["detached"] = detached_objs

        mod_settings_loader.set_mod_settings(mod_state)

    def load_mod_state(self):
        mod_state = mod_settings_loader.get_mod_settings()
        if mod_state == {}:
            return

        main_window_tabs = mod_state["mainWindowTabs"]
        for tab in main_window_tabs:
            if "do_not_restore" in tab:
                continue
            t = locate(tab["type"])
            page = t()
            page.from_json(tab)
            self.tab_widget.add_tab_with_auto_icon(page, tab["title"])

        detached_list = mod_state["detached"]
        for detached_obj in detached_list:
            detached_window = wme_detached_tab.WMEDetachedTab()
            restore_window(detached_obj["detachedState"], detached_window)
            for tab in detached_obj["detachedTabs"]:
                if "do_not_restore" in tab:
                    continue
                t = locate(tab["type"])
                page = t()
                page.from_json(tab)
                detached_window.tab_widget.add_tab_with_auto_icon(page, tab["title"])

            detached_window.show()

    def run_worker_thread(self, target, *args):
        # clean up dead threads
        self.running_threads = [t for t in self.running_threads if t.is_alive()]

        thread = ThreadWithReturnValue(target=target, args=args)
        thread.start()
        self.running_threads.append(thread)
        return thread

    def wait_for_worker_thread(self, thread):
        while thread.is_alive():
            QtWidgets.QApplication.processEvents()
            time.sleep(0.01)
        return thread.get_return()

    def set_progress(self, progress: float, text: str = "Loading..."):
        if progress >= 1:
            self.progress_bar.setHidden(True)
            self.progress_label.setHidden(True)
            return
        self.progress_bar.setHidden(False)
        self.progress_bar.setValue(int(progress * 100))
        self.progress_label.setHidden(False)
        self.progress_label.setText(text)


instance: MainWidget = None
