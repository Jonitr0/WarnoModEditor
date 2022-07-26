from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

from wme_widgets import wme_title_bar, main_widget
from utils import warno_path_loader, settings_manager


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.shadow_layout = QtWidgets.QHBoxLayout()
        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()
        self.main_widget_ref = None
        QtCore.QTimer.singleShot(0, self.start_main_window)

    # open actual main window
    def start_main_window(self):
        if not warno_path_loader.load_warno_path_from_settings():
            QtCore.QCoreApplication.quit()

        warno_path = settings_manager.get_settings_value(settings_manager.WARNO_PATH_KEY)
        self.resize(1152, 648)
        self.setWindowTitle("WARNO Mod Editor")

        shadow_widget = QtWidgets.QWidget()
        self.shadow_layout.setMargin(4)
        shadow_widget.setLayout(self.shadow_layout)

        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setBlurRadius(4)
        self.shadow_effect.setColor(Qt.black)
        shadow_widget.setGraphicsEffect(self.shadow_effect)

        self.setAttribute(Qt.WA_TranslucentBackground)
        shadow_widget.setAttribute(Qt.WA_TranslucentBackground)

        w = QtWidgets.QWidget()
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setMargin(0)
        main_layout.setSpacing(0)
        w.setLayout(main_layout)
        self.shadow_layout.addWidget(w)

        bar = wme_title_bar.WMETitleBar(parent=self)
        main_layout.addWidget(bar)
        self.main_widget_ref = main_widget.MainWidget(warno_path, bar)
        main_layout.addWidget(self.main_widget_ref)

        self.setCentralWidget(shadow_widget)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(16, 16)

        self.showNormal()

    def resizeEvent(self, event):
        QtWidgets.QMainWindow.resizeEvent(self, event)
        rect = self.rect()
        self.grip.move(rect.right() - 16 - 6, rect.bottom() - 16 - 6)

    def close(self):
        if self.main_widget_ref is None:
            super().close()
        if self.main_widget_ref.ask_all_tabs_to_save():
            super().close()

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if (self.windowState() == (Qt.WindowMaximized or Qt.WindowFullScreen)) or int(self.windowState()) == 6:
                self.shadow_layout.setMargin(0)
                self.shadow_effect.setEnabled(False)
            else:
                self.shadow_layout.setMargin(4)
                # stupid but needed to fix shadow effect
                self.resize(self.size().width() + 1, self.size().height() + 1)
                self.resize(self.size().width() - 1, self.size().height() - 1)
                self.shadow_effect.setEnabled(True)
        super().changeEvent(event)
