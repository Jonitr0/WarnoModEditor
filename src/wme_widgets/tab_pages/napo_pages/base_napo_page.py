# provides common functionality for Napo Tool Pages
import logging
import os
import json

from antlr4 import *

import ndf_parse as ndf

from PySide6 import QtWidgets, QtGui

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser import ndf_scanner
from src.ndf_parser.object_generator import napo_generator
from src.ndf_parser.ndf_converter import napo_to_ndf_converter

from src.ndf_parser.napo_entities.napo_collection import *
from src.ndf_parser.napo_entities.napo_assignment import *

from src.wme_widgets.tab_pages import base_tab_page
from src.wme_widgets import main_widget

from src.utils import icon_manager, resource_loader
from src.utils.color_manager import *
from src.dialogs import essential_dialogs


class BaseNapoPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

        self.main_layout = QtWidgets.QVBoxLayout()
        self.main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.main_layout)

        self.tool_bar = QtWidgets.QToolBar()
        self.main_layout.addWidget(self.tool_bar)

        save_action = self.tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        restore_icon = QtGui.QIcon()
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)

        self.restore_action = self.tool_bar.addAction(restore_icon, "Discard changes and restore page (F5)")
        self.restore_action.setShortcut("F5")
        self.restore_action.triggered.connect(self.on_restore)

        self.tool_bar.addSeparator()

        import_state_action = self.tool_bar.addAction(icon_manager.load_icon("import.png", COLORS.PRIMARY),
                                                      "Import configuration from file (Ctrl + I)")
        import_state_action.setShortcut("Ctrl+I")
        import_state_action.triggered.connect(self.import_state)

        export_state_action = self.tool_bar.addAction(icon_manager.load_icon("export.png", COLORS.PRIMARY),
                                                      "Export configuration to file (Ctrl + E)")
        export_state_action.setShortcut("Ctrl+E")
        export_state_action.triggered.connect(self.export_state)

    # parse a whole NDF file and return it as a Napo Entity List
    def get_napo_from_file(self, file_name: str, editing: bool = True) -> [NapoAssignment]:
        file_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file_name)

        if editing:
            self.open_file(file_path)

        input_stream = FileStream(file_path, encoding="utf8")

        lexer = NdfGrammarLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = NdfGrammarParser(stream)
        tree = parser.ndf_file()

        listener = napo_generator.NapoGenerator(parser)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return NapoFile(listener.assignments)

    # parse a part (e.g. object) of a given NDF file and return it as Napo Entity
    def get_napo_from_object(self, file_name: str, obj_name: str, editing: bool = True) -> NapoEntity:
        content, _, _ = ndf_scanner.get_object_range(file_name, obj_name)

        if editing:
            self.open_file(os.path.join(main_widget.instance.get_loaded_mod_path(), file_name))

        input_stream = InputStream(content)
        lexer = NdfGrammarLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = NdfGrammarParser(stream)
        tree = parser.ndf_file()

        listener = napo_generator.NapoGenerator(parser)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return NapoFile(listener.assignments)

    def write_napo_file(self, file_name: str, napo_file: NapoFile):
        file_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file_name)
        converter = napo_to_ndf_converter.NapoToNdfConverter()
        ndf_text = converter.convert(napo_file)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(ndf_text)

    def write_napo_object(self, file_name: str, obj_name: str, entity: NapoFile):
        file_path = os.path.join(main_widget.instance.get_loaded_mod_path(), file_name)
        converter = napo_to_ndf_converter.NapoToNdfConverter()
        ndf_text = converter.convert(entity)

        _, start, end = ndf_scanner.get_object_range(file_name, obj_name)

        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

        file_content = ndf_text.join([file_content[:start], file_content[end:]])
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)

    def parsed_list_to_py_list(self, parsed_list, d_type=str):
        py_list = []
        for entry in parsed_list.value:
            py_list.append(d_type(entry.value))
        return py_list

    def py_list_to_parsed_list(self, py_list):
        parsed_list = ndf.model.List()
        for val in py_list:
            expr = ndf.expression(str(val))
            parsed_list.add(**expr)
        return parsed_list

    # TODO: conversion functions for maps

    def get_parsed_ndf_file(self, file_name: str, editing: bool = True):
        mod_path = main_widget.instance.get_loaded_mod_path()
        file_path = os.path.join(mod_path, file_name)

        if editing:
            self.open_file(file_path)

        mod = ndf.Mod(mod_path, mod_path + "tmp")
        with mod.edit(file_path) as file_obj:
            return file_obj

    def on_restore(self):
        if self.unsaved_changes:
            dialog = essential_dialogs.ConfirmationDialog("Your changes will be discarded! Are you sure?", "Warning!")
            if not dialog.exec():
                return
        self.update_page()

    def get_state(self):
        pass

    def set_state(self, state: dict):
        pass

    # TODO: add version checking
    def import_state(self):
        if self.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog(self.tab_name)
            if not dialog.exec():
                return

            if dialog.save_changes:
                if not self.save_changes():
                    return

        current_state = self.get_state()
        try:
            file_name = resource_loader.get_persistant_path("")
            file_path, ret = QtWidgets.QFileDialog().getOpenFileName(self, "Select config file", file_name,
                                                                     options=QtWidgets.QFileDialog.ReadOnly,
                                                                     filter="*.txt")
            if not ret:
                return

            main_widget.instance.show_loading_screen("Importing state...")

            state = json.load(open(file_path, "r"))
            try:
                self.set_state(state)
            except Exception:
                essential_dialogs.MessageDialog("Error", "Could not import state. The file might be incompatible with "
                                                + self.tab_name).exec()
                self.set_state(current_state)
        except Exception as e:
            logging.error("Error while loading config for " + str(self.__class__) + ":" + str(e))
            self.set_state(current_state)

        main_widget.instance.hide_loading_screen()

    # TODO: add header/payload with metadata (version)
    def export_state(self):
        try:
            state = self.get_state()
            file_name = resource_loader.get_persistant_path(self.get_state_file_name())
            file_path, ret = QtWidgets.QFileDialog().getSaveFileName(self, "Select export file name", file_name,
                                                                     options=QtWidgets.QFileDialog.ReadOnly,
                                                                     filter="*.txt")
            if not ret:
                return

            json.dump(state, open(file_path, "w"), indent=4)
        except Exception as e:
            logging.error("Error while exporting config on " + str(self.__class__) + ":" + str(e))

    def get_state_file_name(self) -> str:
        return ""
