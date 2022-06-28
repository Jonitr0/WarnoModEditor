from PySide2 import QtWidgets


class TabPageBase(QtWidgets.QWidget):
    def __init__(self, tab: QtWidgets.QWidget):
        self.tab = tab
        super().__init__()

    def has_unsaved_changes(self) -> bool:
        pass

    # write changes to file
    def save_changes(self):
        pass

    # restore widget to match file status
    def discard_changes(self):
        pass

    def on_close(self):
        # TODO: ask if changes should be saved
        pass
