from src.ndf_parser.napo_entities.napo_entity import *


class NapoAssignment(NapoEntity):
    def __init__(self):
        super().__init__()
        self.id = ""
        self.datatype = NapoDatatype.STRUCTURAL
        self.export = False
        self.member = False

    def __str__(self):
        return "{id: " + self.id + " type: assignment, export: " + str(self.export) + ", member: " + \
               str(self.member) + ", value: " + str(self.value) + "}"

    def __eq__(self, other):
        if not type(other) == type(self):
            return False
        ret = self.datatype == other.datatype and self.id == other.id and self.export == other.export \
               and self.member == other.member and self.value == other.value
        if not ret:
            print(self.value == other.value)
            print(self)
            print(other)
        return ret
