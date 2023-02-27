from src.ndf_parser.napo_objects.napo_entity import *


class NapoAssignment(NapoEntity):
    id: str = ""
    datatype = NapoDatatype.STRUCTURAL

    def __str__(self):
        return "{id: " + self.id + ", type: assignment, value: " + str(self.value) + "}"
