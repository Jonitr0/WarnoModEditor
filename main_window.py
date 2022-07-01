from PySide2 import QtWidgets, QtCore

from wme_widgets import wme_title_bar, main_widget
from utils import warno_path_loader, settings_manager


# TODO: move warno path verification to own class

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.main_widget_ref = None
        QtCore.QTimer.singleShot(0, self.start_main_window)

    # open actual main window
    def start_main_window(self):
        if not warno_path_loader.load_warno_path_from_settings():
            QtCore.QCoreApplication.quit()

        warno_path = settings_manager.get_settings_value(settings_manager.WARNO_PATH_KEY)
        self.resize(1152, 648)
        self.setWindowTitle("WARNO Mod Editor")

        w = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        w.setLayout(main_layout)

        bar = wme_title_bar.WMETitleBar(parent=self)
        main_layout.addWidget(bar)
        self.main_widget_ref = main_widget.MainWidget(warno_path, bar)
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

    def close(self):
        if self.main_widget_ref is None:
            super().close()
        if self.main_widget_ref.ask_all_tabs_to_save():
            super().close()
