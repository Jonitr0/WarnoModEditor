# provides common functionality for any NAPO object

class NapoDatatype:
    UNKNOWN, STRUCTURAL, Boolean, Integer, HexInteger, Float, String_single, String_double, GUID, RGBA, Reference, \
        Pair, Vector, Map, Arithmetic, Object = range(16)


class NapoEntity:
    def __init__(self):
        self.datatype = NapoDatatype.UNKNOWN
        self.value = None

    def __str__(self):
        return "{type: " + str(self.datatype) + ", value: " + str(self.value) + "}"
