# provides common functionality for any NAPO object

class NapoDatatype:
    UNKNOWN, STRUCTURAL, Boolean, Integer, HexInteger, Float, String_single, String_double, GUID, Reference, Pair, Vector, Map = range(13)


class NapoEntity:
    datatype = NapoDatatype.UNKNOWN
    value = None

    def __str__(self):
        return "{type: " + str(self.datatype) + ", value: " + str(self.value) + "}"
