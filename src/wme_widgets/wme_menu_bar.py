# menu bar for the title bar, includes menus and actions for mod management

import os
import logging
import shutil
from pathlib import Path

from PySide6 import QtWidgets, QtCore, QtGui
from PySide6.QtCore import Qt

from src.dialogs import new_mod_dialog, essential_dialogs, options_dialog, new_backup_dialog, auto_backup_dialog
from src.utils import path_validator, settings_manager
from src.wme_widgets import main_widget


class WMEMainMenuBar(QtWidgets.QMenuBar):
    request_load_mod = QtCore.Signal(str)
    request_quickstart = QtCore.Signal()

    def __init__(self, main_widget_ref, parent=None):
        super().__init__(parent)
        self.actions = []
        self.main_widget_ref = main_widget_ref

        self.file_menu = self.addMenu("&File")
        self.file_menu.setToolTipsVisible(True)

        self.add_action_to_menu("New Mod", self.file_menu, False, self.on_new_action, "Create a new mod.", "Ctrl+Alt+N")
        self.add_action_to_menu("Open Mod", self.file_menu, False, self.on_load_action,
                                "Open an existing mod.", "Ctrl+Alt+O")
        self.add_action_to_menu("Delete Mod", self.file_menu, False, self.on_delete_action,
                                "Delete an existing mod.", "Ctrl+Del")

        self.file_menu.addSeparator()

        self.add_action_to_menu("Options", self.file_menu, False, self.on_options_action,
                                "Change WME settings.", "Ctrl+Alt+S")
        self.add_action_to_menu("Report Issue..", self.file_menu, False, self.on_report_issue_action,
                                "Report an issue on the WME GitHub page (opened in web browser).")
        self.add_action_to_menu("Exit", self.file_menu, False, self.on_exit_action, "Quit WME.", "Alt+X")

        self.edit_menu = self.addMenu("&Edit")
        self.edit_menu.setToolTipsVisible(True)

        self.add_action_to_menu("Generate Mod", self.edit_menu, True, self.on_generate_action,
                                "Generate the binary files for the mod. Launches another application.\n"
                                "This step is required to apply changes made to the mods files in-game.", "Alt+G")
        self.add_action_to_menu("Update Mod", self.edit_menu, True, self.on_update_action,
                                "Update the mod to a new version of WARNO.")
        self.add_action_to_menu("Upload Mod", self.edit_menu, True, self.on_upload_action,
                                "Upload the mod to your Steam Workshop.\n"
                                "Will only work if the mod was generated before.")

        self.edit_menu.addSeparator()

        self.add_action_to_menu("Edit Mod Configuration", self.edit_menu, True, self.on_edit_config_action,
                                "Edit the mods Config.ini file.", "Ctrl+Alt+C")
        self.add_action_to_menu("Delete Mod Configuration", self.edit_menu, True, self.on_delete_config_action,
                                "Delete the mods Config.ini file.")

        self.backup_menu = self.addMenu("&Backup")
        self.backup_menu.setToolTipsVisible(True)

        self.add_action_to_menu("Create Mod Backup", self.backup_menu, True, self.on_new_backup_action,
                                "Create a backup from the current state of the mod.")
        self.add_action_to_menu("Create Quick Mod Backup", self.backup_menu, True, self.on_quick_backup_action,
                                "Create a backup from the current state of the mod using the default name.",
                                "Ctrl+Alt+B")
        self.add_action_to_menu("Retrieve Mod Backup", self.backup_menu, True,
                                self.on_retrieve_backup_action, "Restore an existing mod backup.", "Ctrl+Alt+R")
        self.add_action_to_menu("Delete Mod Backup", self.backup_menu, True, self.on_delete_backup_action,
                                "Delete an existing mod backup.")
        self.add_action_to_menu("Auto Backup Settings", self.backup_menu, True, self.on_auto_backup_action,
                                "Change the auto backup settings for the current mod.")

    def on_new_action(self):
        dialog = new_mod_dialog.NewModDialog(self.main_widget_ref.get_warno_path())
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            if not self.main_widget_ref.ask_all_tabs_to_save():
                return

            mod_name = dialog.get_mod_name()
            mods_path = self.main_widget_ref.get_warno_path() + "/Mods/"
            mods_path = mods_path.replace("/", "\\")

            if self.run_script(mods_path, "CreateNewMod.bat", mod_name) != 0:
                logging.error("Error while running CreateNewMod.bat")
                return

            try:
                if os.path.exists(mods_path + mod_name + "\\.base"):
                    shutil.rmtree(mods_path + mod_name + "\\.base")
            except Exception as e:
                logging.error(e)

            # load mod
            self.request_load_mod.emit(mods_path + mod_name)
            # open quickstart guide
            self.request_quickstart.emit()

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
                if mod_path == main_widget.instance.get_loaded_mod_path():
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
            mod_path = QtWidgets.QFileDialog().getExistingDirectory(self, "Enter path of mod to delete",
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
        mod_name = mod_path[mod_path.rindex("\\") + 1:]
        ret = essential_dialogs.ConfirmationDialog(mod_name + " including all backups in its directory"
                                                              " will be deleted. You might be unable to recover it.\n"
                                                              "Do you really want to continue?", "Warning!").exec()
        if ret != QtWidgets.QDialog.Accepted:
            return

        if mod_path == self.main_widget_ref.get_loaded_mod_path():
            self.main_widget_ref.unload_mod()

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

        # delete mod from config
        app_state = settings_manager.get_settings_value(settings_manager.APP_STATE)
        if app_state:
            app_state[mod_name] = {}
            settings_manager.write_settings_value(settings_manager.APP_STATE, app_state)

    def on_options_action(self):
        options_dialog.OptionsDialog().exec()

    def on_report_issue_action(self):
        QtGui.QDesktopServices.openUrl("https://github.com/Jonitr0/WarnoModEditor/issues")

    def on_exit_action(self):
        self.window().close()

    def generate_mod(self):
        # for whatever reason, the successful run returns 18?
        self.remove_pause_line_from_script("GenerateMod.bat")
        ret_code = self.run_script(self.main_widget_ref.get_loaded_mod_path(), "GenerateMod.bat", [])
        logging.info("GenerateMod.bat executed with return code " + str(ret_code))

    def on_generate_action(self):
        # TODO: ask to save changes
        # backup old config, if applicable
        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      self.main_widget_ref.get_loaded_mod_name() + "\\"
        if QtCore.QFile.exists(config_path + "Config.ini"):
            os.rename(config_path + "Config.ini", config_path + "Config_tmp.ini")
        self.generate_mod()
        # restore old config, if applicable
        if QtCore.QFile.exists(config_path + "Config_tmp.ini"):
            if QtCore.QFile.exists(config_path + "Config.ini"):
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

        self.main_widget_ref.tab_widget.on_mod_config()

    def on_delete_config_action(self):
        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      self.main_widget_ref.get_loaded_mod_name() + "\\Config.ini"

        if not os.path.exists(config_path):
            essential_dialogs.MessageDialog("Config.ini not found", "The configuration file for the mod "
                                            + self.main_widget_ref.get_loaded_mod_name() +
                                            " could not be found. You have to generate the mod to "
                                            "create the configuration file.").exec()
        else:
            confirm_dialog = essential_dialogs.ConfirmationDialog("The configuration file and all changes you made to "
                                                                  "it will be deleted. Are you sure you want to "
                                                                  "continue?", "Warning!")
            if confirm_dialog.exec_() != QtWidgets.QDialog.Accepted:
                return

            try:
                os.remove(config_path)
            except Exception as e:
                logging.error("Error while deleting config file: " + str(e))

    def on_update_action(self):
        self.remove_pause_line_from_script("UpdateMod.bat")
        ret = self.run_script(self.main_widget_ref.get_loaded_mod_path(), "UpdateMod.bat", [])
        logging.info("UpdateMod.bat executed with return code " + str(ret))

        try:
            if os.path.exists(self.main_widget_ref.get_loaded_mod_path() + "\\.base"):
                shutil.rmtree(self.main_widget_ref.get_loaded_mod_path() + "\\.base")
        except Exception as e:
            logging.error(e)
        settings_manager.write_settings_value(settings_manager.MOD_STATE_CHANGED_KEY, 1)

    def remove_pause_line_from_script(self, script_name: str):
        file = self.main_widget_ref.get_loaded_mod_path() + "\\" + script_name

        with open(file, "r") as f:
            lines = f.readlines()
        with open(file, "w") as f:
            for line in lines:
                if not line.__contains__("pause") and not line.__contains__("PAUSE"):
                    f.write(line)

    def on_upload_action(self):
        config_path = str(Path.home()) + "\\Saved Games\\EugenSystems\\WARNO\\mod\\" + \
                      main_widget.instance.get_loaded_mod_name() + "\\Config.ini"

        if not QtCore.QFile.exists(config_path):
            essential_dialogs.MessageDialog("Config.ini not found", "The config.ini file for the mod does not seem "
                                                                    "to exist. Generate the mod (Alt + G) to create "
                                                                    "the configuration file.").exec()
            return

        with open(config_path, "r+") as f:
            f_content = f.read()
            orig_content = f_content
            f_content = f_content.replace("\\n", "")
            f.seek(0)
            f.write(f_content)

        ret = self.run_script(self.main_widget_ref.get_loaded_mod_path(), "UploadMod.bat", [])
        logging.info("UploadMod.bat executed with return code " + str(ret))

        with open(config_path, "w") as f:
            f.write(orig_content)

    def on_new_backup_action(self):
        dialog = new_backup_dialog.NewBackupDialog()
        result = dialog.exec()
        if result != QtWidgets.QDialog.Accepted:
            return

        args = []
        if dialog.get_name() != "":
            args = dialog.get_name()

        self.remove_pause_line_from_script("CreateModBackup.bat")
        ret = self.run_script(self.main_widget_ref.get_loaded_mod_path(), "CreateModBackup.bat", args)
        logging.info("CreateModBackup.bat executed with return code " + str(ret))

    def on_quick_backup_action(self):
        self.remove_pause_line_from_script("CreateModBackup.bat")
        ret = self.run_script(self.main_widget_ref.get_loaded_mod_path(), "CreateModBackup.bat", [])
        logging.info("CreateModBackup.bat executed with return code " + str(ret))

    def create_named_backup(self, name: str):
        self.remove_pause_line_from_script("CreateModBackup.bat")
        ret = self.run_script(self.main_widget_ref.get_loaded_mod_path(), "CreateModBackup.bat", name)
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

        self.retrieve_backup(selection)

    def retrieve_backup(self, backup_name: str):
        dialog = essential_dialogs.ConfirmationDialog("All changes on the current mod will be lost. Are you sure you "
                                                      "want to continue?", "Warning!")
        if dialog.exec_() != QtWidgets.QDialog.Accepted:
            return

        self.remove_pause_line_from_script("RetrieveModBackup.bat")
        ret = self.run_script(self.main_widget_ref.get_loaded_mod_path(), "RetrieveModBackup.bat", backup_name)
        logging.info("RetrieveModBackup.bat executed with return code " + str(ret))

        self.request_load_mod.emit(self.main_widget_ref.get_loaded_mod_path())

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

    def on_auto_backup_action(self):
        dialog = auto_backup_dialog.AutoBackupDialog()
        dialog.exec()

    def add_action_to_menu(self, name: str, menu: QtWidgets.QMenu, start_disabled=False,
                           slot=None, tooltip: str = "", shortcut: str = "") -> QtGui.QAction:
        action = QtGui.QAction(name)
        menu.addAction(action)
        action.triggered.connect(slot)
        action.setToolTip(tooltip)
        action.setShortcut(shortcut)
        action.setShortcutContext(Qt.ApplicationShortcut)

        if start_disabled:
            action.setDisabled(True)
            self.main_widget_ref.mod_loaded.connect(lambda: action.setDisabled(False))
            self.main_widget_ref.mod_unloaded.connect(lambda: action.setDisabled(True))

        self.actions.append(action)
        return action

    def run_script(self, cwd: str, cmd: str, args: list):
        main_widget.instance.show_loading_screen("Running command " + cmd + "...")
        t = main_widget.instance.run_worker_thread(self.run_script_task, cwd, cmd, args)
        main_widget.instance.wait_for_worker_thread(t)

    def run_script_task(self, cwd: str, cmd: str, args: list):
        try:
            self.process = QtCore.QProcess()
            self.process.setProgram("cmd.exe")
            self.process.setArguments(["/C", cmd, args])
            self.process.setWorkingDirectory(cwd)
            logging.info("at " + cwd + " running: cmd.exe /C " + cmd + " " + str(args))

            self.process.readyReadStandardOutput.connect(self.print_process_output)
            self.process.readyReadStandardError.connect(self.print_porcess_error)

            self.process.start()
            if not self.process.waitForFinished(60000):
                logging.warning("Process did not finish in time (60 secs).")
            ret = self.process.exitCode()
            self.process.close()
            main_widget.instance.hide_loading_screen()
            return ret
        except Exception as ex:
            logging.error(ex)
            main_widget.instance.hide_loading_screen()
            return -1

    def print_process_output(self):
        logging.info("Process output: " + str(self.process.readAllStandardOutput()))

    def print_porcess_error(self):
        logging.warning("Possible process error: " + str(self.process.readAllStandardError()))
