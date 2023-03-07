import logging

from src.ndf_parser.napo_objects.napo_entity import *


class NapoPair(NapoEntity):
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
