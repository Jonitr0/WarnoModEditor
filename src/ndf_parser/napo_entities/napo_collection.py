from src.ndf_parser.napo_entities.napo_entity import *
from src.ndf_parser.napo_entities.napo_assignment import *


class NapoCollection(NapoEntity):
    def __init__(self):
        super().__init__()
        self.value = []
        self.lookup = {}

    def append(self, data: NapoEntity):
        self.value.append(data)
        if isinstance(data, NapoAssignment):
            self.lookup[data.id] = len(self.value) - 1
        elif isinstance(data, NapoObject):
            self.lookup[data.obj_type] = len(self.value) - 1

    def find(self, path: str, default=None):
        # get current ID
        current = path.split("\\")[0]
        # build remaining path
        remaining = path.removeprefix(current)
        remaining = remaining.removeprefix("\\")
        # if nothing remains, return own value
        if current == "":
            return self.value
        # otherwise, call function on own value
        elif self.lookup.__contains__(current):
            return self.value[self.lookup[current]].find(remaining, default)
        else:
            return default

    def __eq__(self, other):
        if not type(other) == type(self):
            return False
        if not len(self.value) == len(other.value):
            return False
        for i in range(len(self.value)):
            if not self.value[i] == other.value[i]:
                return False
        return True


class NapoFile(NapoCollection):
    def __init__(self, assignments=[]):
        super().__init__()
        self.datatype = NapoDatatype.STRUCTURAL
        for assignment in assignments:
            self.append(assignment)

    def __str__(self):
        return "{type: file, value: " + ''.join(map(str, self.value)) + "}"


class NapoObject(NapoCollection):
    def __init__(self):
        super().__init__()
        self.value = []
        self.obj_type = ""
        self.datatype = NapoDatatype.Object

    def __str__(self):
        return "{type: object, value: " + ''.join(map(str, self.value)) + "}"

    def __eq__(self, other):
        if not type(other) == type(self):
            return False
        if self.obj_type != other.obj_type or self.value != other.value:
            return False
        return super().__eq__(other)
