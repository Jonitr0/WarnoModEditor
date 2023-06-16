# provides common functionality for Napo Tool Pages
import logging
import os
import json

from antlr4 import *

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

        main_layout = QtWidgets.QVBoxLayout()

        self.tool_bar = QtWidgets.QToolBar()
        main_layout.addWidget(self.tool_bar)

        save_action = self.tool_bar.addAction(icon_manager.load_icon("save.png", COLORS.PRIMARY), "Save (Ctrl + S)")
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_changes)

        restore_icon = QtGui.QIcon()
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.PRIMARY), QtGui.QIcon.Normal)
        restore_icon.addPixmap(icon_manager.load_pixmap("restore.png", COLORS.SECONDARY_LIGHT), QtGui.QIcon.Disabled)

        self.restore_action = self.tool_bar.addAction(restore_icon, "Discard changes and restore page (F5)")
        self.restore_action.setShortcut("F5")
        self.restore_action.triggered.connect(self.on_restore)
        self.restore_action.setEnabled(False)

        self.tool_bar.addSeparator()

        import_state_action = self.tool_bar.addAction(icon_manager.load_icon("import.png", COLORS.PRIMARY),
                                                      "Import configuration from file (Ctrl + I)")
        import_state_action.setShortcut("Ctrl+I")
        import_state_action.triggered.connect(self.import_state)

        export_state_action = self.tool_bar.addAction(icon_manager.load_icon("export.png", COLORS.PRIMARY),
                                                      "Export configuration to file (Ctrl + E)")
        export_state_action.setShortcut("Ctrl+E")
        export_state_action.triggered.connect(self.export_state)

        self.unsaved_status_change.connect(self.on_unsaved_changed)

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_widget = QtWidgets.QWidget()
        scroll_area.setWidget(scroll_widget)
        self.scroll_layout = QtWidgets.QVBoxLayout()
        self.scroll_layout.setContentsMargins(0, 0, 0, 0)
        scroll_widget.setLayout(self.scroll_layout)

        self.setLayout(main_layout)

    def clear_layout(self):
        while self.scroll_layout.count():
            child = self.scroll_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

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

    def on_restore(self):
        if not essential_dialogs.ConfirmationDialog("Your changes will be discarded! Are you sure?", "Warning!").exec():
            return
        self.update_page()

    def on_unsaved_changed(self, unsaved: bool, widget):
        self.restore_action.setEnabled(unsaved)

    def get_state(self):
        pass

    def set_state(self, state: dict):
        pass

    def import_state(self):
        if self.unsaved_changes:
            dialog = essential_dialogs.AskToSaveDialog("Operation Editor")
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
            self.set_state(state)
        except Exception as e:
            logging.error("Error while loading config for " + str(self.__class__) + ":" + str(e))
            self.set_state(current_state)

        main_widget.instance.hide_loading_screen()

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
