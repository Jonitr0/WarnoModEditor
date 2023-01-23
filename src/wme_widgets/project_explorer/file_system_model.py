from PySide6 import QtWidgets, QtCore
from PySide6.QtCore import Qt


# TODO: hide empty dirs
class FileSystemModel(QtWidgets.QFileSystemModel):
    def hasChildren(self, parent) -> bool:
        # no possible children
        if parent.flags() & Qt.ItemNeverHasChildren:
            return False

        name_filters = self.nameFilters()
        # iterate through children
        file_path = QtWidgets.QFileSystemModel.filePath(self, parent)
        qdir = QtCore.QDir(file_path)
        qdir.setNameFilters(name_filters)
        dir_iter = QtCore.QDirIterator(qdir, QtCore.QDirIterator.Subdirectories)
        if dir_iter.hasNext():
            return True
        else:
            return False

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.ToolTipRole:
            return index.data()
        else:
            return super().data(index, role)

    def flags(self, index):
        if not index.isValid():
            return Qt.NoItemFlags  # 0
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ToolTip
