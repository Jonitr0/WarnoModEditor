from src.ndf_parser.napo_objects.napo_entity import *
from src.ndf_parser.napo_objects.napo_assignment import *
from src.ndf_parser.napo_objects import napo_datastructures


class NapoToNdfConverter:
    result = ""

    def convert(self, assignment_list: [NapoEntity]) -> str:
        self.result = ""
        for assignment in assignment_list:
            self.result += self.convert_assignment(assignment)
        return self.result

    def convert_assignment(self, assignment: NapoAssignment) -> str:
        napo_str = assignment.id + " is "
        entity = assignment.value
        napo_str += self.convert_entity(entity) + "\n"
        return napo_str

    def convert_entity(self, entity: NapoEntity) -> str:
        match entity.datatype:
            case NapoDatatype.Pair:
                value_str = "(" + self.convert_entity(entity.value[0]) + ", " + \
                            self.convert_entity(entity.value[1]) + ")"
            case NapoDatatype.String_single:
                value_str = "\'" + str(entity.value) + "\'"
            case NapoDatatype.String_double:
                value_str = "\"" + str(entity.value) + "\""
            case _:
                value_str = str(entity.value)
        return value_str
