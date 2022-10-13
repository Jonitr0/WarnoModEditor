from PySide6 import QtWidgets

from src.wme_widgets.tab_pages import tab_page_base
from src.wme_widgets import main_widget


class DiffPage(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        target_selection_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(target_selection_layout)

        # build combo box area to select comparison target
        target_info_label = QtWidgets.QLabel("Compare " +
                                             main_widget.MainWidget.instance.get_loaded_mod_name() + " with: ")
        target_info_label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        target_selection_layout.addWidget(target_info_label)
        target_combobox = QtWidgets.QComboBox()
        target_combobox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        target_combobox.setMaximumWidth(500)
        target_selection_layout.addWidget(target_combobox)
        compare_button = QtWidgets.QPushButton("Compare")
        compare_button.setFixedWidth(100)
        target_selection_layout.addWidget(compare_button)
        target_selection_layout.addStretch(0)

        results_area = QtWidgets.QScrollArea()
        main_layout.addWidget(results_area)
        results_list_widget = QtWidgets.QWidget()
        results_area.setWidget(results_list_widget)
