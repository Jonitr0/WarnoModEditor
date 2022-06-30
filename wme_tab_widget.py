# TabWidget that manages pages such as editors, etc.

from PySide2 import QtWidgets

from utils import icon_loader
import ndf_editor_widget


class WMETabWidget(QtWidgets.QTabWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        ndf_editor = ndf_editor_widget.NdfEditorWidget()
        self.addTab(ndf_editor, ".ndf Editor")
        cheat_sheet = QtWidgets.QWidget()
        self.addTab(cheat_sheet, "Modding Cheat Sheet")

        # TODO: add menu to select new tabs
        # TODO: style button
        new_tab_button = QtWidgets.QPushButton()
        new_tab_button.setIcon(icon_loader.load_icon("plusIcon.png"))
        self.setCornerWidget(new_tab_button)

        self.tab_menu = QtWidgets.QMenu()
        self.tab_menu.addAction(".ndf Editor")
        self.tab_menu.addAction("Cheatsheet")
        new_tab_button.setMenu(self.tab_menu)

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


