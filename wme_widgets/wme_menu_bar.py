# menu bar for the title bar, includes menus and actions for mod management

import os
import logging
from pathlib import Path

from PySide2 import QtWidgets, QtCore

from dialogs import new_mod_dialog, edit_config_dialog, new_backup_dialog, \
    selection_dialog, confirmation_dialog, options_dialog
from utils import path_validator
from wme_widgets import main_widget


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

        file_menu = self.addMenu("File")

        self.add_action_to_menu("New Mod", file_menu, False, self.on_new_action)
        self.add_action_to_menu("Open Mod", file_menu, False, self.on_load_action)

        file_menu.addSeparator()

        self.add_action_to_menu("Options", file_menu, False, self.on_options_action)

        edit_menu = self.addMenu("Edit")

        self.add_action_to_menu("Generate Mod", edit_menu, True, self.on_generate_action)
        self.add_action_to_menu("Edit Mod Configuration", edit_menu, True, self.on_edit_config_action)
        self.add_action_to_menu("Update Mod", edit_menu, True, self.on_update_action)
        self.add_action_to_menu("Upload Mod", edit_menu, True, self.on_upload_action)

        edit_menu.addSeparator()

        self.add_action_to_menu("Create Mod Backup", edit_menu, True, self.on_new_backup_action)
        self.add_action_to_menu("Retrieve Mod Backup", edit_menu, True,
                                self.on_retrieve_backup_action)
        self.add_action_to_menu("Remove Mod Backup", edit_menu, True, self.on_delete_backup_action)

    def on_new_action(self):
        if not self.main_widget_ref.ask_all_tabs_to_save():
            return

        dialog = new_mod_dialog.NewModDialog(self.main_widget_ref.get_warno_path())
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            mod_name = dialog.get_mod_name()
            mods_path = self.main_widget_ref.get_warno_path() + "/Mods/"
            mods_path = mods_path.replace("/", "\\")

            if run_script(mods_path, "CreateNewMod.bat", mod_name) != 0:
                logging.error("Error while running CreateNewMod.bat")
                return

            # load mod
            self.request_load_mod.emit(mods_path + mod_name)

    def on_load_action(self):
        if not self.main_widget_ref.ask_all_tabs_to_save():
            return

        while True:
            mod_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter mod path",
                                                                    self.main_widget_ref.get_warno_path() + "/Mods")
            if mod_path == "":
                return

            mod_path = mod_path.removesuffix("/")
            if path_validator.validate_mod_path(mod_path):
                self.request_load_mod.emit(mod_path)
                return

            QtWidgets.QMessageBox().information(self, "Path invalid", "The given path does not to point to a valid "
                                                                      "WARNO mod directory. Please enter a valid path")

    def on_options_action(self):
        options_dialog.OptionsDialog().exec_()

    def generate_mod(self):
        # for whatever reason, the successful run returns 18?
        ret_code = run_script(self.main_widget_ref.get_loaded_mod_path(), "GenerateMod.bat", [])
        logging.info("GenerateMod.bat executed with return code " + str(ret_code))

    def on_generate_action(self):
        self.generate_mod()

    def on_edit_config_action(self):
        if not self.main_widget_ref.ask_all_tabs_to_save():
            return

        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      self.main_widget_ref.get_loaded_mod_name() + "\\Config.ini"

        if not QtCore.QFile.exists(config_path):
            QtWidgets.QMessageBox().information(self, "Config.ini not found", "The configuration file for the mod "
                                                + self.main_widget_ref.get_loaded_mod_name() + " could not be found."
                                                " You have to generate the mod to create the configuration file.")
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

            # change relevant directory names and update paths
            if new_name != "":
                loaded_mod_path = self.main_widget_ref.get_loaded_mod_path()
                new_mod_path = loaded_mod_path[
                               :loaded_mod_path.rindex('\\') + 1] + new_name
                old_config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                                  self.main_widget_ref.get_loaded_mod_name()
                new_config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                                  new_name
                config_path = new_config_path + "\\Config.ini"

                os.rename(loaded_mod_path, new_mod_path)
                os.rename(old_config_path, new_config_path)

                self.request_load_mod.emit(new_mod_path)

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
        result = dialog.exec_()
        if result != QtWidgets.QDialog.Accepted:
            return

        args = []
        if dialog.get_name() != "":
            args = dialog.get_name()

        self.remove_pause_line_from_script("CreateModBackup.bat")
        ret = run_script(self.main_widget_ref.get_loaded_mod_path(), "CreateModBackup.bat", args)
        logging.info("CreateModBackup.bat executed with return code " + str(ret))

    def find_backups(self):
        all_backups = []
        backup_dir = QtCore.QDir(self.main_widget_ref.get_loaded_mod_path() + "\\Backup")
        if not backup_dir.exists():
            return []

        file_filter = ["*.zip"]
        all_backups = backup_dir.entryList(file_filter)
        return all_backups

    def on_retrieve_backup_action(self):
        all_backups = self.find_backups()
        if len(all_backups) == 0:
            logging.info("No backups found")
            return

        dialog = selection_dialog.SelectionDialog("Please select a backup to retrieve.",
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
            logging.info("No backups found")
            return

        dialog = selection_dialog.SelectionDialog("Please select a backup to delete.",
                                                  "Select Backup",
                                                  all_backups)
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        selection = dialog.get_selection()

        confirm_dialog = confirmation_dialog.ConfirmationDialog("The backup " + selection +
                                                                " will be removed and you might not be able to "
                                                                "restore it! Are you sure you want to continue?",
                                                                "Warning!")
        if confirm_dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        try:
            os.remove(self.main_widget_ref.get_loaded_mod_path() + "\\Backup\\" + selection)
        except Exception as ex:
            logging.error(ex)

    def add_action_to_menu(self, name: str, menu: QtWidgets.QMenu, start_disabled=False,
                           slot=None) -> QtWidgets.QAction:
        action = QtWidgets.QAction(name)
        menu.addAction(action)
        action.triggered.connect(slot)

        if start_disabled:
            action.setDisabled(True)
            self.main_widget_ref.mod_loaded.connect(lambda: action.setDisabled(False))

        self.actions.append(action)
        return action
