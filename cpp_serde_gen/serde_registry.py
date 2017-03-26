class SerdeRegistry(object):
    """
    A class which wraps a dictionary keys of keys to SerDe generators.
    """

    def __init__(self, serdes=[]):
        """
        Initialize with some serdes, extract the serdes key and insert it into
        the dictionary.

        Parameters ::
            - serdes: A List of SerdeGenerator's (see serdes/generic.py)
        """
        self.registry = {serde.key: serde for serde in serdes}

    def register(self, serde):
        """
        Add a serde to the registry.

        Parameters ::
            - serde: A SerdeGenerator to add.
        """
        self.registry[serde.key] = serde

    def get(self, key):
        """
        Lookup the SerdeGenerator by key.

        Parameters ::
            - key: The key as a string to lookup

        Returns ::
            - The SerdeGenerator associated with the key or will throw an
              exception
        """
        return self.registry[key]

    def generate_serialize(self, key, record):
        """
        A convenience function for calling the SerdeGenerator's
        generate_serialize function directly from the registry.

        Parameters ::
            - key: The key of the SerdeGenerator to look up.
            - record: The record to generate the serialize code for.

        Returns ::
            - Returns the serialiation code as a string
        """
        return self.registry[key].generate_serialize(record)

    def generate_deserialize(self, key, record):
        """
        A convenience function for calling the SerdeGenerator's
        generate_deserialize function directly from the registry.

        Parameters ::
            - key: The key of the SerdeGenerator to look up.
            - record: The record to generate the deserialize code for.

        Returns ::
            - Returns the deserialize code as a string
        """
        return self.registry[key].generate_deserialize(record)
