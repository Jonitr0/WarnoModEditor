from PySide6 import QtCore, QtWidgets
from dialogs import warno_path_dialog
from utils import path_validator, settings_manager

dialog_finished_once = False


def validate_warno_path(warno_path):
    if path_validator.validate_warno_path(warno_path):
        settings_manager.write_settings_value(settings_manager.WARNO_PATH_KEY, warno_path)
        return True
    if dialog_finished_once:
        QtWidgets.QMessageBox().information(QtWidgets.QWidget(), "Path invalid",
                                            "The WARNO path appears to be invalid. "
                                            "Please enter the correct path.")
    return open_warno_path_dialog()


def load_warno_path_from_settings():
    tmp_path = settings_manager.get_settings_value(settings_manager.WARNO_PATH_KEY)
    if tmp_path is None:
        return open_warno_path_dialog()
    else:
        return validate_warno_path(str(tmp_path))


def open_warno_path_dialog():
    tmp_path = "C:\Program Files (x86)\Steam\steamapps\common\WARNO"
    if not QtCore.QDir(tmp_path).exists():
        tmp_path = QtCore.QDir().currentPath()

    path_dialog = warno_path_dialog.WarnoPathDialog(tmp_path)
    result = path_dialog.exec()

    if result == QtWidgets.QDialog.Accepted:
        warno_path = path_dialog.get_path()
        global dialog_finished_once
        dialog_finished_once = True
        return validate_warno_path(warno_path)
    elif result == QtWidgets.QDialog.Rejected:
        return False
