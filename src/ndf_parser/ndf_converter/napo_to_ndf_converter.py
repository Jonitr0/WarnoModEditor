from src.ndf_parser.napo_entities.napo_collection import *
from src.ndf_parser.napo_entities.napo_assignment import *


INDENT_SIZE = 4

class NapoToNdfConverter:
    def __init__(self):
        self.indent = 0

    def increase_indent(self):
        self.indent += INDENT_SIZE

    def decrease_indent(self):
        self.indent -= INDENT_SIZE
        self.indent = max(0, self.indent)

    # TODO: formatting: add break up of structures based on line length
    def convert(self, napo_file: NapoFile) -> str:
        return self.convert_entity(napo_file)

    def convert_entity(self, entity: NapoEntity) -> str:
        match entity.datatype:
            case NapoDatatype.Pair:
                result_str = "(" + self.convert_entity(entity.value[0]) + ", " + \
                            self.convert_entity(entity.value[1]) + ")"
            case NapoDatatype.Vector:
                result_str = "["
                for i in range(len(entity.value)):
                    result_str += self.convert_entity(entity.value[i])
                    if i < len(entity.value)-1:
                        result_str += ", "
                result_str += "]"
            case NapoDatatype.Map:
                result_str = "MAP["
                for i in range(len(entity.value)):
                    result_str += self.convert_entity(entity.value[i])
                    if i < len(entity.value)-1:
                        result_str += ", "
                result_str += "]"
            case NapoDatatype.String_single:
                result_str = "\'" + str(entity.value) + "\'"
            case NapoDatatype.String_double:
                result_str = "\"" + str(entity.value) + "\""
            case NapoDatatype.RGBA:
                result_str = "RGBA["
                for i in range(4):
                    result_str += str(entity.value[i])
                    if i < 3:
                        result_str += ","
                result_str += "]"
            case NapoDatatype.Object:
                result_str = ""
                if entity.obj_type != "":
                    result_str = entity.obj_type + "\n"
                result_str += (self.indent - INDENT_SIZE) * " " + "(\n"
                for i in range(len(entity.value)):
                    result_str += self.convert_entity(entity.value[i])
                result_str += (self.indent - INDENT_SIZE) * " " + ")"
            case NapoDatatype.STRUCTURAL:
                if type(entity) == NapoAssignment:
                    result_str = ""
                    if type(entity.value) == NapoObject:
                        result_str += "\n"
                    result_str += self.indent * " "
                    if entity.export:
                        result_str = "export "
                    if entity.member:
                        result_str += entity.id + " = "
                    else:
                        result_str += entity.id + " is "
                    val_entity = entity.value
                    self.increase_indent()
                    result_str += self.convert_entity(val_entity) + "\n"
                    self.decrease_indent()
                elif type(entity) == NapoFile:
                    result_str = ""
                    for val in entity.value:
                        result_str += self.convert_entity(val)
                else:
                    result_str = ""
            case _:
                result_str = str(entity.value)
        return result_str
