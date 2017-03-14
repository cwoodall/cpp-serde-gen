from .generic import GenericSerdeGenerator
from textwrap import dedent

class PrintfSerdeGenerator(GenericSerdeGenerator):
    def __init__(self, key="printf"):
        GenericSerdeGenerator.__init__(self, key)

    def generate_serialize_for_fields(self, record):

        return "\n".join(["\tprintf(\"\\n\\t{0}: \");\n\tprintf_serialize(data.{1});\n\tprintf(\"\\n\");".format(field.name, field.name) for field in record.fields])

    def generate_serialize(self, record):
        return dedent("""\
bool printf_serialize({0} const & data) {{
\tprintf("{0}:");
{1}
}}""".format(record.name, self.generate_serialize_for_fields(record)))

    def generate_deserialize(self, record):
        pass