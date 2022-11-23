# menu bar for the title bar, includes menus and actions for mod management

import os
import logging
import shutil
from pathlib import Path

from PySide6 import QtWidgets, QtCore, QtGui

from src.dialogs import new_mod_dialog, edit_config_dialog
from src.dialogs import essential_dialogs, options_dialog, new_backup_dialog
from src.utils import path_validator
from src.wme_widgets import main_widget


def run_script(cwd: str, cmd: str, args: list):
    main_widget.MainWidget.instance.show_loading_screen("running command " + cmd + "...")
    try:
        process = QtCore.QProcess()
        process.setProgram("cmd.exe")
        process.setArguments(["/C", cmd, args])
        process.setWorkingDirectory(cwd)
        logging.info("at " + cwd + " running: cmd.exe /C " + cmd + " " + str(args))

        process.start()
        process.waitForFinished()
        ret = process.exitCode()
        process.close()
        main_widget.MainWidget.instance.hide_loading_screen()
        return ret
    except Exception as ex:
        logging.error(ex)
        main_widget.MainWidget.instance.hide_loading_screen()
        return -1


class WMEMainMenuBar(QtWidgets.QMenuBar):
    request_load_mod = QtCore.Signal(str)

    def __init__(self, main_widget_ref, parent=None):
        super().__init__(parent)
        self.actions = []
        self.main_widget_ref = main_widget_ref

        self.file_menu = self.addMenu("File")
        self.file_menu.setToolTipsVisible(True)

        self.add_action_to_menu("New Mod", self.file_menu, False, self.on_new_action, "Create a new mod")
        self.add_action_to_menu("Open Mod", self.file_menu, False, self.on_load_action, "Open an existing mod")
        self.add_action_to_menu("Delete Mod", self.file_menu, False, self.on_delete_action, "Delete an existing mod")

        self.file_menu.addSeparator()

        self.add_action_to_menu("Options", self.file_menu, False, self.on_options_action, "Change WME settings")

        self.edit_menu = self.addMenu("Edit")
        self.edit_menu.setToolTipsVisible(True)

        self.add_action_to_menu("Generate Mod", self.edit_menu, True, self.on_generate_action,
                                "Generate the binary files for the mod.\n"
                                "This step is required to apply changes made to the mods files ingame")
        self.add_action_to_menu("Edit Mod Configuration", self.edit_menu, True, self.on_edit_config_action,
                                "Edit the mods Config.ini file")
        self.add_action_to_menu("Update Mod", self.edit_menu, True, self.on_update_action,
                                "Update the mod to a new version of WARNO")
        self.add_action_to_menu("Upload Mod", self.edit_menu, True, self.on_upload_action,
                                "Upload the mod to your Steam Workshop")

        self.edit_menu.addSeparator()

        self.add_action_to_menu("Create Mod Backup", self.edit_menu, True, self.on_new_backup_action,
                                "Create a backup from the current state of the mod")
        self.add_action_to_menu("Retrieve Mod Backup", self.edit_menu, True,
                                self.on_retrieve_backup_action, "Restore an existing mod backup")
        self.add_action_to_menu("Delete Mod Backup", self.edit_menu, True, self.on_delete_backup_action,
                                "Delete an existing mod backup")

    def on_new_action(self):
        dialog = new_mod_dialog.NewModDialog(self.main_widget_ref.get_warno_path())
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            if not self.main_widget_ref.ask_all_tabs_to_save():
                return

            mod_name = dialog.get_mod_name()
            mods_path = self.main_widget_ref.get_warno_path() + "/Mods/"
            mods_path = mods_path.replace("/", "\\")

            if run_script(mods_path, "CreateNewMod.bat", mod_name) != 0:
                logging.error("Error while running CreateNewMod.bat")
                return

            try:
                if os.path.exists(mods_path + mod_name + "\\.base"):
                    shutil.rmtree(mods_path + mod_name + "\\.base")
            except Exception as e:
                logging.error(e)

            # load mod
            self.request_load_mod.emit(mods_path + mod_name)

    def on_load_action(self):
        while True:
            mod_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter mod path",
                                                                    self.main_widget_ref.get_warno_path() + "/Mods",
                                                                    options=(QtWidgets.QFileDialog.ShowDirsOnly |
                                                                             QtWidgets.QFileDialog.ReadOnly))
            if mod_path == "":
                return

            mod_path = mod_path.removesuffix("/")
            mod_path = mod_path.replace("/", "\\")
            if path_validator.validate_mod_path(mod_path):
                if mod_path == main_widget.MainWidget.instance.get_loaded_mod_path():
                    return
                if not self.main_widget_ref.ask_all_tabs_to_save():
                    return
                self.request_load_mod.emit(mod_path)
                return

            essential_dialogs.MessageDialog("Path invalid", "The given path does not to point to a valid "
                                                            "WARNO mod directory. Please enter a valid path").exec()

    def on_delete_action(self):
        # let user select a mod
        while True:
            # TODO: make this actually read-only
            mod_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter mod path",
                                                                    self.main_widget_ref.get_warno_path() + "/Mods",
                                                                    options=(QtWidgets.QFileDialog.ShowDirsOnly |
                                                                             QtWidgets.QFileDialog.ReadOnly))
            if mod_path == "":
                return

            mod_path = mod_path.removesuffix("/")
            mod_path = mod_path.replace("/", "\\")
            if path_validator.validate_mod_path(mod_path):
                break

            essential_dialogs.MessageDialog("Path invalid", "The given path does not to point to a valid "
                                                            "WARNO mod directory. Please enter a valid path").exec()
        # ask to really delete
        ret = essential_dialogs.ConfirmationDialog("The selected mod including all backups in its directory"
                                                   " will be deleted. You might be unable to recover it.\n"
                                                   "Do you really want to continue?", "Warning!").exec()
        if ret != QtWidgets.QDialog.Accepted:
            return

        try:
            shutil.rmtree(mod_path)
        except Exception as e:
            logging.error(e)

        # find config dir
        mod_name = mod_path[mod_path.rindex('\\') + 1:]
        config_dir = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + mod_name

        # ask to remove config dir
        if QtCore.QDir(config_dir).exists():
            dialog = essential_dialogs.ConfirmationDialog("Delete config file and generated binaries?",
                                                          "Delete Mod", urgent=False)
            dialog.set_button_texts(ok="Yes", cancel="No")
            ret = dialog.exec()
            if ret == QtWidgets.QDialog.Accepted:
                try:
                    shutil.rmtree(config_dir)
                except Exception as e:
                    logging.error(e)

        if mod_path == self.main_widget_ref.get_loaded_mod_path():
            # disable all edit actions
            for action in self.edit_menu.actions():
                if not (action.isSeparator() or action.menu()):
                    action.setDisabled(True)
            self.main_widget_ref.unload_mod()

    def on_options_action(self):
        options_dialog.OptionsDialog().exec()

    def generate_mod(self):
        # for whatever reason, the successful run returns 18?
        ret_code = run_script(self.main_widget_ref.get_loaded_mod_path(), "GenerateMod.bat", [])
        logging.info("GenerateMod.bat executed with return code " + str(ret_code))

    def on_generate_action(self):
        # backup old config, if applicable
        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      self.main_widget_ref.get_loaded_mod_name() + "\\"
        if QtCore.QFile.exists(config_path + "Config.ini"):
            os.rename(config_path + "Config.ini", config_path + "Config_tmp.ini")
        self.generate_mod()
        # restore old config, if applicable
        if QtCore.QFile.exists(config_path + "Config_tmp.ini"):
            os.remove(config_path + "Config.ini")
            os.rename(config_path + "Config_tmp.ini", config_path + "Config.ini")

    def on_edit_config_action(self):
        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      self.main_widget_ref.get_loaded_mod_name() + "\\Config.ini"

        if not QtCore.QFile.exists(config_path):
            essential_dialogs.MessageDialog("Config.ini not found", "The configuration file for the mod "
                                            + self.main_widget_ref.get_loaded_mod_name() +
                                            " could not be found. You have to generate the mod to "
                                            "create the configuration file.").exec()
            return

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

            # replace to make the file readable for Eugen...
            with open(config_path, "r+") as f:
                f_content = f.read()
                f_content = f_content.replace("=", " = ")
                f.seek(0)
                f.write(f_content)

    def on_update_action(self):
        self.remove_pause_line_from_script("UpdateMod.bat")
        ret = run_script(self.main_widget_ref.get_loaded_mod_path(), "UpdateMod.bat", [])
        logging.info("UpdateMod.bat executed with return code " + str(ret))

    def remove_pause_line_from_script(self, script_name: str):
        file = self.main_widget_ref.get_loaded_mod_path() + "\\" + script_name
        with open(file, "r") as f:
            lines = f.readlines()
        with open(file, "w") as f:
            for line in lines:
                if line.strip("\n") != "pause":
                    f.write(line)

    def on_upload_action(self):
        ret = run_script(self.main_widget_ref.get_loaded_mod_path(), "UploadMod.bat", [])
        logging.info("UploadMod.bat executed with return code " + str(ret))

    def on_new_backup_action(self):
        dialog = new_backup_dialog.NewBackupDialog()
        result = dialog.exec()
        if result != QtWidgets.QDialog.Accepted:
            return

        args = []
        if dialog.get_name() != "":
            args = dialog.get_name()

        self.remove_pause_line_from_script("CreateModBackup.bat")
        ret = run_script(self.main_widget_ref.get_loaded_mod_path(), "CreateModBackup.bat", args)
        logging.info("CreateModBackup.bat executed with return code " + str(ret))

    def find_backups(self):
        backup_dir = QtCore.QDir(self.main_widget_ref.get_loaded_mod_path() + "\\Backup")
        if not backup_dir.exists():
            return []

        file_filter = ["*.zip"]
        all_backups = backup_dir.entryList(file_filter)
        return all_backups

    def on_retrieve_backup_action(self):
        all_backups = self.find_backups()
        if len(all_backups) == 0:
            essential_dialogs.MessageDialog("No backups found",
                                            "No backups could be found for the currently loaded mod.").exec()
            return

        dialog = essential_dialogs.SelectionDialog("Please select a backup to retrieve.",
                                                   "Select Backup",
                                                   all_backups)
        res = dialog.exec_()
        if res != QtWidgets.QDialog.Accepted:
            return

        selection = dialog.get_selection()

        self.remove_pause_line_from_script("RetrieveModBackup.bat")
        ret = run_script(self.main_widget_ref.get_loaded_mod_path(), "RetrieveModBackup.bat", selection)
        logging.info("RetrieveModBackup.bat executed with return code " + str(ret))

    def on_delete_backup_action(self):
        all_backups = self.find_backups()
        if len(all_backups) == 0:
            essential_dialogs.MessageDialog("No backups found",
                                            "No backups could be found for the currently loaded mod.").exec()
            return

        dialog = essential_dialogs.SelectionDialog("Please select a backup to delete.",
                                                   "Select Backup",
                                                   all_backups)
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        selection = dialog.get_selection()

        confirm_dialog = essential_dialogs.ConfirmationDialog("The backup " + selection +
                                                              " will be deleted and you might not be able to "
                                                              "restore it! Are you sure you want to continue?",
                                                              "Warning!")
        if confirm_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        try:
            os.remove(self.main_widget_ref.get_loaded_mod_path() + "\\Backup\\" + selection)
        except Exception as ex:
            logging.error(ex)

    def add_action_to_menu(self, name: str, menu: QtWidgets.QMenu, start_disabled=False,
                           slot=None, tooltip: str = "") -> QtGui.QAction:
        action = QtGui.QAction(name)
        menu.addAction(action)
        action.triggered.connect(slot)
        action.setToolTip(tooltip)

        if start_disabled:
            action.setDisabled(True)
            self.main_widget_ref.mod_loaded.connect(lambda: action.setDisabled(False))

        self.actions.append(action)
        return action
