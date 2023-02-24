from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets import base_window, main_widget
from src.wme_widgets.tab_widget import wme_detached_tab
from src.utils import settings_manager, warno_path_loader, icon_manager


class MainWindow(base_window.BaseWindow):
    def __init__(self):
        super().__init__()
        self.main_widget_ref = None
        QtCore.QTimer.singleShot(0, self.start_main_window)

    # open actual main window
    def start_main_window(self):
        # write a standard path if there is no defined path
        tmp_path = "C:\\Program Files (x86)\\Steam\\steamapps\\common\\WARNO"
        if settings_manager.get_settings_value(settings_manager.WARNO_PATH_KEY) is None:
            settings_manager.write_settings_value(settings_manager.WARNO_PATH_KEY, tmp_path)

        if not warno_path_loader.load_warno_path_from_settings():
            QtCore.QCoreApplication.quit()

        warno_path = settings_manager.get_settings_value(settings_manager.WARNO_PATH_KEY)
        self.resize(1408, 792)
        self.setWindowTitle("WARNO Mod Editor")
        self.setWindowIcon(QtGui.QIcon(icon_manager.load_colored_icon("app_icon_colored")))

        self.main_widget_ref = main_widget.MainWidget(warno_path, self.title_bar)
        self.bar_layout.addWidget(self.main_widget_ref)

        self.showNormal()

    def close(self):
        if self.main_widget_ref is None:
            super().close()
            QtWidgets.QApplication.quit()
        if self.main_widget_ref.ask_all_tabs_to_save():
            wme_detached_tab.clear_detached_list()
            super().close()
            QtWidgets.QApplication.quit()
