# TabWidget that manages pages such as editors, etc.

from PySide2 import QtWidgets

from wme_widgets.tab_widget import wme_tab_bar, wme_detached_tab
from wme_widgets.tab_pages import ndf_editor_widget


class WMETabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # TODO: add tab context menu (close all, close all but this, close all saved)

        tab_bar = wme_tab_bar.WMETabBar(self)
        self.setTabBar(tab_bar)

        # TODO: style button
        new_tab_button = QtWidgets.QPushButton()
        new_tab_button.setText("Add Tab..")
        new_tab_button.setMinimumHeight(20)
        self.setCornerWidget(new_tab_button)

        self.tab_menu = QtWidgets.QMenu()
        new_tab_button.setMenu(self.tab_menu)

        self.add_new_tab_action(".ndf Editor")

        self.setTabsClosable(True)
        # TODO: run save check
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

    def add_new_tab_action(self, name: str):
        action = self.tab_menu.addAction(name)
        if name == ".ndf Editor":
            action.triggered.connect(self.add_ndf_editor)
        return action

    def add_ndf_editor(self):
        self.addTab(ndf_editor_widget.NdfEditorWidget(), ".ndf Editor")

    def on_tab_close_pressed(self, index: int):
        # TODO: ask to save progress
        self.removeTab(index)

    def on_open_ndf_editor(self, file_path: str):
        file_path = file_path.replace("/", "\\")
        file_name = file_path[file_path.rindex('\\') + 1:]
        editor = ndf_editor_widget.NdfEditorWidget()
        self.addTab(editor, file_name)
        editor.open_file(file_path)


    def ask_all_tabs_to_save(self, all_windows: bool = False):
        # TODO: iterate through tabs
        if not all_windows:
            return True

        while len(wme_detached_tab.detached_list) > 0:
            # TODO: ask each detached to save, break and return False on cancel pressed
            detached = wme_detached_tab.detached_list[0]
            detached.close()
        # TODO: ask each tab to save
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
