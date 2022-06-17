from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt

import ndf_editor_widget, new_mod_dialog
import subprocess

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
        process.start()
        process.waitForFinished()
        return process.exitCode()
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

    def __init__(self, warno_path: str, settings: QtCore.QSettings):
        super().__init__()
        self.toolbar = QtWidgets.QToolBar()
        self.loaded_mod_path = ""
        self.warno_path = warno_path
        self.status_label = QtWidgets.QLabel()
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(lambda: self.status_label.setText(""))
        self.settings = settings
        self.setup_ui()
        MainWidget.instance = self
        last_open = self.settings.value(SETTINGS_LAST_OPEN_KEY)
        if not last_open is None:
            if validate_mod_path(str(last_open)):
                self.load_mod(last_open)

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        main_layout.addWidget(self.toolbar)

        new_action = self.toolbar.addAction("New")
        new_action.setToolTip("Create new mod (Ctrl + N)")
        new_action.setShortcut(QtGui.QKeySequence.New)
        new_action.triggered.connect(self.on_new_action)

        load_action = self.toolbar.addAction("Open")
        load_action.setToolTip("Open existing mod (Ctrl + O)")
        load_action.setShortcut(QtGui.QKeySequence.Open)
        load_action.triggered.connect(self.on_load_action)

        self.toolbar.addSeparator()

        self.add_script_action("Generate", "Generate mod", self.on_generate_action)
        self.add_script_action("Edit Configuration", "Edit mod configuration")
        self.add_script_action("Update", "Update mod")
        self.add_script_action("Upload", "Upload mod")
        self.add_script_action("Create Backup", "Create mod backup")
        self.add_script_action("Retrieve Backup", "Retrieve mod backup")
        self.add_script_action("Remove Backup", "Remove mod backup")
        self.toolbar.addSeparator()
        self.toolbar.addAction("Undo")
        self.toolbar.addAction("Redo")
        self.toolbar.addSeparator()
        self.toolbar.addAction("Options")

        tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(tab_widget)

        ndf_editor = ndf_editor_widget.NdfEditorWidget()
        tab_widget.addTab(ndf_editor, ".ndf Editor")
        cheat_sheet = QtWidgets.QWidget()
        tab_widget.addTab(cheat_sheet, "Modding Cheat Sheet")

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

            # load mod
            self.load_mod(mods_path + mod_name)

            # generation not requested
            generated = 2
            if dialog.get_mod_generate():
                if self.generate_mod():
                    # generation requested and successful
                    generated = 1
                else:
                    # generation requested but failed
                    generated = 0

            if generated == 2:
                text = "Your mod " + mod_name + " was successfully created."
            elif generated == 1:
                text = "Your mod " + mod_name + " was successfully created and generated."
            else:
                text = "Your mod " + mod_name + " was successfully created but the generation appears to have failed."

            set_status_text("Mod creation for " + mod_name + " finished.")
            QtWidgets.QMessageBox().information(self, "Mod created", text)

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
        print("loaded mod at " + mod_path)
        # TODO: set window title
        self.settings.setValue(SETTINGS_LAST_OPEN_KEY, mod_path)
        self.mod_loaded.emit(mod_path)

    def generate_mod(self):
        # for whatever reason, the successful run returns 18?
        ret_code = run_script(self.loaded_mod_path, "GenerateMod.bat", [])
        if ret_code != 18:
            print("Error while running GenerateMod.bat, returned " + str(ret_code))
            return False
        return True

    def add_script_action(self, name: str, tooltip: str, slot=None) -> QtWidgets.QAction:
        action = QtWidgets.QAction(name)
        self.toolbar.addAction(action)
        action.setToolTip(tooltip)
        action.triggered.connect(slot)

        action.setDisabled(True)
        self.mod_loaded.connect(lambda: action.setDisabled(False))

        return action

    def on_generate_action(self):
        self.generate_mod()

    def active_tab_ask_to_save(self):
        # TODO: ask the current tab if progress needs to be saved
        # TODO: open dialog to save, discard, or cancel
        # TODO: on save/discard perform action and return true
        # TODO: on cancel return false
        return True
