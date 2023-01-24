from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt

# based on: https://stackoverflow.com/questions/63669844/pyqt5-dont-show-empty-folders-after-filtering-files-with-a-setnamefilters

# TODO: hide empty dirs
class FileSystemModel(QtCore.QSortFilterProxyModel):
    name_filters = ''

    def __init__(self):
        super().__init__()
        self.data_model = QtWidgets.QFileSystemModel()
        self.data_model.setFilter(
            QtCore.QDir.NoDotAndDotDot | QtCore.QDir.AllDirs | QtCore.QDir.Files)
        self.setSourceModel(self.data_model)

    def setNameFilters(self, filters):
        if not isinstance(filters, (tuple, list)):
            filters = [filters]
        self.name_filters = filters
        self.invalidateFilter()

    def hasChildren(self, parent):
        sourceParent = self.mapToSource(parent)
        if not self.data_model.hasChildren(sourceParent):
            return False
        qdir = QtCore.QDir(self.data_model.filePath(sourceParent))
        return bool(qdir.entryList(qdir.NoDotAndDotDot | qdir.AllEntries | qdir.AllDirs))

    def filterAcceptsRow(self, row, parent):
        # TODO: accept anything that's shorter than root path
        source = self.data_model.index(row, 0, parent)
        if source.isValid():
            if self.data_model.isDir(source):
                qdir = QtCore.QDir(self.data_model.filePath(source))
                if self.name_filters:
                    qdir.setNameFilters(self.name_filters)
                # TODO: entry list needs to get dirs removed
                print(QtWidgets.QFileSystemModel.filePath(self.data_model, source))
                print(qdir.entryList(qdir.NoDotAndDotDot | qdir.AllEntries | qdir.AllDirs))
                return bool(qdir.entryList(qdir.NoDotAndDotDot | qdir.AllEntries | qdir.AllDirs))

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
