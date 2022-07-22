from PySide2 import QtWidgets, QtCore
from PySide2.QtCore import Qt


class WMEProjectExplorer(QtWidgets.QTreeView):
    open_ndf_editor = QtCore.Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.doubleClicked.connect(self.on_double_click)
        self.setHeaderHidden(True)
        self.setSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Expanding)
        self.setMinimumWidth(160)

    def update_model(self, mod_path: str):
        data_model = QtWidgets.QFileSystemModel()
        data_model.setRootPath(mod_path)
        data_model.setNameFilters(["*.ndf"])
        data_model.setNameFilterDisables(False)

        self.setModel(data_model)
        self.setRootIndex(data_model.index(mod_path))

        self.hideColumn(1)
        self.hideColumn(2)
        self.hideColumn(3)

    def on_double_click(self, index):
        file_path = QtWidgets.QFileSystemModel.filePath(self.model(), index)
        if file_path.endswith(".ndf"):
            self.open_ndf_editor.emit(file_path)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.LeftButton:
            super().mouseDoubleClickEvent(event)

