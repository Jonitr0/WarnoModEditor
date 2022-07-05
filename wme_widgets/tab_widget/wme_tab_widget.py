# TabWidget that manages pages such as editors, etc.

from PySide2 import QtWidgets

from wme_widgets.tab_widget import wme_tab_bar
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

    def ask_all_tabs_to_save(self):
        # can be called even when close is later canceled, will be overwritten anyway
        self.save_state()
        for detached in self.tabBar().get_detached_list():
            # TODO: ask each detached to save, cancel on cancel pressed
            detached.close()
        # TODO: ask each tab to save
        return True





