from PySide2 import QtWidgets

from wme_widgets.tab_pages import tab_page_base


class NdfEditorWidget(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()

        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        tool_bar.addAction("Open")
        tool_bar.addAction("Save")
        tool_bar.addSeparator()
        tool_bar.addAction("Undo")
        tool_bar.addAction("Redo")

        text_edit = QtWidgets.QTextEdit()
        main_layout.addWidget(text_edit)
