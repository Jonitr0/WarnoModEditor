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

    def __eq__(self, other):
        if not type(other) == type(self):
            return False
        return self.datatype == other.datatype and self.value == other.value

    def __hash__(self):
        return hash((self.datatype, self.value))

    # TODO: create analogous method to set values
    def find(self, path: str, default=None):
        # to be implemented by subclasses
        return default
