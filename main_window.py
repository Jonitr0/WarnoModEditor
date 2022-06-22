import sys
import os

from PySide2 import QtWidgets, QtCore, QtGui
from qt_material import apply_stylesheet

import main_widget
import title_bar
from dialogs import warno_path_dialog

SETTINGS_WARNO_PATH_KEY = "wme_warno_path"


# TODO: move warno path verification to own class

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

        w = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        w.setLayout(main_layout)

        bar = title_bar.TitleBar(parent=self)
        main_layout.addWidget(bar)
        main_layout.addWidget(main_widget.MainWidget(self.warno_path, self.settings, bar))

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

    screen = app.screens()[0]
    dpi = screen.physicalDotsPerInch()

    scale = -2
    if dpi > 100:
        scale = 2

    extra = {'density_scale': scale,
             'danger': '#dc3545',
             'warning': '#ffc107',
             'success': '#17a2b8',
             }
    apply_stylesheet(app, theme="dark_nato.xml", extra=extra)

    stylesheet = app.styleSheet()
    with open('resources/custom_style.css') as file:
        app.setStyleSheet(stylesheet + file.read().format(**os.environ))

    QtWidgets.QApplication.instance().setAttribute(QtCore.Qt.AA_DisableWindowContextHelpButton)

    app_icon = QtGui.QIcon()
    app_icon.addFile('resources/img/icon16.png', QtCore.QSize(16, 16))
    app_icon.addFile('resources/img/icon24.png', QtCore.QSize(24, 24))
    app_icon.addFile('resources/img/icon32.png', QtCore.QSize(32, 32))
    app_icon.addFile('resources/img/icon48.png', QtCore.QSize(48, 48))
    app_icon.addFile('resources/img/icon64.png', QtCore.QSize(64, 64))
    app.setWindowIcon(app_icon)

    main_window = MainWindow()
    sys.exit(app.exec_())
