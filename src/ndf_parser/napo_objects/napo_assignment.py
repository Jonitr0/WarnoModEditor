from src.ndf_parser.napo_objects.napo_entity import *


class NapoAssignment(NapoEntity):
    def __init__(self):
        super().__init__()
        self.id = ""
        self.datatype = NapoDatatype.STRUCTURAL
        self.export = False

    def __str__(self):
        return "{id: " + self.id + ", type: assignment, value: " + str(self.value) + "}"
