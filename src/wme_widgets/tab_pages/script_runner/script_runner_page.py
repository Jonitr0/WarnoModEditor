from PySide6 import QtWidgets

from src.wme_widgets import wme_essentials
from src.wme_widgets.tab_pages import base_tab_page
from src.utils import icon_manager
from src.utils.color_manager import *


class ScriptRunnerPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.tool_bar = QtWidgets.QToolBar()
        self.main_layout.addWidget(self.tool_bar)

        # TODO: icon
        run_action = self.tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY),
                                             "Run Selected Script (Ctrl + T)")
        run_action.setShortcut("Ctrl+T")
        run_action.triggered.connect(self.run_script)

        # define import location, automatically import from there
        script_selector = wme_essentials.WMECombobox()
        script_selector.addItems(["Script1", "Script2"])
        self.tool_bar.addWidget(script_selector)

        # TODO: action that opens import location in explorer

        self.main_layout.addStretch(1)

    def run_script(self):
        # lots of error handling, maybe backup before?
        pass