import os

from PySide6 import QtCore

from src.wme_widgets import main_widget


class AssetIconManager:
    def __init__(self):
        self.icons = []
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.directoryChanged.connect(self.load_asset_icons)

    def load_asset_icons(self):
        self.icons.clear()
        self.watcher.removePaths(self.watcher.directories())
        mod_path = main_widget.instance.get_loaded_mod_path()
        # find all png files in the mod directory and its subdirectories
        for root, dirs, files in os.walk(mod_path):
            for file in files:
                if file.endswith(".png"):
                    file_path = os.path.join(root, file)
                    self.icons.append(file_path)
            for d in dirs:
                self.watcher.addPath(os.path.join(main_widget.instance.get_loaded_mod_path(), d))

    def add_icon(self, icon_path):
        self.icons.append(icon_path)
