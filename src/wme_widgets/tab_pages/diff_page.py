from PySide6 import QtWidgets, QtCore

from src.wme_widgets.tab_pages import tab_page_base
from src.wme_widgets import main_widget

from filecmp import dircmp

import os
import shutil
import zipfile
import string
import random


class DiffPage(tab_page_base.TabPageBase):
    def __init__(self):
        super().__init__()
        self.compare_button = QtWidgets.QPushButton("Compare")
        self.target_combobox = QtWidgets.QComboBox()
        self.setup_ui()
        self.load_mods_to_combobox()

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
        self.target_combobox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.target_combobox.setMaximumWidth(500)
        target_selection_layout.addWidget(self.target_combobox)
        self.compare_button.setFixedWidth(100)
        self.compare_button.pressed.connect(self.on_compare)
        target_selection_layout.addWidget(self.compare_button)
        target_selection_layout.addStretch(0)

        results_area = QtWidgets.QScrollArea()
        main_layout.addWidget(results_area)
        results_list_widget = QtWidgets.QWidget()
        results_area.setWidget(results_list_widget)

    def load_mods_to_combobox(self):
        # get Mods dir
        mod_dir = main_widget.MainWidget.instance.get_loaded_mod_path()
        mod_dir = mod_dir[:mod_dir.rindex('\\')]

        self.target_combobox.addItem("Unmodded game files", "unmodded")
        # list of items that can't be compared with
        exclude_list = ["Utils", "ModData", main_widget.MainWidget.instance.get_loaded_mod_name()]
        dir_iter = QtCore.QDirIterator(mod_dir, (QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs))
        while dir_iter.hasNext():
            next = dir_iter.next()
            next_name = next[next.rindex('/') + 1:]
            if not exclude_list.__contains__(next_name):
                self.target_combobox.addItem(next_name, next)

    def on_compare(self):
        main_widget.MainWidget.instance.show_loading_screen("Running comparison...")
        target = self.target_combobox.currentData()
        mod_dir = main_widget.MainWidget.instance.get_loaded_mod_path()
        delete = False
        # comparison with original files
        if target == "unmodded":
            mods_base_dir = mod_dir[:mod_dir.rindex('\\')]
            target = mods_base_dir + "\\" + ''.join(random.choice(string.ascii_letters) for i in range(8))
            shutil.copytree(mods_base_dir + "\\ModData", target)
            newbase = os.path.join(mods_base_dir + "\\ModData", "base.zip")
            with zipfile.ZipFile(newbase, 'r') as archive:
                archive.extractall(target)
            delete = True
        res = dircmp(mod_dir, target)
        res_d, res_l, res_r = self.compare_subdirs(res, [], [], [])
        print(res_d)
        print(res_l)
        print(res_r)
        if delete:
            shutil.rmtree(target)
        main_widget.MainWidget.instance.hide_loading_screen()

    def compare_subdirs(self, dcmp: dircmp, diffs: list[str], left: list[str], right: list[str]):
        # TODO: add full path
        diffs += dcmp.diff_files
        left += dcmp.left_only
        right += dcmp.right_only
        for sub_dcmp in dcmp.subdirs.values():
            sub_diffs, sub_left, sub_right = self.compare_subdirs(sub_dcmp, [], [], [])
            diffs += sub_diffs
            left += sub_left
            right += sub_right
        return diffs, left, right

