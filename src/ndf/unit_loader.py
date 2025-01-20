# TODO: when unit editor exists, make a unit browser for main widget
import os
import time
import threading
import multiprocessing

import ndf_parse as ndf

from PySide6 import QtCore

from src.ndf import parser_utils, ndf_scanner


class UnitLoader(QtCore.QObject):
    request_update_progress = QtCore.Signal(float, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # update when mod is loaded
        self.mod_path = ""
        # TODO: cache this in a file
        self.units = []
        self.worker = None
        self.progress_queue = None
        self.results_queue = None
        self.terminate_updater = False
        self.updater = None
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.load_units)

    def update_progress(self):
        progress = 0
        text = "Loading units..."
        while progress < 1 and self.terminate_updater is False:
            while not self.progress_queue.empty():
                progress, text = self.progress_queue.get(block=False)
            self.request_update_progress.emit(progress, text)
            time.sleep(0.01)
            QtCore.QCoreApplication.processEvents()
        self.request_update_progress.emit(1, "")
        while not self.results_queue.empty():
            res = self.results_queue.get(block=False)
            if isinstance(res, list):
                self.units = res

    def load_units(self):
        self.terminate()
        self.units.clear()
        self.watcher.removePaths(self.watcher.files())
        units_file_path = os.path.join(self.mod_path, r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
        self.watcher.addPath(units_file_path)
        self.request_update_progress.emit(0, "Loading units from file...")

        self.progress_queue = multiprocessing.Queue()
        self.results_queue = multiprocessing.Queue()
        self.worker = UnitLoaderWorker(self.mod_path, self.progress_queue, self.results_queue)
        self.worker.start()
        self.updater = threading.Thread(target=self.update_progress)
        self.updater.start()

    def get_units(self):
        if self.worker and self.worker.proc.is_alive():
            self.parent().show_loading_screen("Waiting for units to load...")
            while len(self.units) == 0:
                time.sleep(0.01)
                QtCore.QCoreApplication.processEvents()
            self.parent().hide_loading_screen()
        return self.units

    def terminate(self):
        if self.worker and self.worker.proc.is_alive():
            self.worker.proc.terminate()
        self.terminate_updater = True
        if self.updater and self.updater.is_alive():
            self.updater.join()
        self.terminate_updater = False


class UnitLoaderWorker:
    def __init__(self, mod_path, progress_queue, results_queue):
        self.mod_path = mod_path
        self.units = []
        self.proc = multiprocessing.Process(target=self.load_units, args=(progress_queue, results_queue))

    def start(self):
        self.proc.start()

    def load_units(self, progress_queue, results_queue):
        units_file_path = os.path.join(self.mod_path, r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
        progress_queue.put((0, "Loading units..."))
        with open(units_file_path, "r") as f:
            text = f.read()
        index = 0
        while index < len(text):
            # try parsing objects individually
            progress_queue.put((index / len(text), "Loading units..."))
            end = ndf_scanner.traverse_object(text, index)
            unit_text = text[index:end]
            index = end + 1
            unit = ndf.convert(unit_text)[0]
            # get unit name
            name = unit.n.removeprefix("Descriptor_Unit_")
            # get unit category
            modules = unit.value.by_member("ModulesDescriptors").v
            cat = modules.find_by_cond(
                lambda x: getattr(x.v, "type", None) == "TProductionModuleDescriptor").v.by_member("Factory").v
            cat = cat.removeprefix("EDefaultFactories/")
            # get transport module
            is_transport = True
            try:
                modules.find_by_cond(lambda x: getattr(x, "namespace", None) == "Transporter")
            except TypeError:
                is_transport = False
            unit = {"name": name, "category": cat, "is_transport": is_transport}
            self.units.append(unit)
        progress_queue.put((1, ""))
        results_queue.put(self.units)
