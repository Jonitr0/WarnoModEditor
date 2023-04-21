import logging

from src.ndf_parser.napo_entities.napo_entity import *


class NapoPair(NapoDeepComparable):
    def __init__(self):
        super().__init__()
        self.value = []
        self.datatype = NapoDatatype.Pair

    def append(self, data: NapoEntity):
        if len(self.value) >= 2:
            logging.warning("Tried to append " + str(data) + " to a full Pair. Discarded")
            return
        self.value.append(data)

    def __str__(self):
        return "{type: pair, value: " + ''.join(map(str, self.value)) + "}"


class NapoVector(NapoDeepComparable):
    def __init__(self):
        super().__init__()
        self.value = []
        self.datatype = NapoDatatype.Vector

    def append(self, data: NapoEntity):
        self.value.append(data)

    def __str__(self):
        return "{type: vector, value: " + ''.join(map(str, self.value)) + "}"


class NapoMap(NapoDeepComparable):
    def __init__(self):
        super().__init__()
        self.value = []
        self.map = {}
        self.datatype = NapoDatatype.Map

    def append(self, data: NapoPair):
        self.value.append(data)
        self.map[data.value[0]] = data.value[1]

    def __str__(self):
        return "{type: map, value: " + ''.join(map(str, self.value)) + "}"


