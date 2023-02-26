from src.ndf_parser.napo_objects.napo_entity import *


class NapoToNdfConverter:
    result = ""

    def convert(self, assignment_list: [NapoEntity]) -> str:
        self.result = ""
        for assignment in assignment_list:
            self.result += self.convert_assignment(assignment)
        return self.result

    def convert_assignment(self, assignment: NapoEntity) -> str:
        napo_str = assignment.id + " is "
        match assignment.datatype:
            case NapoDatatype.String_single:
                value = "\'" + str(assignment.value) + "\'"
            case NapoDatatype.String_double:
                value = "\"" + str(assignment.value) + "\""
            case _:
                value = str(assignment.value)
        napo_str += value + "\n"
        return napo_str
