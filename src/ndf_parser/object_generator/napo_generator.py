from antlr4 import *
from src.ndf_parser.antlr_output.NdfGrammarListener import NdfGrammarListener
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.napo_objects.napo_entity import *

import logging


class NapoGenerator(NdfGrammarListener):

    def __init__(self, parser: NdfGrammarParser):
        super().__init__()
        self.rule_names = parser.ruleNames

        self.assignments = []
        self.current_assignment = None

    def enterAssignment(self, ctx:NdfGrammarParser.AssignmentContext):
        self.current_assignment = NapoEntity()

    def exitAssignment(self, ctx:NdfGrammarParser.AssignmentContext):
        self.assignments.append(self.current_assignment)

    def enterId(self, ctx:NdfGrammarParser.IdContext):
        self.current_assignment.id = ctx.getText()

    def enterPrimitive_value(self, ctx:NdfGrammarParser.Primitive_valueContext):
        datatype = self.rule_names[ctx.children[0].getRuleIndex()]
        value = ctx.getText()
        match datatype:
            case "bool_value":
                self.current_assignment.datatype = NapoDatatype.Boolean
                if value.lower() == "false":
                    self.current_assignment.value = False
                else:
                    self.current_assignment.value = True
            case "int_value":
                self.current_assignment.datatype = NapoDatatype.Integer
                self.current_assignment.value = int(value)
            case "hex_value":
                self.current_assignment.datatype = NapoDatatype.HexInteger
                self.current_assignment.value = value
            case "float_value":
                self.current_assignment.datatype = NapoDatatype.Float
                self.current_assignment.value = float(value)
            case "string_value":
                if value[0] == "\'":
                    self.current_assignment.datatype = NapoDatatype.String_single
                else:
                    self.current_assignment.datatype = NapoDatatype.String_double
                self.current_assignment.value = value[1:-1]
            case "guid_value":
                self.current_assignment.datatype = NapoDatatype.GUID
                self.current_assignment.value = value
            case _:
                logging.warning("Unknown Data type for " + datatype)
                self.current_assignment.datatype = NapoDatatype.Unknown
                self.current_assignment.value = value

    def enterObj_reference_value(self, ctx:NdfGrammarParser.Obj_reference_valueContext):
        self.current_assignment.datatype = NapoDatatype.Reference
        self.current_assignment.value = ctx.getText()
