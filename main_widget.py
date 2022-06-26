import os
from pathlib import Path

from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt

import icon_loader
import ndf_editor_widget
from dialogs import new_mod_dialog, edit_config_dialog, new_backup_dialog

# TODO: incorporate Eugen's scripts (CreateMod, GenerateMod, UpdateMod, UploadMod, BackupMod, RemoveBackup)
# TODO: find mods in dir, switch between mods, remember last worked on

SETTINGS_LAST_OPEN_KEY = "wme_last_open"


def set_status_text(text: str):
    MainWidget.instance.status_set_text.emit(text)


def get_warno_path():
    return MainWidget.instance.warno_path


def run_script(cwd: str, cmd: str, args: list):
    try:
        process = QtCore.QProcess()
        process.setProgram("cmd.exe")
        process.setArguments(["/C", cmd, args])
        process.setWorkingDirectory(cwd)
        print("at " + cwd + " running: cmd.exe /C " + cmd + " " + str(args))

        process.start()
        process.waitForFinished()
        ret = process.exitCode()
        process.close()
        return ret
    except Exception as ex:
        print(ex)
        return -1


def validate_mod_path(mod_path):
    return QtCore.QFile().exists(mod_path + "/CreateModBackup.bat") and \
           QtCore.QFile().exists(mod_path + "/GenerateMod.bat") and \
           QtCore.QFile().exists(mod_path + "/RetrieveModBackup.bat") and \
           QtCore.QFile().exists(mod_path + "/UpdateMod.bat") and \
           QtCore.QFile().exists(mod_path + "/UploadMod.bat")


