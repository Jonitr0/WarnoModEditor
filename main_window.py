from PySide2 import QtWidgets, QtCore

import main_widget
import wme_title_bar
from dialogs import warno_path_dialog
from utils import settings_manager, path_validator


# TODO: move warno path verification to own class

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.warno_path = ""
        self.dialog_finished_once = False
        self.main_widget_ref = None
        QtCore.QTimer.singleShot(0, self.load_warno_path_from_settings)

    # open actual main window
    def start_main_window(self):
        self.resize(1152, 648)
        self.setWindowTitle("WARNO Mod Editor")

        w = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        w.setLayout(main_layout)

        bar = wme_title_bar.WMETitleBar(parent=self)
        main_layout.addWidget(bar)
        self.main_widget_ref = main_widget.MainWidget(self.warno_path, bar)
        main_layout.addWidget(self.main_widget_ref)

        self.setCentralWidget(w)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(16, 16)

        self.showNormal()

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        self.grip.move(rect.right() - 16, rect.bottom() - 16)

    def validate_warno_path(self, warno_path):
        if path_validator.validate_warno_path(warno_path):
            self.warno_path = warno_path
            settings_manager.write_settings_value(settings_manager.WARNO_PATH_KEY, warno_path)
            self.start_main_window()
            return
        if self.dialog_finished_once:
            QtWidgets.QMessageBox().information(self, "Path invalid",
                                                "The WARNO path appears to be invalid. "
                                                "Please enter the correct path.")
        self.open_warno_path_dialog()

    def load_warno_path_from_settings(self):
        tmp_path = settings_manager.get_settings_value(settings_manager.WARNO_PATH_KEY)
        if tmp_path is None:
            self.open_warno_path_dialog()
        else:
            self.validate_warno_path(str(tmp_path))

    def open_warno_path_dialog(self):
        tmp_path = "C:\Program Files (x86)\Steam\steamapps\common\WARNO"
        if not QtCore.QDir(tmp_path).exists():
            tmp_path = QtCore.QDir().currentPath()

        path_dialog = warno_path_dialog.WarnoPathDialog(tmp_path)
        result = path_dialog.exec()

        if result == QtWidgets.QDialog.Accepted:
            self.warno_path = path_dialog.get_path()
            self.dialog_finished_once = True
            self.validate_warno_path(self.warno_path)
        elif result == QtWidgets.QDialog.Rejected:
            QtCore.QCoreApplication.quit()

    def close(self):
        if self.main_widget_ref.ask_all_tabs_to_save():
            super().close()


