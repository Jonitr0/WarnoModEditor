from PySide2 import QtWidgets


class TabPageBase(QtWidgets.QWidget):
    def __init__(self, tab: QtWidgets.QWidget):
        self.tab = tab
        super().__init__()

    def has_unsaved_changes(self) -> bool:
        pass

    def on_close(self):
        # TODO: ask if changes should be saved
        pass
