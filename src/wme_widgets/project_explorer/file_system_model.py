from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

import time

# based on:
# https://stackoverflow.com/questions/63669844/pyqt5-dont-show-empty-folders-after-filtering-files-with-a-setnamefilters


class FileSystemModel(QtCore.QSortFilterProxyModel):
    name_filters = ""
    root_path = ""
    show_all_dirs = True

    def __init__(self):
        super().__init__()
        self.data_model = QtWidgets.QFileSystemModel()
        self.data_model.setFilter(
            QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs | QtCore.QDir.Files)
        self.dirs_to_load = []
        self.data_model.directoryLoaded.connect(self.on_directory_loaded)
        self.setSourceModel(self.data_model)

    def setNameFilters(self, filters):
        if not isinstance(filters, (tuple, list)):
            filters = [filters]
        self.name_filters = filters
        self.invalidateFilter()

    def hasChildren(self, parent):
        sourceParent = self.mapToSource(parent)
        # accept anything that's shorter than root path
        entry_path = QtWidgets.QFileSystemModel.filePath(self.data_model, sourceParent)
        if len(entry_path) <= len(self.root_path):
            return True
        if not self.data_model.hasChildren(sourceParent):
            return False
        qdir = QtCore.QDir(self.data_model.filePath(sourceParent))
        return bool(qdir.entryList(qdir.NoDotAndDotDot | qdir.AllEntries | qdir.AllDirs))

    def filterAcceptsRow(self, row, parent):
        source = self.data_model.index(row, 0, parent)
        # accept anything that's shorter than root path
        entry_path = QtWidgets.QFileSystemModel.filePath(self.data_model, source)
        if len(entry_path) <= len(self.root_path):
            return True
        if source.isValid():
            if self.data_model.isDir(source):
                if self.show_all_dirs:
                    return True
                qdir = QtCore.QDir(self.data_model.filePath(source))
                dir_iter = QtCore.QDirIterator(qdir.path(), self.name_filters,
                                               qdir.Files, QtCore.QDirIterator.Subdirectories)
                return dir_iter.hasNext()

            elif self.name_filters:  # file
                qdir = QtCore.QDir(self.data_model.filePath(source))
                return qdir.match(self.name_filters,
                                  self.data_model.fileName(source))
        return True

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.ToolTipRole:
            return index.data()
        else:
            return super().data(index, role)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags  # 0
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ToolTip

    def get_file_path_for_index(self, index):
        return QtWidgets.QFileSystemModel.filePath(self.data_model, self.mapToSource(index))

    def set_root_path(self, root_path: str):
        self.data_model.setRootPath(root_path)
        self.root_path = root_path

    def load_dir(self, path: str):
        index = self.data_model.index(path)
        self.data_model.fetchMore(index)
        for i in range(self.data_model.rowCount(index)):
            child_path = self.data_model.filePath(self.data_model.index(i, 0, index))
            if child_path in self.dirs_to_load or not self.data_model.isDir(self.data_model.index(i, 0, index)):
                continue
            self.dirs_to_load.append(child_path)
            self.load_dir(child_path)

    def on_directory_loaded(self, path):
        if path in self.dirs_to_load:
            self.dirs_to_load.remove(path)

            index = self.data_model.index(path)
            # add children to the list
            for i in range(self.data_model.rowCount(index)):
                child_path = self.data_model.filePath(self.data_model.index(i, 0, index))
                if child_path in self.dirs_to_load or not self.data_model.isDir(self.data_model.index(i, 0, index)):
                    continue
                self.dirs_to_load.append(child_path)
                self.load_dir(child_path)

    def load_all_dirs(self):
        self.load_dir(self.root_path)
        while len(self.dirs_to_load) > 0:
            time.sleep(0.1)
