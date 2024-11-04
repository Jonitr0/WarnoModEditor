import os
import logging

from PySide6 import QtCore


class AssetStringManager:
    def __init__(self, main_widget):
        self.asset_strings = {}
        self.main_widget = main_widget
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.load_strings_from_csv)

    def load_asset_strings(self):
        self.asset_strings = {}

        mod_path = self.main_widget.get_loaded_mod_path()
        mod_name = self.main_widget.get_loaded_mod_name()
        csv_path = os.path.join(mod_path, "GameData", "Localisation", mod_name)

        for file in os.listdir(csv_path):
            if file.endswith(".csv"):
                file_path = os.path.join(csv_path, file)
                self.watcher.addPath(file_path)
                self.load_strings_from_csv(file_path)

    def load_strings_from_csv(self, file_path: str):
        file_name = os.path.basename(file_path)
        if not os.path.exists(file_path):
            return
        self.asset_strings[file_name] = {}
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            keys = []
            for i, line in enumerate(lines):
                if i == 0:
                    continue
                parts = line.split(";")
                key = parts[0]
                if key in keys:
                    logging.warning(f"Duplicate key {key} in {file_name}!")
                keys.append(key)
                value = parts[1]
                value = value.replace("\n", "")
                self.asset_strings[file_name][key] = value

    def get_string(self, file: str, token: str):
        return self.asset_strings.get(file, {}).get(token, None)

    def remove_string_from_file(self, file: str, token: str):
        mod_path = self.main_widget.get_loaded_mod_path()
        mod_name = self.main_widget.get_loaded_mod_name()
        file_path = os.path.join(mod_path, "GameData", "Localisation", mod_name, file)

        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        with open(file_path, "w", encoding="utf-8") as f:
            for line in lines:
                if not line.startswith(token + ";"):
                    f.write(line)

    def add_string_to_file(self, file: str, token: str, value: str):
        self.remove_string_from_file(file, token)

        mod_path = self.main_widget.get_loaded_mod_path()
        mod_name = self.main_widget.get_loaded_mod_name()
        file_path = os.path.join(mod_path, "GameData", "Localisation", mod_name, file)

        with open(file_path, "r+", encoding="utf-8") as f:
            # add newline if file does not end on one
            if not f.read().endswith("\n"):
                f.write("\n")
            f.write(f"{token};{value}\n")
