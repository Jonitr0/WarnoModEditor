from PySide2 import QtWidgets, QtCore

from wme_widgets.tab_pages import tab_page_base
from wme_widgets import wme_code_editor, main_widget


class FindBar(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.find_close_button = QtWidgets.QToolButton()
        self.find_next_button = QtWidgets.QToolButton()
        self.find_prev_button = QtWidgets.QToolButton()
        self.find_results_label = QtWidgets.QLabel("0 results")
        self.find_line_edit = QtWidgets.QLineEdit()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.setup_ui()

    def setup_ui(self):
        self.setLayout(self.main_layout)

        self.main_layout.addWidget(self.find_line_edit)
        self.main_layout.addWidget(self.find_results_label)
        self.find_prev_button.setText("<")
        self.main_layout.addWidget(self.find_prev_button)
        self.find_next_button.setText(">")
        self.main_layout.addWidget(self.find_next_button)
        self.find_close_button.setText("X")
        self.find_close_button.clicked.connect(self.on_close)
        self.main_layout.addWidget(self.find_close_button)

    def on_close(self):
        # TODO: remove find highlighting
        self.setHidden(True)


class NdfEditorWidget(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()

        self.find_bar = FindBar()
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
        tool_bar.addSeparator()
        find_action = tool_bar.addAction("Find")
        find_action.setShortcut("Ctrl+F")
        find_action.triggered.connect(self.on_find)

        main_layout.addWidget(self.find_bar)
        self.find_bar.setHidden(True)
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

    def on_find(self):
        self.find_bar.setHidden(False)
