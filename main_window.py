import sys

from PySide2 import QtWidgets, QtCore

import warno_path_dialog, main_widget

SETTINGS_WARNO_PATH_KEY = "wme_warno_path"


class MainWindow(QtWidgets.QMainWindow):
    quit_app = QtCore.Signal(int)

    def __init__(self):
        super().__init__()
        self.warno_path = ""
        self.dialog_finished_once = False
        self.settings = QtCore.QSettings("jonitro", "WarnoModEditor")
        QtCore.QTimer.singleShot(0, self.load_warno_path_from_settings)

    # open actual main window
    def start_main_window(self):
        self.resize(1152, 648)
        self.setWindowTitle("WARNO Mod Editor")
        self.setCentralWidget(main_widget.MainWidget(self.warno_path, self.settings))
        self.showNormal()

    def validate_warno_path(self, warno_path):
        if QtCore.QFile().exists(warno_path + "/WARNO.exe") and QtCore.QDir(warno_path + "/Mods").exists():
            self.warno_path = warno_path
            self.settings.setValue(SETTINGS_WARNO_PATH_KEY, warno_path)
            self.start_main_window()
            return
        if self.dialog_finished_once:
            QtWidgets.QMessageBox().information(self, "Path invalid",
                                                      "The WARNO path appears to be invalid. "
                                                      "Please enter the correct path.")
        self.open_warno_path_dialog()

    def load_warno_path_from_settings(self):
        tmp_path = self.settings.value(SETTINGS_WARNO_PATH_KEY)
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

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    QtWidgets.QApplication.instance().setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)
    main_window = MainWindow()
    sys.exit(app.exec_())