# TODO: when unit editor exists, make a unit browser for main widget
import os
import time
import threading
import multiprocessing

from PySide6 import QtCore

from src.ndf import parser_utils


class UnitLoader(QtCore.QObject):
    request_update_progress = QtCore.Signal(float, str)

    def __init__(self):
        super().__init__()
        # update when mod is loaded
        self.mod_path = ""
        self.units = []
        self.worker = None
        self.queue = None
        self.terminate_updater = False
        self.updater = None
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.load_units)

    def update_progress(self):
        progress = 0
        text = "Loading units..."
        while self.worker.proc.is_alive() and self.terminate_updater is False:
            while not self.queue.empty():
                progress, text = self.queue.get(block=False)
            self.request_update_progress.emit(progress, text)
            time.sleep(0.01)
        self.request_update_progress.emit(1, "")

    def load_units(self):
        self.terminate()
        self.units.clear()
        self.watcher.removePaths(self.watcher.files())
        units_file_path = os.path.join(self.mod_path, r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
        self.watcher.addPath(units_file_path)
        self.request_update_progress.emit(0, "Loading units from file...")

        self.queue = multiprocessing.Queue()
        self.worker = UnitLoaderWorker(self.mod_path, self.queue)
        self.worker.start()
        self.updater = threading.Thread(target=self.update_progress)
        self.updater.start()

    def terminate(self):
        if self.worker and self.worker.proc.is_alive():
            self.worker.proc.terminate()
        self.terminate_updater = True
        if self.updater and self.updater.is_alive():
            self.updater.join()
        self.terminate_updater = False


class UnitLoaderWorker:
    def __init__(self, mod_path, queue):
        self.mod_path = mod_path
        self.units = []
        self.proc = multiprocessing.Process(target=self.load_units, args=(queue,))

    def start(self):
        self.proc.start()

    def load_units(self, queue):
        units_file_path = os.path.join(self.mod_path, r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
        queue.put((0.05, "Parsing units file..."))
        units_ndf = parser_utils.get_parsed_ndf_file(units_file_path)
        queue.put((0.1, "Loading units..."))
        for i, unit in enumerate(units_ndf):
            # try parsing objects individually
            queue.put((0.1 + i / len(units_ndf) * 0.9, f"Loading units ({i}/{len(units_ndf)})..."))
            # get unit name
            name = unit.n.removeprefix("Descriptor_Unit_")
            # get unit category
            modules = unit.value.by_member("ModulesDescriptors").v
            cat = modules.find_by_cond(
                lambda x: getattr(x.v, "type", None) == "TProductionModuleDescriptor").v.by_member("Factory").v
            print(name, cat)
