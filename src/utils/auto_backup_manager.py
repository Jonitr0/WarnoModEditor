from PySide6 import QtCore

from src.utils import settings_manager


class AutoBackupManager(QtCore.QObject):
    file_system_lock = QtCore.QMutex()

    def __init__(self, parent=None):
        super().__init__(parent)

        # TODO: if default settings arent set, set them
        # TODO: run the backup creation in a thread in the background

    def on_mod_loaded(self):
        # TODO: load mod specific settings or default settings
        pass

    def on_mod_unloaded(self):
        # TODO: if time has elapsed and auto backup is set on close, backup
        pass
