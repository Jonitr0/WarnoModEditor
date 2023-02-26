# provides common functionality for any NAPO object

class NapoDatatype:
    Boolean, Integer, HexInteger, Float, String, GUID, Reference = range(7)


class NapoEntity:
    id = ""
    datatype = NapoDatatype.Boolean
    value = None
