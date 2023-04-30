import logging

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
        elif isinstance(data, NapoPair):
            self.lookup[data.value[0]] = len(self.value) - 1

    def _get_value(self, path: str, default=None):
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
            return self.value[self.lookup[current]]._get_value(remaining, default)
        else:
            print("Could not find value for " + str(path))
            return default

    def _set_value(self, path: str, value):
        # get current ID
        current = path.split("\\")[0]
        # build remaining path
        remaining = path.removeprefix(current)
        remaining = remaining.removeprefix("\\")
        # if nothing remains, return own value
        if current == "":
            self.value = value
        # otherwise, call function on own value
        elif self.lookup.__contains__(current):
            self.value[self.lookup[current]]._set_value(remaining, value)
        else:
            print("could not find " + path + "\nremaining: " + remaining)

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

    def set_value(self, path: str, value, dtypes: [NapoDatatype]):
        entity = napo_from_value(value, dtypes)
        self._set_value(path, entity)

    def get_value(self, path: str, default=None):
        result = self._get_value(path, default)
        return value_from_napo(result)

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


class NapoPair(NapoCollection):
    def __init__(self):
        super().__init__()
        self.value = []
        self.datatype = NapoDatatype.Pair

    def append(self, data: NapoEntity):
        super().append(data)
        if len(self.value) > 2:
            logging.warning("Tried to append " + str(data) + " to a full Pair. Discarded")
            del self.value[2]

    def _get_value(self, path: str, default=None):
        # TODO: handle path properly
        pass

    def __str__(self):
        return "{type: pair, value: " + ''.join(map(str, self.value)) + "}"


class NapoVector(NapoCollection):
    def __init__(self):
        super().__init__()
        self.value = []
        self.datatype = NapoDatatype.Vector

    def __str__(self):
        return "{type: vector, value: " + ''.join(map(str, self.value)) + "}"


class NapoMap(NapoCollection):
    def __init__(self):
        super().__init__()
        self.value = []
        self.map = {}
        self.datatype = NapoDatatype.Map

    def append(self, data: NapoPair):
        super().append(data)
        self.map[data.value[0]] = data.value[1]

    def __str__(self):
        return "{type: map, value: " + ''.join(map(str, self.value)) + "}"


def value_from_napo(entity: NapoEntity):
    if isinstance(entity, NapoMap):
        py_map = {}
        for key in entity.map.keys():
            py_map[value_from_napo(key)] = value_from_napo(entity.map[key])
        return py_map
    elif isinstance(entity, NapoCollection):
        vals = []
        for val in entity.value:
            vals.append(value_from_napo(val))
        return vals
    # else return a simple data type
    match entity.datatype:
        case NapoDatatype.Integer:
            return int(entity.value)
        case NapoDatatype.Boolean:
            return bool(entity.value)
        case NapoDatatype.Float:
            return float(entity.value)
        case _:
            return str(entity.value)


def napo_from_value(value, dtypes: [NapoDatatype]) -> NapoEntity:
    if isinstance(value, map):
        napo_map = NapoMap()
        for key in value.keys():
            napo_pair = NapoPair()
            napo_pair.append(napo_from_value(key, dtypes))
            napo_pair.append(napo_from_value(value[key], dtypes))
        return napo_map
    elif isinstance(value, list):
        napo_list = NapoVector()
        for val in value:
            napo_list.append(napo_from_value(val, dtypes))
        return napo_list
    # else construct primitive entity
    entity = NapoEntity()
    entity.datatype = dtypes.pop()
    match entity.datatype:
        case NapoDatatype.Integer:
            entity.value = int(value)
        case NapoDatatype.Boolean:
            entity.value = bool(value)
        case NapoDatatype.Float:
            entity.value = float(value)
        case _:
            entity.value = str(value)
    return entity
