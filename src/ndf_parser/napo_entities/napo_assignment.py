from src.ndf_parser.napo_entities.napo_entity import *


class NapoAssignment(NapoEntity):
    def __init__(self):
        super().__init__()
        self.id = ""
        self.datatype = NapoDatatype.STRUCTURAL
        self.export = False
        self.private = False
        self.member = False

    def __str__(self):
        return "{id: " + self.id + " type: assignment, export: " + str(self.export) + ", private: " + \
               str(self.private) + ", member: " + str(self.member) + ", value: " + str(self.value) + "}"

    def __eq__(self, other):
        if not type(other) == type(self):
            return False
        ret = self.datatype == other.datatype and self.id == other.id and self.export == other.export \
               and self.member == other.member and self.value == other.value
        return ret

    def get_napo_value(self, path: str, default=None):
        # get current ID
        current = path.split("\\")[0]
        # if nothing remains, return own value
        if current == "":
            return self.value
        elif isinstance(self.value, NapoEntity):
            return self.value.get_napo_value(path, default)
        else:
            return default

    def set_napo_value(self, path: str, value):
        # get current ID
        current = path.split("\\")[0]
        # if nothing remains, return own value
        if current == "":
            self.value = value
        elif isinstance(self.value, NapoEntity):
            self.value.set_napo_value(path, value)
        else:
            print("could not find " + path + "\ncurrent: " + current)

