# TODO: when a mod is loaded, start loading certain information of all units in the background
# TODO: show progress bar in main widget
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
        self.pipe = None
        self.updater = threading.Thread(target=self.update_progress)

    def update_progress(self):
        while self.worker.proc.is_alive():
            # TODO: pull all
            if self.pipe.poll():
                progress, text = self.pipe.recv()
                self.request_update_progress.emit(progress, text)
                time.sleep(0.01)

    def load_units(self):
        self.pipe, child_pipe = multiprocessing.Pipe()
        self.worker = UnitLoaderWorker(self.mod_path, child_pipe)
        self.worker.start()
        self.updater.start()

    # TODO: stop loading units when mod is closed


class UnitLoaderWorker:
    def __init__(self, mod_path, pipe):
        self.mod_path = mod_path
        self.units = []
        self.proc = multiprocessing.Process(target=self.load_units, args=(pipe,))

    def start(self):
        self.proc.start()

    def load_units(self, pipe):
        units_file_path = os.path.join(self.mod_path, r"GameData\Generated\Gameplay\Gfx\UniteDescriptor.ndf")
        pipe.send((0.05, "Parsing units file..."))
        units_ndf = parser_utils.get_parsed_ndf_file(units_file_path)
        pipe.send((0.1, "Loading units..."))
        for i, unit in enumerate(units_ndf):
            pipe.send((0.1 + i / len(units_ndf) * 0.9, f"Loading units ({i}/{len(units_ndf)})..."))
            print(unit.namespace)
