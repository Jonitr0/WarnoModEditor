from PySide2 import QtWidgets, QtCore


class TabPageBase(QtWidgets.QWidget):
    unsaved_status_change = QtCore.Signal(bool, QtWidgets.QWidget)

    def __init__(self):
        super().__init__()

        self._unsaved_changes = False
        self.tab_name = ""

    @property
    def unsaved_changes(self) -> bool:
        return self._unsaved_changes

    @unsaved_changes.setter
    def unsaved_changes(self, value: bool):
        if self._unsaved_changes != value:
            self.unsaved_status_change.emit(value, self)
        self._unsaved_changes = value

    # slot for unsaved changes
    def set_unsaved_changes(self, value: bool):
        self.unsaved_changes = value

    # write changes to file
    def save_changes(self):
        pass

    # restore widget to match file status
    def discard_changes(self):
        pass

    def on_close(self):
        # TODO: ask if changes should be saved
        pass

    def to_json(self) -> str:
        # TODO: return status as JSON string
        pass
