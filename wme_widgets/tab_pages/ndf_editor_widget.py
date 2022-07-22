from PySide2 import QtWidgets, QtCore

from wme_widgets.tab_pages import tab_page_base
from wme_widgets import wme_code_editor, main_widget


class NdfEditorWidget(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()

        self.code_editor = wme_code_editor.WMECodeEditor()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        open_action = tool_bar.addAction("Open")
        open_action.triggered.connect(self.on_open)
        tool_bar.addAction("Save")
        tool_bar.addSeparator()
        tool_bar.addAction("Undo")
        tool_bar.addAction("Redo")

        main_layout.addWidget(self.code_editor)

    def on_open(self):
        file_path, _ = QtWidgets.QFileDialog().getOpenFileName(self,
                                                               "Select .ndf File",
                                                               main_widget.MainWidget.instance.get_loaded_mod_path(),
                                                               "*.ndf")
        if not QtCore.QFile.exists(file_path):
            return
        self.open_file(file_path)

    def open_file(self, file_path):
        with open(file_path, encoding="UTF-8") as f:
            self.code_editor.setPlainText(f.read())
