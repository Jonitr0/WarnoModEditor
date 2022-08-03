from PySide6 import QtWidgets, QtCore

pages_for_file = {}


class TabPageBase(QtWidgets.QWidget):
    unsaved_status_change = QtCore.Signal(bool, QtWidgets.QWidget)

    def __init__(self):
        super().__init__()

        self._unsaved_changes = False
        self.tab_name = ""
        self.file_path = ""

    @property
    def unsaved_changes(self) -> bool:
        return self._unsaved_changes

    @unsaved_changes.setter
    def unsaved_changes(self, value: bool):
        if self._unsaved_changes != value:
            self.unsaved_status_change.emit(value, self)
            global pages_for_file
            # changed to true
            if value:
                page_list = pages_for_file.get(self.file_path, [])
                page_list.append(self)
                pages_for_file[self.file_path] = page_list
            # changed to false
            else:
                page_list = pages_for_file.get(self.file_path, [])
                if page_list.__contains__(self):
                    page_list.remove(self)
                pages_for_file[self.file_path] = page_list

        self._unsaved_changes = value

    # slot for unsaved changes
    def set_unsaved_changes(self, value: bool):
        self.unsaved_changes = value

    # write changes to file. Return True on success
    def save_changes(self) -> bool:
        pass

    # restore widget to match file status
    def discard_changes(self):
        pass

    # make sure self.file_path is set and add page to a watch list
    def open_file(self, file_path):
        self.file_path = file_path
        self.unsaved_changes = False
        pass

    def to_json(self) -> str:
        # TODO: return status as JSON string
        pass
