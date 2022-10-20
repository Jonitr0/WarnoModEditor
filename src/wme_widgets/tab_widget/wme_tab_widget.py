# TabWidget that manages pages such as editors, etc.

from PySide6 import QtWidgets, QtCore

from src.wme_widgets.tab_widget import wme_detached_tab, wme_tab_bar
from src.wme_widgets.tab_pages import tab_page_base, diff_page
from src.wme_widgets.tab_pages.text_editor_page import ndf_editor_page
from src.dialogs import essential_dialogs


class WMETabWidget(QtWidgets.QTabWidget):
    tab_removed_by_button = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)

        tab_bar = wme_tab_bar.WMETabBar(self)
        self.setTabBar(tab_bar)

        # TODO: style button
        new_tab_button = QtWidgets.QPushButton()
        new_tab_button.setText("Add Tab..")
        new_tab_button.setMinimumHeight(32)
        self.setCornerWidget(new_tab_button)

        self.tab_menu = QtWidgets.QMenu()
        self.tab_menu.setToolTipsVisible(True)
        new_tab_button.setMenu(self.tab_menu)
        diff_page_action = self.tab_menu.addAction("Comparison Tool")
        diff_page_action.setToolTip("Show differences between a mod and the game files or another mod.")
        diff_page_action.triggered.connect(self.on_diff_page_action)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.on_tab_close_pressed)
        self.setAcceptDrops(True)

        # make sure explorer isn't so big
        self.resize(1000, self.height())

    def to_json(self) -> str:
        # TODO: call to_json on all pages
        pass

    def save_state(self):
        # TODO: call to_json and save to settings
        pass

    def on_tab_close_pressed(self, index: int):
        page = self.widget(index)
        if page.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog(page.tab_name)
            result = dialog.exec()

            # don't close on cancel
            if not result == QtWidgets.QDialog.Accepted:
                return
            # on save
            elif dialog.save_changes:
                if not page.save_changes():
                    return

        self.removeTab(index)
        self.tab_removed_by_button.emit()

    def on_open_ndf_editor(self, file_path: str):
        file_path = file_path.replace("/", "\\")
        file_name = file_path[file_path.rindex('\\') + 1:]
        editor = ndf_editor_page.NdfEditorPage()
        self.addTab(editor, file_name)
        editor.open_file(file_path)
        editor.unsaved_changes = False

    def addTab(self, widget, title: str) -> int:
        ret = super().addTab(widget, title)
        widget.tab_name = title
        self.setCurrentIndex(ret)
        self.setTabToolTip(ret, title)
        widget.unsaved_status_change.connect(self.on_save_status_changed)
        tab_page_base.all_pages.add(widget)
        return ret

    def insertTab(self, index: int, widget, title: str) -> int:
        ret = super().insertTab(index, widget, title)
        widget.tab_name = title
        self.setCurrentIndex(ret)
        self.setTabToolTip(ret, title)
        widget.unsaved_status_change.connect(self.on_save_status_changed)
        tab_page_base.all_pages.add(widget)
        return ret

    def removeTab(self, index: int):
        widget = self.widget(index)
        tab_page_base.all_pages.remove(widget)
        super().removeTab(index)

    def ask_all_tabs_to_save(self, all_windows: bool = False) -> bool:
        # close all tabs with no unsaved changes
        i = 0
        while i < self.count():
            page = self.widget(i)
            if not page.unsaved_changes:
                self.removeTab(i)
                i -= 1
            i += 1

        # iterate through own tabs with unsaved changes
        i = 0
        while i < self.count():
            page = self.widget(i)
            dialog = essential_dialogs.AskToSaveDialog(page.tab_name)
            result = dialog.exec()

            # don't close on cancel
            if not result == QtWidgets.QDialog.Accepted:
                return False
            # on save
            elif dialog.save_changes:
                if not page.save_changes():
                    return False
            # on discard, remove tab
            else:
                self.removeTab(i)
                i -= 1
            i += 1

        if all_windows:
            # call function on other windows
            for detached in wme_detached_tab.detached_list:
                if not detached.tab_widget.ask_all_tabs_to_save(False):
                    return False

        # if cancel is never pressed, return True
        return True

    def close_all(self, all_windows: bool = False):
        self.clear()
        if all_windows:
            for detached in wme_detached_tab.detached_list:
                detached.tab_widget.clear()
                detached.close()

    def dragEnterEvent(self, event):
        mime_data = event.mimeData()
        event.accept()
        if mime_data.property('tab_bar') is not None and mime_data.property('index') is not None:
            wme_tab_bar.drop_bar = self.tabBar()
        super().dragEnterEvent(event)

    def dragLeaveEvent(self, event):
        event.accept()
        wme_tab_bar.drop_bar = None
        super().dragLeaveEvent(event)

    def on_save_status_changed(self, status: bool, widget: QtWidgets.QWidget):
        index = self.indexOf(widget)
        # if it has unsaved changes
        if status:
            self.setTabText(index, widget.tab_name + "(*)")
            self.setTabToolTip(index, widget.tab_name + "(*)")
        else:
            self.setTabText(index, widget.tab_name)
            self.setTabToolTip(index, widget.tab_name)

    def on_diff_page_action(self, _):
        diff_page_widget = diff_page.DiffPage()
        self.addTab(diff_page_widget, "Comparison Tool")
