from PySide6 import QtCore


def validate_mod_path(mod_path):
    return QtCore.QFile().exists(mod_path + "/CreateModBackup.bat") and \
           QtCore.QFile().exists(mod_path + "/GenerateMod.bat") and \
           QtCore.QFile().exists(mod_path + "/RetrieveModBackup.bat") and \
           QtCore.QFile().exists(mod_path + "/UpdateMod.bat") and \
           QtCore.QFile().exists(mod_path + "/UploadMod.bat")


def validate_warno_path(warno_path):
    return QtCore.QFile().exists(warno_path + "/WARNO.exe") and QtCore.QDir(warno_path + "/Mods").exists()
