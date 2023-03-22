from PySide6 import QtWidgets, QtCore
from src.dialogs import essential_dialogs, rich_text_dialog

import json

# key: file_path, value: reference to page
# stores references to all pages that have unsaved changes on a file
pages_for_file = {}

# managed by tab_widget, contains all pages across all tab_widgets
all_pages = set()


def get_pages_for_file(file_path: str, unsaved_only: bool = True):
    page_list = []
    for page in all_pages:
        if page.file_path == file_path and (not unsaved_only or page.unsaved_changes):
            page_list.append(page)

    return page_list


class BaseTabPage(QtWidgets.QWidget):
    unsaved_status_change = QtCore.Signal(bool, QtWidgets.QWidget)

    def __init__(self):
        super().__init__()

        self._unsaved_changes = False
        self.tab_name = ""
        self.file_path = ""
        self.help_file_path = ""
        self.help_page = None

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
        # if more than one page has unsaved changes
        page_list = get_pages_for_file(self.file_path, unsaved_only=True)
        if len(page_list) > 1:
            file_name = self.file_path[self.file_path.rindex('\\') + 1:]
            dialog = essential_dialogs.ConfirmationDialog("Multiple tabs have unsaved changes on " + file_name +
                                                          ". If you save on this tab, changes on other tabs will "
                                                          "be discarded. Continue?", "Warning!")
            res = dialog.exec()
            if res == QtWidgets.QDialog.Rejected:
                return False

        if not self.save_changes_overwrite():
            return False

        # restore changes for other pages after successful save
        page_list = get_pages_for_file(self.file_path, unsaved_only=False)
        for page in page_list:
            if page != self:
                page.update_page()

        return True

    # called by actual save_changes function, should be overwritten in child class
    def save_changes_overwrite(self) -> bool:
        pass

    # restore widget to match file status
    def update_page(self):
        pass

    # make sure self.file_path is set and add page to a watch list
    def open_file(self, file_path):
        self.file_path = file_path
        self.unsaved_changes = False
        pass

    def to_json(self) -> dict:
        # TODO (0.1.1): return status as JSON string
        pass

    def on_help(self):
        if self.help_page:
            self.help_page.deleteLater()
        self.help_page = rich_text_dialog.RichTextDialog(self.help_file_path, "Help")
        self.help_page.show()

