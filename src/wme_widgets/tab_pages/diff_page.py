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

        # TODO: check if this is shown
        results_area = QtWidgets.QScrollArea(self)
        results_area.setWidgetResizable(True)
        main_layout.addWidget(results_area)
        results_list_widget = QtWidgets.QWidget(self)
        results_area.setWidget(results_list_widget)
        results_list_widget.setLayout(self.results_layout)

        self.results_layout.addStretch(1)

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
        # clear results layout
        for i in reversed(range(self.results_layout.count())):
            widget_to_remove = self.results_layout.itemAt(i).widget()
            self.results_layout.removeWidget(widget_to_remove)
            if widget_to_remove:
                widget_to_remove.setParent(None)

        main_widget.MainWidget.instance.show_loading_screen("Running comparison...")

        target = self.target_combobox.currentData()
        mod_dir = main_widget.MainWidget.instance.get_loaded_mod_path()
        delete = False
        # comparison with original files
        if target == "unmodded":
            # copy and unzip mod data to randomly named dir, delete it afterwards
            mods_base_dir = mod_dir[:mod_dir.rindex('\\')]
            target = mods_base_dir + "\\" + ''.join(random.choice(string.ascii_letters) for i in range(8))
            shutil.copytree(mods_base_dir + "\\ModData", target)
            newbase = os.path.join(mods_base_dir + "\\ModData", "base.zip")
            with zipfile.ZipFile(newbase, 'r') as archive:
                archive.extractall(target)
            delete = True
        res = dircmp(mod_dir, target)
        res_d, res_l, res_r = self.compare_subdirs(res, [], [], [])
        # TODO: process results

        left_name = main_widget.MainWidget.instance.get_loaded_mod_name()
        if delete:
            right_name = "unmodded game files"
        else:
            right_name = target[target.rindex('/') + 1:]

        print(res_d)
        print(res_l)
        print(res_r)

        for diff in res_l:
            diff_w = DiffWidget(self)
            diff_w.left_only(diff, left_name)
            self.results_layout.insertWidget(self.results_layout.count()-1, diff_w)

        for diff in res_r:
            diff_w = DiffWidget(self)
            diff_w.right_only(diff, right_name)
            self.results_layout.insertWidget(self.results_layout.count()-1, diff_w)

        if delete:
            shutil.rmtree(target)

        if len(res_d) < 1 and len(res_l) < 1 and len(res_r) < 1:
            self.results_layout.insertWidget(self.results_layout.count()-1, QtWidgets.QLabel("No differences found."))

        main_widget.MainWidget.instance.hide_loading_screen()

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


class DiffWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.text_edit = QtWidgets.QTextEdit()
        self.open_in_editor_button = QtWidgets.QPushButton("Open in text editor")
        self.info_label = QtWidgets.QLabel()
        self.setup_ui()

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        info_layout = QtWidgets.QHBoxLayout()
        main_layout.addLayout(info_layout)

        info_layout.addWidget(self.info_label)
        info_layout.addStretch(1)
        info_layout.addWidget(self.open_in_editor_button)

        main_layout.addWidget(self.text_edit)

    def left_only(self, diff_name: str, left_name: str):
        self.info_label.setText(diff_name + " only exists in " + left_name)
        self.text_edit.setHidden(True)

    def right_only(self, diff_name: str, right_name: str):
        self.info_label.setText(diff_name + " only exists in " + right_name)
        self.text_edit.setHidden(True)
