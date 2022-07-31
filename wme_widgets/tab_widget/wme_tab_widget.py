# TabWidget that manages pages such as editors, etc.

from PySide6 import QtWidgets, QtCore

from wme_widgets.tab_widget import wme_tab_bar, wme_detached_tab
from wme_widgets.tab_pages import ndf_editor_widget
from dialogs import essential_dialogs


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
        new_tab_button.setMenu(self.tab_menu)
        self.tab_menu.addAction("bla")

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
        editor = ndf_editor_widget.NdfEditorWidget()
        self.addTab(editor, file_name)
        editor.open_file(file_path)
        editor.unsaved_status_change.connect(self.on_save_status_changed)
        editor.unsaved_changes = False

    def addTab(self, widget, title: str) -> int:
        ret = super().addTab(widget, title)
        widget.tab_name = title
        self.setCurrentIndex(ret)
        self.setTabToolTip(ret, title)
        widget.unsaved_status_change.connect(self.on_save_status_changed)
        return ret

    def insertTab(self, index: int, widget, title: str) -> int:
        ret = super().insertTab(index, widget, title)
        self.setCurrentIndex(ret)
        self.setTabToolTip(ret, title)
        return ret

    def ask_all_tabs_to_save(self, all_windows: bool = False) -> bool:
        # iterate through own tabs
        for i in range(self.count()):
            page = self.widget(i)
            if page.unsaved_changes:
                dialog = essential_dialogs.AskToSaveDialog(page.tab_name)
                result = dialog.exec()

                # don't close on cancel
                if not result == QtWidgets.QDialog.Accepted:
                    return False
                # on save
                elif dialog.save_changes:
                    if not page.save_changes():
                        return False
                # on discard
                else:
                    page.discard_changes()

        if all_windows:
            # call function on other windows
            for detached in wme_detached_tab.detached_list:
                if not detached.tab_widget.ask_all_tabs_to_save(False):
                    return False

        # if cancel is never pressed, return True
        return True

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

