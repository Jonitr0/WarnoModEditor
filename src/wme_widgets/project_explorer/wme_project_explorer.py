from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtCore import Qt

from src.utils.color_manager import *
from src.wme_widgets import wme_essentials, main_widget
from src.wme_widgets.project_explorer import file_system_treeview


class WMEProjectExplorer(QtWidgets.QWidget):
    request_open_explorer = QtCore.Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # create minimalistic search bar
        self.search_bar = wme_essentials.WMELineEdit()
        self.search_bar.setPlaceholderText("Find files...")
        main_layout.addWidget(self.search_bar)

        # file size checkbox
        file_size_label = QtWidgets.QLabel("Show file sizes: ")
        self.file_size_checkbox = QtWidgets.QCheckBox()
        check_status = settings_manager.get_settings_value(settings_manager.SHOW_EXPLORER_FILESIZE_KEY)
        if check_status is not None:
            self.file_size_checkbox.setChecked(check_status)
        else:
            self.file_size_checkbox.setChecked(False)
        file_size_layout = QtWidgets.QHBoxLayout()
        file_size_layout.addWidget(file_size_label)
        file_size_layout.addWidget(self.file_size_checkbox)
        file_size_layout.addStretch()
        main_layout.addLayout(file_size_layout)

        self.tree_view = file_system_treeview.FileSystemTreeView(self)
        main_layout.addWidget(self.tree_view)
        self.file_size_checkbox.stateChanged.connect(self.tree_view.on_show_size_changed)

        self.search_bar.textChanged.connect(self.tree_view.on_find_text_changed)

        shortcut = QtGui.QShortcut("Ctrl+Shift+F", self, self.on_focus_search)
        shortcut.setContext(Qt.ApplicationShortcut)

    def on_focus_search(self):
        self.search_bar.setFocus()
        self.request_open_explorer.emit()

    def update_model(self, mod_path: str):
        self.tree_view.update_model(mod_path)
        self.tree_view.model().loaded_all_dirs.connect(self.on_all_loaded)
        self.file_size_checkbox.stateChanged.emit(self.file_size_checkbox.checkState())

        main_widget.instance.show_loading_screen("Loading directories...")
        t = main_widget.instance.run_worker_thread(self.tree_view.model().load_all_dirs)
        main_widget.instance.wait_for_worker_thread(t)
        main_widget.instance.hide_loading_screen()

        self.search_bar.setText("")

    def on_all_loaded(self):
        logging.info("All directories loaded")



