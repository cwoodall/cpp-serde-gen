class GenericSerdeGenerator(object):
    def __init__(self, key):
        self.key = key

    def generate_serialize(self, record):
        pass

    def generate_deserialize(self, record):
        pass

    def __str__(self):
        return "SerdeGenerator <{0}>".format(self.key)
