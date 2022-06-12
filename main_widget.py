from PySide2 import QtWidgets, QtCore, QtGui
from PySide2.QtCore import Qt

import ndf_editor_widget, new_mod_dialog
import subprocess


# TODO: incorporate Eugen's scripts (CreateMod, GenerateMod, UpdateMod, UploadMod, BackupMod, RemoveBackup)
# TODO: find mods in dir, switch between mods, remember last worked on


def set_status_text(text):
    MainWidget.instance.status_set_text.emit(text)


def get_warno_path():
    return MainWidget.instance.warno_path

def run_script(cwd, cmd, args: list):
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


class MainWidget(QtWidgets.QWidget):
    status_set_text = QtCore.Signal(str)
    status_clear_text = QtCore.Signal()
    instance = None

    def __init__(self, warno_path):
        super().__init__()
        self.warno_path = warno_path
        self.status_label = QtWidgets.QLabel()
        self.status_timer = QtCore.QTimer()
        self.status_timer.timeout.connect(lambda: self.status_label.setText(""))
        self.setup_ui()
        MainWidget.instance = self

    def setup_ui(self):
        main_layout = QtWidgets.QVBoxLayout()
        self.setLayout(main_layout)

        tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(tool_bar)

        new_action = tool_bar.addAction("New")
        new_action.setToolTip("Create a new mod (Ctrl + N)")
        new_action.setShortcut(QtGui.QKeySequence.New)
        new_action.triggered.connect(self.on_new_action)

        tool_bar.addAction("Load")
        tool_bar.addAction("Load recent")
        tool_bar.addSeparator()
        tool_bar.addAction("Generate")
        tool_bar.addAction("Update")
        tool_bar.addAction("Upload")
        tool_bar.addAction("Backup")
        tool_bar.addAction("Remove Backup")
        tool_bar.addSeparator()
        tool_bar.addAction("Undo")
        tool_bar.addAction("Redo")
        tool_bar.addSeparator()
        tool_bar.addAction("Options")

        tab_widget = QtWidgets.QTabWidget()
        main_layout.addWidget(tab_widget)

        ndf_editor = ndf_editor_widget.NdfEditorWidget()
        tab_widget.addTab(ndf_editor, ".ndf Editor")
        cheat_sheet = QtWidgets.QWidget()
        tab_widget.addTab(cheat_sheet, "Modding Cheat Sheet")

        main_layout.addWidget(self.status_label)
        main_layout.setAlignment(self.status_label, Qt.AlignRight)

        self.status_set_text.connect(self.on_status_set_text)

    def on_status_set_text(self, text):
        self.status_label.setText(text)
        self.status_timer.setInterval(5000)
        self.status_timer.start()

    def on_new_action(self):
        dialog = new_mod_dialog.NewModDialog(self.warno_path)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            mod_name = dialog.get_mod_name()
            mods_path = self.warno_path + "/Mods/"
            mods_path = mods_path.replace("/", "\\")

            if run_script(mods_path, "CreateNewMod.bat", mod_name) != 0:
                print("Error while running CreateNewMod.bat")

            # TODO: generate if needed
            # TODO: load mod, send signal to UI

