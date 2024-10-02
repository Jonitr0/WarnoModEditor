from PySide6 import QtWidgets, QtGui
from PySide6.QtCore import Qt

from src.wme_widgets import base_window
from src.wme_widgets.tab_widget import wme_tab_widget
from src.dialogs import essential_dialogs

detached_list = []


def clear_detached_list():
    orig_len = len(detached_list)
    for i in range(len(detached_list)):
        detached = detached_list[orig_len - i - 1]
        detached.close()


class WMEDetachedTab(base_window.BaseWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        self.bar_layout.addLayout(main_layout)
        self.tab_widget = wme_tab_widget.WMETabWidget(self)
        self.tab_widget.tab_removed_by_button.connect(self.on_tab_removed)
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        main_layout.addWidget(self.tab_widget)

        self.load_screen = QtWidgets.QLabel()
        self.load_screen.setHidden(True)
        self.load_screen.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.load_screen.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.load_screen)

        detached_list.append(self)

    def add_tab(self, widget, icon, title: str):
        self.tab_widget.addTab(widget, icon, title)

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

    def show_loading_screen(self, text: str):
        self.title_bar.close_button.setDisabled(True)
        self.load_screen.setText(text)
        self.tab_widget.setHidden(True)
        self.load_screen.setHidden(False)

    def hide_loading_screen(self):
        self.title_bar.close_button.setDisabled(False)
        self.tab_widget.setHidden(False)
        self.load_screen.setHidden(True)

