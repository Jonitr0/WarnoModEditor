from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages.diff_page import diff_widget, file_comparison_page
from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import main_widget
from src.dialogs import essential_dialogs

from filecmp import dircmp

import os
import shutil
import zipfile
import string
import random
import logging


class DiffPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()
        self.results_layout = QtWidgets.QVBoxLayout()
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
                                             main_widget.instance.get_loaded_mod_name() + " with: ")
        target_info_label.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        target_selection_layout.addWidget(target_info_label)
        self.target_combobox.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.target_combobox.setMaximumWidth(500)
        target_selection_layout.addWidget(self.target_combobox)
        self.compare_button.setFixedWidth(100)
        self.compare_button.clicked.connect(self.on_compare)
        target_selection_layout.addWidget(self.compare_button)
        target_selection_layout.addStretch(0)

        self.results_layout.setAlignment(Qt.AlignTop)
        self.results_layout.setSpacing(0)

        results_list_widget = QtWidgets.QWidget(self)
        results_list_widget.setLayout(self.results_layout)

        results_area = QtWidgets.QScrollArea(self)
        results_area.setWidgetResizable(True)
        results_area.setWidget(results_list_widget)
        main_layout.addWidget(results_area)

        # TODO: create and fill this file
        self.help_file_path = "Help_DiffPage.html"

    def load_mods_to_combobox(self):
        # get Mods dir
        mod_dir = main_widget.instance.get_loaded_mod_path()
        mod_dir = mod_dir[:mod_dir.rindex('\\')]

        self.target_combobox.addItem("Unmodded game files", "unmodded")
        # list of items that can't be compared with
        exclude_list = ["Utils", "ModData", main_widget.instance.get_loaded_mod_name()]
        dir_iter = QtCore.QDirIterator(mod_dir, (QtCore.QDir.NoDotAndDotDot | QtCore.QDir.Dirs))
        while dir_iter.hasNext():
            next = dir_iter.next()
            next_name = next[next.rindex('/') + 1:]
            if not exclude_list.__contains__(next_name):
                self.target_combobox.addItem(next_name, next)

    def on_compare(self):
        # clear results layout
        for i in reversed(range(self.results_layout.count())):
            widget_to_remove = self.results_layout.itemAt(i).widget()
            self.results_layout.removeWidget(widget_to_remove)
            if widget_to_remove:
                widget_to_remove.setParent(None)

        target = self.target_combobox.currentData()
        if target != "unmodded" and not os.path.exists(target):
            essential_dialogs.MessageDialog("Error!", "Mod " +
                                            self.target_combobox.currentText() + " not found!").show()
            return

        main_widget.instance.show_loading_screen("Running comparison...")

        mod_dir = main_widget.instance.get_loaded_mod_path()
        delete = False
        # comparison with original files
        if target == "unmodded":
            target = self.create_tmp_mod()
            delete = True

        res = dircmp(mod_dir, target)
        res_d, res_l, res_r = self.compare_subdirs(res, [], [], [])

        left_name = main_widget.instance.get_loaded_mod_name()
        if delete:
            right_name = "unmodded game files"
        else:
            right_name = target[target.rindex('/') + 1:]

        # TODO: separate, collapsible layouts
        if len(res_l) > 0:
            self.results_layout.addWidget(QtWidgets.QLabel(left_name + " only:"))
        for diff_file in res_l:
            self.add_diff_widget(diff_file, mod_dir, None, left_name, right_name)

        if len(res_r) > 0:
            self.results_layout.addWidget(QtWidgets.QLabel(right_name + " only:"))
        for diff_file in res_r:
            self.add_diff_widget(diff_file, None, target, left_name, right_name)

        if len(res_d) > 0:
            self.results_layout.addWidget(QtWidgets.QLabel("Different files:"))
        for diff_file in res_d:
            self.add_diff_widget(diff_file, mod_dir, target, left_name, right_name)

        if delete:
            try:
                shutil.rmtree(target)
            except Exception as e:
                logging.error(e)

        if len(res_d) < 1 and len(res_l) < 1 and len(res_r) < 1:
            self.results_layout.insertWidget(self.results_layout.count() - 1, QtWidgets.QLabel("No differences found."))

        main_widget.instance.hide_loading_screen()

    def add_diff_widget(self, file_name: str, left_mod_path: str = None, right_mod_path: str = None,
                        left_mod_name: str = None, right_mod_name: str = None):
        left_text = None
        right_text = None
        file_type = diff_widget.FILE_TYPE.OTHER

        if left_mod_path is not None:
            left_text = ""
            full_path = os.path.join(left_mod_path, file_name)
            # if left is text file, read it
            if os.path.isfile(full_path) and full_path.endswith(".ndf"):
                file_type = diff_widget.FILE_TYPE.TEXT
                with open(full_path, "r", encoding="utf-8") as f:
                    left_text = f.read()
            elif os.path.isdir(full_path):
                file_type = diff_widget.FILE_TYPE.DIR

        if right_mod_path is not None:
            right_text = ""
            full_path = os.path.join(right_mod_path, file_name)
            # if right is text file, read it
            if os.path.isfile(full_path) and full_path.endswith(".ndf"):
                file_type = diff_widget.FILE_TYPE.TEXT
                with open(full_path, "r", encoding="utf-8") as f:
                    right_text = f.read()
            elif os.path.isdir(full_path):
                file_type = diff_widget.FILE_TYPE.DIR

        widget = diff_widget.DiffWidget(file_name, left_text, right_text,
                                        left_mod_name, right_mod_name, file_type, self)
        widget.open_in_text_editor.connect(self.get_current_tab_widget().on_open_ndf_editor)
        widget.open_comparison_page.connect(self.get_current_tab_widget().on_open_comparison)
        self.results_layout.addWidget(widget)

    # copy and unzip mod data to randomly named dir, delete it afterwards
    def create_tmp_mod(self):
        main_widget.instance.show_loading_screen("Creating temporary mod...")
        mod_dir = main_widget.instance.get_loaded_mod_path()
        mods_base_dir = mod_dir[:mod_dir.rindex('\\')]
        target = mods_base_dir + "\\" + ''.join(random.choice(string.ascii_letters) for i in range(8))
        shutil.copytree(mods_base_dir + "\\ModData", target)
        new_base = os.path.join(mods_base_dir + "\\ModData", "base.zip")

        with zipfile.ZipFile(new_base, 'r') as archive:
            archive.extractall(target)
        try:
            shutil.rmtree(os.path.join(target, ".base"))
        except Exception as e:
            logging.error(e)

        main_widget.instance.show_loading_screen("Running comparison...")
        return target

    def compare_subdirs(self, dcmp: dircmp, diffs: list[str], left: list[str], right: list[str], path=""):
        # add full path to diffs and left/right
        diffs_new = dcmp.diff_files
        diffs_new = [path + i for i in diffs_new]
        diffs += diffs_new

        left_new = dcmp.left_only
        left_new = [path + i for i in left_new]
        left += left_new

        right_new = dcmp.right_only
        right_new = [path + i for i in right_new]
        right += right_new

        for subdir in dcmp.subdirs:
            sub_diffs, sub_left, sub_right = self.compare_subdirs(dcmp.subdirs[subdir], [], [], [], path + subdir + "/")
            diffs += sub_diffs
            left += sub_left
            right += sub_right

        return diffs, left, right
