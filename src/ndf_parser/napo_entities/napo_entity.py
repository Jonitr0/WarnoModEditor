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


class NapoDeepComparable(NapoEntity):
    def __init__(self):
        super().__init__()
        self.value = []

    def __eq__(self, other):
        if not type(other) == type(self):
            return False
        if not len(self.value) == len(other.value):
            return False
        for i in range(len(self.value)):
            if not self.value[i] == other.value[i]:
                return False
        return True


class NapoFile(NapoDeepComparable):
    def __init__(self, assignments=[]):
        super().__init__()
        self.datatype = NapoDatatype.STRUCTURAL
        self.value = assignments

    def __str__(self):
        return "{type: file, value: " + ''.join(map(str, self.value)) + "}"