class MainWidget(QtWidgets.QWidget):
    status_set_text = QtCore.Signal(str)
    mod_loaded = QtCore.Signal(str)
    instance = None

    def __init__(self, warno_path: str, settings: QtCore.QSettings, title_bar):
        super().__init__()
        self.menu_bar = QtWidgets.QMenuBar()
        self.loaded_mod_path = ""
        self.loaded_mod_name = ""
        self.warno_path = warno_path
        self.status_label = QtWidgets.QLabel()
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(lambda: self.status_label.setText(""))
        self.settings = settings
        self.title_bar = title_bar
        self.title_label = QtWidgets.QLabel()
        self.setup_ui()
        MainWidget.instance = self
        last_open = self.settings.value(SETTINGS_LAST_OPEN_KEY)
        if not last_open is None:
            if validate_mod_path(str(last_open)):
                self.load_mod(str(last_open))

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        self.setLayout(main_layout)

        self.title_label.setObjectName("title")
        self.title_bar.add_widget(self.title_label)
        self.title_bar.add_spacing(10)
        self.title_bar.add_widget(self.menu_bar)

        file_menu = self.menu_bar.addMenu("File")

        self.new_action = self.add_action_to_menu("New Mod", file_menu, False, self.on_new_action)
        self.load_action = self.add_action_to_menu("Open Mod", file_menu, False, self.on_load_action)

        edit_menu = self.menu_bar.addMenu("Edit")

        self.add_action_to_menu("Generate Mod", edit_menu, True, self.on_generate_action)
        self.add_action_to_menu("Edit Mod Configuration", edit_menu, True, self.on_edit_config_action)
        self.add_action_to_menu("Update Mod", edit_menu, True, self.on_update_action)
        self.add_action_to_menu("Upload Mod", edit_menu, True, self.on_upload_action)

        edit_menu.addSeparator()

        self.add_action_to_menu("Create Mod Backup", edit_menu, True, self.on_new_backup_action)
        self.add_action_to_menu("Retrieve Mod Backup", edit_menu, True, self.on_retrieve_backup_action)
        self.add_action_to_menu("Remove Mod Backup", edit_menu, True)

        self.menu_bar.addAction("Options")

        tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(tab_widget)

        ndf_editor = ndf_editor_widget.NdfEditorWidget()
        tab_widget.addTab(ndf_editor, ".ndf Editor")
        cheat_sheet = QtWidgets.QWidget()
        tab_widget.addTab(cheat_sheet, "Modding Cheat Sheet")

        # TODO: add menu to select new tabs
        # TODO: style button
        new_tab_button = QtWidgets.QToolButton()
        new_tab_button.setIcon(icon_loader.load_icon("plusIcon.png"))
        new_tab_button.setFixedSize(36, 36)
        tab_widget.setCornerWidget(new_tab_button)

        tab_widget.setTabsClosable(True)
        tab_widget.setMovable(True)
        # TODO: run save check
        tab_widget.tabCloseRequested.connect(tab_widget.removeTab)

        main_layout.addWidget(self.status_label)
        main_layout.setAlignment(self.status_label, Qt.AlignRight)

        self.status_set_text.connect(self.on_status_set_text)

    def on_status_set_text(self, text: str):
        self.status_label.setText(text)
        self.status_timer.setInterval(5000)
        self.status_timer.start()

    def on_new_action(self):
        if not self.active_tab_ask_to_save():
            return

        dialog = new_mod_dialog.NewModDialog(self.warno_path)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            mod_name = dialog.get_mod_name()
            mods_path = self.warno_path + "/Mods/"
            mods_path = mods_path.replace("/", "\\")

            if run_script(mods_path, "CreateNewMod.bat", mod_name) != 0:
                print("Error while running CreateNewMod.bat")
                return

            # remove all pause lines from .bat files
            pause_files = ["CreateModBackup.bat", "RetrieveModBackup.bat", "UpdateMod.bat"]
            for file in pause_files:
                file = mods_path + mod_name + "\\" + file
                print(file)
                with open(file, "r") as f:
                    lines = f.readlines()
                with open(file, "w") as f:
                    for line in lines:
                        if line.strip("\n") != "pause":
                            f.write(line)

            # load mod
            self.load_mod(mods_path + mod_name)

            if dialog.get_mod_generate():
                self.generate_mod()

            set_status_text("Mod creation for " + mod_name + " finished.")

    def on_load_action(self):
        if not self.active_tab_ask_to_save():
            return

        while True:
            mod_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter mod path", self.warno_path + "/Mods")
            if mod_path == "":
                return

            mod_path = mod_path.removesuffix("/")
            if validate_mod_path(mod_path):
                self.load_mod(mod_path)
                return

            QtWidgets.QMessageBox().information(self, "Path invalid", "The given path does not to point to a valid "
                                                                      "WARNO mod directory. Please enter a valid path")

    def load_mod(self, mod_path: str):
        self.loaded_mod_path = mod_path
        self.loaded_mod_name = mod_path[mod_path.rindex('\\') + 1:]
        print("loaded mod " + self.loaded_mod_name + " at " + mod_path)
        self.title_label.setText(self.loaded_mod_name)
        self.settings.setValue(SETTINGS_LAST_OPEN_KEY, mod_path)
        self.mod_loaded.emit(mod_path)

    def generate_mod(self):
        # for whatever reason, the successful run returns 18?
        ret_code = run_script(self.loaded_mod_path, "GenerateMod.bat", [])
        print("GenerateMod.bat executed with return code " + str(ret_code))

    def on_generate_action(self):
        self.generate_mod()

    def on_edit_config_action(self):
        if not self.active_tab_ask_to_save():
            return

        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      self.loaded_mod_name + "\\Config.ini"
        config = QtCore.QSettings(config_path, QtCore.QSettings.IniFormat)
        config_values = {}
        for key in config.allKeys():
            config_values[key] = config.value(key)
        dialog = edit_config_dialog.WarnoPathDialog(config_values)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            config_values = dialog.get_config_values()

            new_name = ""

            for key in config.allKeys():
                if key == "Properties/Name" and config_values[key] != config.value(key):
                    new_name = config_values[key]
                config.setValue(key, config_values[key])

            # delete QSettings object so file can be edited
            del config

            # change relevant directory names and update paths
            if new_name != "":
                new_mod_path = self.loaded_mod_path[:self.loaded_mod_path.rindex('\\') + 1] + new_name
                old_config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                                  self.loaded_mod_name
                new_config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                                  new_name
                config_path = new_config_path + "\\Config.ini"

                os.rename(self.loaded_mod_path, new_mod_path)
                os.rename(old_config_path, new_config_path)

                self.load_mod(new_mod_path)

            # replace to make the file readable for Eugen...
            with open(config_path, "r+") as f:
                f_content = f.read()
                f_content = f_content.replace("=", " = ")
                f.seek(0)
                f.write(f_content)

    # TODO: run as python or remove pause
    def on_update_action(self):
        ret = run_script(self.loaded_mod_path, "UpdateMod.bat", [])
        print("UpdateMod.bat executed with return code " + str(ret))

    def on_upload_action(self):
        ret = run_script(self.loaded_mod_path, "UploadMod.bat", [])
        print("UploadMod.bat executed with return code " + str(ret))

    # TODO: run as python or remove pause
    def on_new_backup_action(self):
        dialog = new_backup_dialog.NewBackupDialog()
        result = dialog.exec_()
        if result != QtWidgets.QDialog.Accepted:
            return

        args = []
        if dialog.get_name() != "":
            args = dialog.get_name()

        ret = run_script(self.loaded_mod_path, "CreateModBackup.bat", args)
        print("CreateModBackup.bat executed with return code " + str(ret))

    def find_backups(self):
        backup_dir = QtCore.QDir(self.loaded_mod_path + "\\Backup")
        if not backup_dir.exists():
            return []

        filter = [".zip"]
        all_backups = backup_dir.entryList(filter)
        print(all_backups)

    # TODO: run as python or remove pause
    def on_retrieve_backup_action(self):
        self.find_backups()

    def add_action_to_menu(self, name: str, menu: QtWidgets.QMenu, start_disabled=False,
                           slot=None) -> QtWidgets.QAction:
        action = QtWidgets.QAction(name)
        menu.addAction(action)
        action.triggered.connect(slot)

        if start_disabled:
            action.setDisabled(True)
            self.mod_loaded.connect(lambda: action.setDisabled(False))

        return action

    def active_tab_ask_to_save(self):
        # TODO: ask the current tab if progress needs to be saved
        # TODO: open dialog to save, discard, or cancel
        # TODO: on save/discard perform action and return true
        # TODO: on cancel return false
        return True
