# TabWidget that manages pages such as editors, etc.

from PySide2 import QtWidgets

from utils import icon_loader
from wme_widgets.tab_pages import ndf_editor_widget


class WMETabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.tabBar().setMinimumHeight(32)

        # TODO: style button
        new_tab_button = QtWidgets.QPushButton()
        new_tab_button.setIcon(icon_loader.load_icon("plusIcon.png"))
        new_tab_button.setMinimumHeight(20)
        self.setCornerWidget(new_tab_button)

        self.tab_menu = QtWidgets.QMenu()
        new_tab_button.setMenu(self.tab_menu)

        self.add_new_tab_action(".ndf Editor")
        self.add_new_tab_action("Cheat Sheet")

        self.setTabsClosable(True)
        self.setMovable(True)
        # TODO: run save check
        self.tabCloseRequested.connect(self.removeTab)

    def to_json(self) -> str:
        # TODO: call to_json on all pages
        pass

    def save_state(self):
        # TODO: call to_json and save to settings
        pass

    def add_new_tab_action(self, name: str):
        action = self.tab_menu.addAction(name)
        if name == ".ndf Editor":
            action.triggered.connect(lambda: self.addTab(ndf_editor_widget.NdfEditorWidget(), name))
        elif name == "Cheat Sheet":
            action.triggered.connect(lambda: self.addTab(QtWidgets.QWidget(), name))
        return action


