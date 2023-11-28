from PySide6 import QtCore


# TODO: mutex for running, lock whenever something is saved, loaded or a script is run
class AutoBackupManager(QtCore.QObject):
    file_system_lock = QtCore.QMutex()

    def __init__(self):
        super().__init__()

        # TODO: if default settings arent set, set them

    def on_mod_loaded(self):
        # TODO: load mod specific settings or default settings
        pass

    def on_mod_unloaded(self):
        # TODO: if time has elapsed and auto backup is set on close, backup
        pass
