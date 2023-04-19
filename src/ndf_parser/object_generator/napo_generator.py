from antlr4 import *
from src.ndf_parser.antlr_output.NdfGrammarListener import NdfGrammarListener
from src.ndf_parser.antlr_output.NdfGrammarParser import NdfGrammarParser

from src.ndf_parser.napo_objects.napo_entity import *
from src.ndf_parser.napo_objects.napo_assignment import *
from src.ndf_parser.napo_objects.napo_datastructures import *
from src.ndf_parser.napo_objects.napo_object import *

import logging


class Stack:
    def __init__(self):
        self._stack = []

    def push(self, elem):
        self._stack.append(elem)

    def pop(self):
        return self._stack.pop()

    # return top element without removing it
    def top(self):
        if len(self._stack) > 0:
            return self._stack[len(self._stack)-1]
        else:
            return None

    def __len__(self):
        return len(self._stack)


# put on the Stack to mark end of a Stack frame
class StackMarker:
    pass


class NapoGenerator(NdfGrammarListener):

    def __init__(self, parser: NdfGrammarParser):
        super().__init__()
        self.rule_names = parser.ruleNames

        self.assignments = []
        self.stack = Stack()

    def enterAssignment(self, ctx:NdfGrammarParser.AssignmentContext):
        # push new assignment to stack
        self.stack.push(NapoAssignment())

    def exitAssignment(self, ctx:NdfGrammarParser.AssignmentContext):
        # pop value off stack and assign to assignment
        value = self.stack.pop()
        self.stack.top().value = value
        # pop assignment off stack if it's top level
        if len(self.stack) == 1:
            assignment = self.stack.pop()
            self.assignments.append(assignment)

    def enterExport(self, ctx:NdfGrammarParser.ExportContext):
        # assign "export" to top item on stack
        self.stack.top().export = True

    def enterId(self, ctx:NdfGrammarParser.IdContext):
        # assign ID to top item on stack
        self.stack.top().id = ctx.getText()

    def enterPrimitive_value(self, ctx:NdfGrammarParser.Primitive_valueContext):
        # assign datatype and value to new entity
        datatype = self.rule_names[ctx.children[0].getRuleIndex()]
        value = ctx.getText()
        entity = NapoEntity()
        match datatype:
            case "bool_value":
                entity.datatype = NapoDatatype.Boolean
                if value.lower() == "false":
                    entity.value = False
                else:
                    entity.value = True
            case "int_value":
                entity.datatype = NapoDatatype.Integer
                entity.value = int(value)
            case "hex_value":
                entity.datatype = NapoDatatype.HexInteger
                entity.value = value
            case "float_value":
                entity.datatype = NapoDatatype.Float
                entity.value = float(value)
            case "string_value":
                if value[0] == "\'":
                    entity.datatype = NapoDatatype.String_single
                else:
                    entity.datatype = NapoDatatype.String_double
                entity.value = value[1:-1]
            case "guid_value":
                entity.datatype = NapoDatatype.GUID
                entity.value = value
            case _:
                logging.warning("Unknown Data type for " + datatype)
                entity.datatype = NapoDatatype.UNKNOWN
                entity.value = value
        self.stack.push(entity)

    def enterObj_reference_value(self, ctx:NdfGrammarParser.Obj_reference_valueContext):
        # assign reference datatype and value to top item on stack
        entity = NapoEntity()
        entity.datatype = NapoDatatype.Reference
        entity.value = ctx.getText()
        self.stack.push(entity)

    def enterPair_value(self, ctx:NdfGrammarParser.Pair_valueContext):
        self.stack.push(NapoPair())
        self.stack.push(StackMarker())

    def exitPair_value(self, ctx:NdfGrammarParser.Pair_valueContext):
        pair_values = []
        while type(self.stack.top()) != StackMarker:
            pair_values.append(self.stack.pop())
        pair_values.reverse()
        # remove stack marker
        self.stack.pop()
        for value in pair_values:
            self.stack.top().append(value)

    # TODO: can this be merged with Pair and Map?
    def enterVector_value(self, ctx:NdfGrammarParser.Vector_valueContext):
        self.stack.push(NapoVector())
        self.stack.push(StackMarker())
        
    def exitVector_value(self, ctx:NdfGrammarParser.Vector_valueContext):
        vector_values = []
        while type(self.stack.top()) != StackMarker:
            vector_values.append(self.stack.pop())
        vector_values.reverse()
        # remove stack marker
        self.stack.pop()
        for value in vector_values:
            self.stack.top().append(value)

    def enterMap_value(self, ctx:NdfGrammarParser.Map_valueContext):
        self.stack.push(NapoMap())
        self.stack.push(StackMarker())

    def exitMap_value(self, ctx:NdfGrammarParser.Map_valueContext):
        map_values = []
        while type(self.stack.top()) != StackMarker:
            map_values.append(self.stack.pop())
        map_values.reverse()
        # remove stack marker
        self.stack.pop()
        for value in map_values:
            self.stack.top().append(value)

    def enterObj_type(self, ctx:NdfGrammarParser.Obj_typeContext):
        obj = NapoObject()
        obj.obj_type = ctx.getText()
        self.stack.push(obj)
        self.stack.push(StackMarker())





