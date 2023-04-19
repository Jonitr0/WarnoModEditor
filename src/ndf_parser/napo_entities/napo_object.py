from src.ndf_parser.napo_entities.napo_entity import *


class NapoObject(NapoEntity):
    def __init__(self):
        super().__init__()
        self.value = []
        self.obj_type = ""
        self.datatype = NapoDatatype.Object

    def append(self, member: NapoEntity):
        self.value.append(member)

    def __str__(self):
        return "{type: object, value: " + ''.join(map(str, self.value)) + "}"
