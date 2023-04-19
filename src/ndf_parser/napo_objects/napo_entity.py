# provides common functionality for any NAPO object

class NapoDatatype:
    UNKNOWN, STRUCTURAL, Boolean, Integer, HexInteger, Float, String_single, String_double, GUID, Reference, Pair, Vector, Map, Object = range(14)


class NapoEntity:
    def __init__(self):
        self.datatype = NapoDatatype.UNKNOWN
        self.value = None

    def __str__(self):
        return "{type: " + str(self.datatype) + ", value: " + str(self.value) + "}"
