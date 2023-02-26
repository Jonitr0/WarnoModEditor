# provides common functionality for any NAPO object

class NapoDatatype:
    Unknown, Boolean, Integer, HexInteger, Float, String_single, String_double, GUID, Reference = range(9)


class NapoEntity:
    id = ""
    datatype = NapoDatatype.Unknown
    value = None

    def __str__(self):
        return "id: " + self.id + " type: " + str(self.datatype) + " value: " + str(self.value)
