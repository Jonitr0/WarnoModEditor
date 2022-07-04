from PySide2 import QtWidgets

from wme_widgets.tab_pages import tab_page_base


class NdfEditorWidget(tab_page_base.TabPageBase):
    def __init__(self, other=None):
        super().__init__()

        self.text_edit = QtWidgets.QTextEdit()
        self.setup_ui()

        self.copy_data(other)

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        tool_bar.addAction("Open")
        tool_bar.addAction("Save")
        tool_bar.addSeparator()
        tool_bar.addAction("Undo")
        tool_bar.addAction("Redo")

        main_layout.addWidget(self.text_edit)

    def copy_data(self, other):
        if other is None:
            return

        self.text_edit.setPlainText(other.text_edit.toPlainText())
