import logging

from src.ndf_parser.napo_objects.napo_entity import *


class NapoPair(NapoEntity):
    datatype = NapoDatatype.Pair
    value = []

    def append(self, data: NapoEntity):
        if len(self.value) >= 2:
            logging.warning("Tried to append " + str(data) + " to a full Pair. Discarded")
            return
        self.value.append(data)