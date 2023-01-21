from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets import wme_title_bar
from src.wme_widgets.tab_widget import wme_tab_widget
from src.dialogs import essential_dialogs
from src.utils import icon_manager

detached_list = []


def clear_detached_list():
    orig_len = len(detached_list)
    for i in range(len(detached_list)):
        detached = detached_list[orig_len - i - 1]
        detached.close()


class WMEDetachedTab(QtWidgets.QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.shadow_layout = QtWidgets.QHBoxLayout()
        self.shadow_effect = QtWidgets.QGraphicsDropShadowEffect()

        shadow_widget = QtWidgets.QWidget()
        self.shadow_layout.setContentsMargins(4, 4, 4, 4)
        shadow_widget.setLayout(self.shadow_layout)

        self.shadow_effect.setOffset(0, 0)
        self.shadow_effect.setBlurRadius(4)
        self.shadow_effect.setColor(QtGui.QColor(0, 0, 0, 150))
        shadow_widget.setGraphicsEffect(self.shadow_effect)

        self.setAttribute(Qt.WA_TranslucentBackground)
        shadow_widget.setAttribute(Qt.WA_TranslucentBackground)

        self.setModal(False)
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.bar_layout = QtWidgets.QVBoxLayout(self)
        self.bar_layout.setContentsMargins(0, 0, 0, 6)
        self.bar_layout.setSpacing(0)

        bar_widget = QtWidgets.QWidget()
        self.shadow_layout.addWidget(bar_widget)
        bar_widget.setLayout(self.bar_layout)

        dialog_layout = QtWidgets.QHBoxLayout()
        dialog_layout.setContentsMargins(0, 0, 0, 0)
        dialog_layout.addWidget(shadow_widget)
        self.setLayout(dialog_layout)

        self.title_bar = wme_title_bar.WMETitleBar(self)
        self.bar_layout.addWidget(self.title_bar)

        content_layout = QtWidgets.QVBoxLayout(self)
        content_layout.setContentsMargins(10, 10, 10, 10)
        self.bar_layout.addLayout(content_layout)
        self.tab_widget = wme_tab_widget.WMETabWidget(self)
        self.tab_widget.tab_removed_by_button.connect(self.on_tab_removed)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        content_layout.addWidget(self.tab_widget)

        self.load_screen = QtWidgets.QLabel()
        self.load_screen.setHidden(True)
        self.load_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.load_screen.setAlignment(Qt.AlignCenter)
        content_layout.addWidget(self.load_screen)

        self.grip = QtWidgets.QSizeGrip(self)
        self.grip.resize(16, 16)

        self.setWindowIcon(QtGui.QIcon(icon_manager.load_colored_icon("app_icon_colored")))

    def add_tab(self, widget, icon, title: str):
        self.tab_widget.addTab(widget, icon, title)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        rect = self.rect()
        self.grip.move(rect.right() - 16 - 4, rect.bottom() - 16 - 4)
        # TODO (0.1.1): add borders that allow resize, in shadow area

    def close(self):
        # close all tabs with no unsaved changes
        orig_count = self.tab_widget.count()
        for i in range(orig_count):
            page = self.tab_widget.widget(orig_count - i - 1)
            if not page.unsaved_changes:
                self.tab_widget.removeTab(orig_count - i - 1)
        # check for each unsaved tab if it should be saved
        while self.tab_widget.count() > 0:
            page = self.tab_widget.widget(0)
            dialog = essential_dialogs.AskToSaveDialog(page.tab_name)
            result = dialog.exec()

            # don't close on cancel
            if not result == QtWidgets.QDialog.Accepted:
                return
            # on save
            elif dialog.save_changes:
                if not page.save_changes():
                    return
            # on revert
            else:
                page.update_page()
            # close tab
            self.tab_widget.removeTab(0)

        # remove window from list of detached windows
        detached_list.remove(self)
        return super().close()

    def on_tab_removed(self):
        if self.tab_widget.tabBar().count() < 1:
            self.close()

    def on_tab_changed(self, index: int):
        # set Window title to current tab title
        title = self.tab_widget.tabText(index)
        self.setWindowTitle(title)

    def setWindowTitle(self, title: str):
        super().setWindowTitle(title)
        self.title_bar.set_title(title)

    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Return or key == Qt.Key_Enter:
            event.ignore()
        else:
            super().keyPressEvent(event)

    def changeEvent(self, event):
        if event.type() == QtCore.QEvent.WindowStateChange:
            if (self.windowState() == (Qt.WindowMaximized or Qt.WindowFullScreen)) or int(self.windowState()) == 6:
                self.shadow_layout.setContentsMargins(0, 0, 0, 0)
                self.shadow_effect.setEnabled(False)
            else:
                self.shadow_layout.setContentsMargins(4, 4, 4, 4)
                # stupid but needed to fix shadow effect
                self.resize(self.size().width() + 1, self.size().height() + 1)
                self.resize(self.size().width() - 1, self.size().height() - 1)
                self.shadow_effect.setEnabled(True)
        super().changeEvent(event)

    def show_loading_screen(self, text: str):
        self.load_screen.setText(text)
        self.tab_widget.setHidden(True)
        self.load_screen.setHidden(False)

    def hide_loading_screen(self):
        self.tab_widget.setHidden(False)
        self.load_screen.setHidden(True)

