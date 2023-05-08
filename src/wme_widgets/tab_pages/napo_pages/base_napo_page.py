# provides common functionality for Napo Tool Pages

from antlr4 import *

from PySide6 import QtWidgets, QtGui

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.object_generator import napo_generator
from src.ndf_parser.ndf_converter import napo_to_ndf_converter

from src.ndf_parser.napo_entities.napo_collection import *
from src.ndf_parser.napo_entities.napo_assignment import *

from src.wme_widgets.tab_pages import base_tab_page
from src.utils import icon_manager
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

    # parse a whole NDF file and return it as a Napo Entity List
    def get_napo_from_file(self, file_name: str) -> [NapoAssignment]:
        self.open_file(file_name)

        input_stream = FileStream(file_name, encoding="utf8")

        lexer = NdfGrammarLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = NdfGrammarParser(stream)
        tree = parser.ndf_file()

        listener = napo_generator.NapoGenerator(parser)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return NapoFile(listener.assignments)

    # parse a part (e.g. object) of a given NDF file and return it as Napo Entity
    def get_napo_from_object(self, file_name: str, obj_name: str) -> NapoEntity:
        pass

    def write_napo_file(self, file_name: str, napo_file: NapoFile):
        converter = napo_to_ndf_converter.NapoToNdfConverter()
        ndf_text = converter.convert(napo_file)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(ndf_text)

    def write_napo_object(self, file_name: str, obj_name: str, entity: NapoEntity):
        pass

    def on_restore(self):
        if not essential_dialogs.ConfirmationDialog("Your changes will be discarded! Are you sure?", "Warning!").exec():
            return
        self.update_page()

    def on_unsaved_changed(self, unsaved: bool, widget):
        self.restore_action.setEnabled(unsaved)
