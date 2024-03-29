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

    def get_napo_value(self, path: str, default=None):
        # to be implemented by subclasses
        print(self)
        print("not implemented")
        return default

    def set_napo_value(self, path: str, value):
        # to be implemented by subclasses
        print(self)
        print("not implemented")
