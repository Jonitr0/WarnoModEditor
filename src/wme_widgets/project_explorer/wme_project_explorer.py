from PySide6 import QtWidgets

from src.utils.color_manager import *
from src.wme_widgets import wme_lineedit, main_widget
from src.wme_widgets.project_explorer import file_system_treeview


class WMEProjectExplorer(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        # create minimalistic search bar
        search_bar = wme_lineedit.WMELineEdit()
        search_bar.setPlaceholderText("Find in Directory...")
        main_layout.addWidget(search_bar)

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

        search_bar.textChanged.connect(self.tree_view.on_find_text_changed)

    def update_model(self, mod_path: str):
        self.tree_view.update_model(mod_path)
        self.file_size_checkbox.stateChanged.emit(self.file_size_checkbox.checkState())

        main_widget.MainWidget.instance.show_loading_screen("Loading file system...")

        # load file system
        for i in range(20):
            self.tree_view.expandAll()
            QtWidgets.QApplication.processEvents()

        self.tree_view.collapseAll()

        main_widget.MainWidget.instance.hide_loading_screen()



