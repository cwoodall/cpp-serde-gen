class SerdeRegistry(object):
    def __init__(self, serdes=[]):
        self.registry = {serde.key: serde for serde in serdes}

    def register(self, serde):
        self.registry[serde.key] = serde

    def get(self, key):
        return self.registry[key]

    def generate_serialize(self, key, record):
        return self.registry[key].generate_serialize(record)

    def generate_deserialize(self, key, record):
        return self.registry[key].generate_deserialize(record)
