# provides common functionality for Napo Tool Pages

from antlr4 import *

from src.ndf_parser.antlr_output.NdfGrammarLexer import NdfGrammarLexer
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.object_generator import napo_generator
from src.ndf_parser.ndf_converter import napo_to_ndf_converter

from src.wme_widgets.tab_pages import base_tab_page

from src.ndf_parser.napo_entities.napo_assignment import *


class BaseNapoPage(base_tab_page.BaseTabPage):
    def __init__(self):
        super().__init__()

    # parse a whole NDF file and return it as a Napo Entity List
    def get_napo_from_file(self, file_name: str) -> [NapoAssignment]:
        input_stream = FileStream(file_name, encoding="utf8")

        lexer = NdfGrammarLexer(input_stream)
        stream = CommonTokenStream(lexer)
        parser = NdfGrammarParser(stream)
        tree = parser.ndf_file()

        listener = napo_generator.NapoGenerator(parser)
        walker = ParseTreeWalker()
        walker.walk(listener, tree)

        return listener.assignments

    # parse a part (e.g. object) of a given NDF file and return it as Napo Entity
    def get_napo_from_object(self, file_name: str, obj_name: str) -> NapoEntity:
        pass

    def write_napo_file(self, file_name: str, assignments: [NapoAssignment]):
        converter = napo_to_ndf_converter.NapoToNdfConverter()
        ndf_text = converter.convert(assignments)
        with open(file_name, "t", encoding="utf-8") as f:
            f.write(ndf_text)

    def write_napo_object(self, file_name: str, obj_name: str, entity: NapoEntity):
        pass


# TODO: maybe include specific UI elements which can be linked to NAPO properties
