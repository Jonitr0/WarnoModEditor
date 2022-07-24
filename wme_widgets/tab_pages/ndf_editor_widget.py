from PySide2 import QtWidgets, QtCore

from wme_widgets.tab_pages import tab_page_base
from wme_widgets import wme_code_editor, main_widget


class FindBar(QtWidgets.QWidget):
    request_find_pattern = QtCore.Signal(str)
    request_find_reset = QtCore.Signal()
    request_uncheck = QtCore.Signal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.enter_button = QtWidgets.QToolButton()
        self.close_button = QtWidgets.QToolButton()
        self.next_button = QtWidgets.QToolButton()
        self.prev_button = QtWidgets.QToolButton()
        self.results_label = QtWidgets.QLabel()
        self.line_edit = QtWidgets.QLineEdit()
        self.main_layout = QtWidgets.QHBoxLayout()
        self.current_search = ""
        self.setup_ui()

    def setup_ui(self):
        self.setLayout(self.main_layout)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

        self.main_layout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.on_search)
        self.main_layout.addWidget(self.enter_button)
        self.enter_button.setText("Go")
        self.enter_button.clicked.connect(self.on_search)
        self.main_layout.addWidget(self.results_label)
        self.results_label.setMinimumWidth(100)
        self.prev_button.setText("<")
        self.main_layout.addWidget(self.prev_button)
        self.next_button.setText(">")
        self.main_layout.addWidget(self.next_button)
        self.close_button.setText("X")
        self.close_button.clicked.connect(self.on_close)
        self.main_layout.addWidget(self.close_button)

    def on_search(self):
        if self.line_edit.text() == "":
            self.request_find_reset.emit()
            self.results_label.setText("")
            return

        self.results_label.setText("searching...")

        QtCore.QCoreApplication.processEvents()
        self.current_search = self.line_edit.text()
        self.request_find_pattern.emit(self.current_search)

    def on_close(self):
        self.reset()
        self.request_uncheck.emit(False)

    def reset(self):
        self.request_find_reset.emit()
        self.line_edit.setText("")
        self.results_label.setText("")
        self.setHidden(True)

    def set_label_text(self, text: str):
        self.results_label.setText(text)


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
        find_action.setCheckable(True)
        find_action.toggled.connect(self.on_find)

        main_layout.addWidget(self.find_bar)
        self.find_bar.setHidden(True)
        self.find_bar.request_find_pattern.connect(self.code_editor.find_pattern)
        self.find_bar.request_find_reset.connect(self.code_editor.reset_find)
        self.find_bar.request_uncheck.connect(find_action.setChecked)

        main_layout.addWidget(self.code_editor)
        self.code_editor.search_complete.connect(self.on_search_complete)

    def on_open(self):
        file_path, _ = QtWidgets.QFileDialog().getOpenFileName(self,
                                                               "Select .ndf File",
                                                               main_widget.MainWidget.instance.get_loaded_mod_path(),
                                                               "*.ndf")
        if not QtCore.QFile.exists(file_path):
            return
        self.open_file(file_path)

    def open_file(self, file_path):
        main_widget.MainWidget.instance.show_loading_screen("opening file...")
        with open(file_path, encoding="UTF-8") as f:
            self.code_editor.setPlainText(f.read())
        main_widget.MainWidget.instance.hide_loading_screen()

    def on_find(self, checked):
        if checked:
            self.find_bar.setHidden(False)
            self.find_bar.line_edit.setFocus()
        else:
            self.find_bar.reset()

    def on_search_complete(self):
        results = len(self.code_editor.get_find_results())
        if results == 0:
            self.find_bar.set_label_text("0 results")
        else:
            self.find_bar.set_label_text(str(results) + " results for \"" + self.find_bar.current_search + "\"")
