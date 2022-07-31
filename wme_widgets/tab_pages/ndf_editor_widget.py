from PySide6 import QtWidgets, QtCore, QtGui

from wme_widgets.tab_pages import tab_page_base
from wme_widgets import wme_code_editor, main_widget

from utils import icon_manager
from utils.color_manager import *


class FindBar(QtWidgets.QWidget):
    request_find_pattern = QtCore.Signal(str)
    request_find_reset = QtCore.Signal()
    request_uncheck = QtCore.Signal(bool)

    request_prev = QtCore.Signal()
    request_next = QtCore.Signal()

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
        self.main_layout.setSpacing(0)

        self.main_layout.addWidget(self.line_edit)
        self.line_edit.returnPressed.connect(self.on_search)

        self.enter_button.setIcon(icon_manager.load_icon("magnify.png", COLORS.PRIMARY))
        self.enter_button.setToolTip("Start search")
        self.enter_button.clicked.connect(self.on_search)
        self.enter_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.enter_button)

        self.main_layout.addWidget(self.results_label)
        self.results_label.setMinimumWidth(120)

        prev_icon = QtGui.QIcon()
        prev_icon.addPixmap(icon_manager.load_pixmap("arrowUp.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        prev_icon.addPixmap(icon_manager.load_pixmap("arrowUp.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.prev_button.setIcon(prev_icon)
        self.prev_button.clicked.connect(self.on_prev)
        self.prev_button.setToolTip("Previous search result")
        self.prev_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.prev_button)

        next_icon = QtGui.QIcon()
        next_icon.addPixmap(icon_manager.load_pixmap("arrowDown.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        next_icon.addPixmap(icon_manager.load_pixmap("arrowDown.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.next_button.setIcon(next_icon)
        self.next_button.clicked.connect(self.on_next)
        self.next_button.setToolTip("Next search result")
        self.next_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.next_button)

        self.enable_find_buttons(False)

        self.close_button.setIcon(icon_manager.load_icon("titlebar/close.png", COLORS.PRIMARY))
        self.close_button.clicked.connect(self.on_close)
        self.close_button.setToolTip("Close search")
        self.close_button.setFixedSize(32, 32)
        self.main_layout.addWidget(self.close_button)

    def on_search(self):
        if self.line_edit.text() == "":
            self.request_find_reset.emit()
            self.results_label.setText("")
            self.enable_find_buttons(False)
            return

        self.results_label.setText("searching...")

        QtCore.QCoreApplication.processEvents()
        self.current_search = self.line_edit.text()
        self.request_find_pattern.emit(self.current_search)

    def on_close(self):
        self.reset()
        self.request_uncheck.emit(False)

    def on_next(self):
        self.request_next.emit()

    def on_prev(self):
        self.request_prev.emit()

    def reset(self):
        self.request_find_reset.emit()
        self.line_edit.setText("")
        self.results_label.setText("")
        self.setHidden(True)
        self.enable_find_buttons(False)

    def set_label_text(self, text: str):
        self.results_label.setText(text)

    def enable_find_buttons(self, enable: bool = True):
        self.next_button.setDisabled(not enable)
        self.prev_button.setDisabled(not enable)


class NdfEditorWidget(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()

        self.file_path = ""

        self.find_bar = FindBar()
        self.code_editor = wme_code_editor.WMECodeEditor()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        open_action = tool_bar.addAction(icon_manager.load_icon("open.png", COLORS.PRIMARY), "Open (Ctrl + O)")
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.on_open)

        save_action = tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        tool_bar.addSeparator()

        undo_icon = QtGui.QIcon()
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        undo_icon.addPixmap(icon_manager.load_pixmap("undo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.undo_action = tool_bar.addAction(undo_icon, "Undo (Ctrl + Z)")
        self.undo_action.setShortcut("Ctrl+Z")
        self.undo_action.setDisabled(True)
        self.undo_action.triggered.connect(self.on_undo)

        redo_icon = QtGui.QIcon()
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        redo_icon.addPixmap(icon_manager.load_pixmap("redo.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)
        self.redo_action = tool_bar.addAction(redo_icon, "Redo (Ctrl + Y)")
        self.redo_action.setShortcut("Ctrl+Y")
        self.redo_action.setDisabled(True)
        self.redo_action.triggered.connect(self.on_redo)

        tool_bar.addSeparator()

        find_action = tool_bar.addAction(icon_manager.load_icon("magnify.png", COLORS.PRIMARY), "Find (Ctrl + F)")
        find_action.setShortcut("Ctrl+F")
        find_action.setCheckable(True)
        find_action.toggled.connect(self.on_find)

        main_layout.addWidget(self.find_bar)
        self.find_bar.setHidden(True)
        self.find_bar.request_find_pattern.connect(self.code_editor.find_pattern)
        self.find_bar.request_find_reset.connect(self.code_editor.reset_find)
        self.find_bar.request_uncheck.connect(find_action.setChecked)
        self.find_bar.request_next.connect(self.code_editor.goto_next_find)
        self.find_bar.request_prev.connect(self.code_editor.goto_prev_find)

        main_layout.addWidget(self.code_editor)
        self.code_editor.search_complete.connect(self.on_search_complete)
        self.code_editor.unsaved_changes.connect(self.set_unsaved_changes)
        self.code_editor.document().undoAvailable.connect(self.on_undo_available)
        self.code_editor.document().redoAvailable.connect(self.on_redo_available)

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
        try:
            with open(file_path, encoding="UTF-8") as f:
                self.code_editor.setPlainText(f.read())
            self.file_path = file_path
            self.unsaved_changes = False
        except Exception as e:
            logging.error("Could not open file " + file_path + ": " + str(e))
        main_widget.MainWidget.instance.hide_loading_screen()

    def save_changes(self):
        # TODO: check if other widgets have unsaved changes on the file, ask to progress
        main_widget.MainWidget.instance.show_loading_screen("saving file...")
        ret = False
        try:
            with open(self.file_path, "w", encoding="UTF-8") as f:
                f.write(self.code_editor.toPlainText())
            ret = True
        except Exception as e:
            logging.error("Could not save to file " + self.file_path + ": " + str(e))
        main_widget.MainWidget.instance.hide_loading_screen()
        if ret:
            self.unsaved_changes = False
        return ret

    def discard_changes(self):
        # TODO: there might be a better way
        self.open_file(self.file_path)

    def on_find(self, checked):
        if checked:
            self.find_bar.setHidden(False)
            self.find_bar.line_edit.setFocus()
        else:
            self.find_bar.reset()

    def on_search_complete(self):
        results = len(self.code_editor.get_find_results())
        if results == 0:
            self.find_bar.set_label_text("0 results for \"" + self.find_bar.current_search + "\"")
            self.find_bar.enable_find_buttons(False)
        else:
            self.find_bar.set_label_text(str(results) + " results for \"" + self.find_bar.current_search + "\"")
            self.find_bar.enable_find_buttons(True)

    def on_undo_available(self, available: bool):
        self.undo_action.setDisabled(not available)

    def on_redo_available(self, available: bool):
        self.redo_action.setDisabled(not available)

    def on_undo(self):
        self.code_editor.document().undo()

    def on_redo(self):
        self.code_editor.document().redo()

