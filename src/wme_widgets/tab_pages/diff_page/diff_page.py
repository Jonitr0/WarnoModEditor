from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

from src.wme_widgets.tab_pages.diff_page import diff_widget
from src.wme_widgets.tab_pages import tab_page_base
from src.wme_widgets import main_widget
from src.dialogs import essential_dialogs

from filecmp import dircmp

import os
import shutil
import zipfile
import string
import random
import logging


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
        self.compare_button.clicked.connect(self.on_compare)
        target_selection_layout.addWidget(self.compare_button)
        target_selection_layout.addStretch(0)

        results_area = QtWidgets.QScrollArea(self)
        results_area.setWidgetResizable(True)
        main_layout.addWidget(results_area)
        results_list_widget = QtWidgets.QWidget(self)
        results_area.setWidget(results_list_widget)
        results_list_widget.setLayout(self.results_layout)

        self.results_layout.setAlignment(Qt.AlignTop)
        self.results_layout.setSpacing(0)

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

    # TODO: split this in smaller functions
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

        main_widget.MainWidget.instance.show_loading_screen("Running comparison...")

        mod_dir = main_widget.MainWidget.instance.get_loaded_mod_path()
        delete = False
        # comparison with original files
        if target == "unmodded":
            target = self.create_tmp_mod()
            delete = True

        res = dircmp(mod_dir, target)
        res_d, res_l, res_r = self.compare_subdirs(res, [], [], [])

        left_name = main_widget.MainWidget.instance.get_loaded_mod_name()
        if delete:
            right_name = "unmodded game files"
        else:
            right_name = target[target.rindex('/') + 1:]

        for diff_file in res_l:
            diff_w = diff_widget.DiffWidget(self)
            diff_w.request_open_in_text_editor.connect(self.on_request_open_file_at_line)
            diff_w.left_only(diff_file, left_name)
            self.results_layout.addWidget(diff_w)

        for diff_file in res_r:
            diff_w = diff_widget.DiffWidget(self)
            diff_w.request_open_in_text_editor.connect(self.on_request_open_file_at_line)
            diff_w.right_only(diff_file, right_name)
            self.results_layout.addWidget(diff_w)

        for diff_file in res_d:
            changed_lines, left_lines, right_lines = self.compare_files(diff_file, mod_dir, target)
            if len(changed_lines) == 0:
                continue

            # TODO: connect signal so text editor is opened
            diff_w = diff_widget.DiffWidget(self)
            diff_w.request_open_in_text_editor.connect(self.on_request_open_file_at_line)
            diff_w.changed_text_file(diff_file, changed_lines, left_lines, right_lines)
            self.results_layout.addWidget(diff_w)

        if delete:
            try:
                shutil.rmtree(target)
            except Exception as e:
                logging.error(e)

        if len(res_d) < 1 and len(res_l) < 1 and len(res_r) < 1:
            self.results_layout.insertWidget(self.results_layout.count() - 1, QtWidgets.QLabel("No differences found."))

        main_widget.MainWidget.instance.hide_loading_screen()

    # copy and unzip mod data to randomly named dir, delete it afterwards
    def create_tmp_mod(self):
        mod_dir = main_widget.MainWidget.instance.get_loaded_mod_path()
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

    def compare_files(self, diff_file: str, mod_dir: str, target: str):
        if not diff_file.endswith(".ndf"):
            return [], [], []

        path1 = str(mod_dir + "\\" + diff_file).replace("/", "\\")
        path2 = str(target + "\\" + diff_file).replace("/", "\\")

        changed_lines = []
        lines1 = []
        lines2 = []
        with open(path1, 'r') as file1, open(path2, 'r') as file2:
            lines1 = file1.readlines()
            lines2 = file2.readlines()

            line_count = min(len(lines1), len(lines2))
            for i in range(line_count):
                if lines1[i] != lines2[i]:
                    changed_lines.append(i)

        return changed_lines, lines1, lines2

    def on_request_open_file_at_line(self, path: str, line: int):
        print(path)
        print(line)