import clang.cindex as cl

class SerdeField(object):
    def __init__(self, name, t="void", access="PUBLIC"):
        self.name = name
        self.type = t
        self.access = access

    def __str__(self):
        return "{0}, {1}, {2}".format(self.name, self.type, self.access)

class SerdeType(object):
    def __init__(self, name, fields=[], serdes=[]):
        self.name = name
        self.fields = fields
        self.serdes = []

    def append_field(self, field):
        self.fields.append(field)

    # A serde is the string key of a serializer/deserializer class.
    def append_serde(self, serde):
        self.serdes.append(serde)

    def __str__(self):
        return "name: {0}\nfields: {1}".format(self.name,
            [str(field) for field in self.fields])
