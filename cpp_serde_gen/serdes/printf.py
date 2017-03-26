from .generic import GenericSerdeGenerator
from textwrap import dedent


class PrintfSerdeGenerator(GenericSerdeGenerator):

    def __init__(self, key="printf"):
        GenericSerdeGenerator.__init__(self, key)

    def generate_serialize_for_fields(self, record):
        fmt_str = """\tprintf("\\n\\t{0}: ");
\tprintf_serialize(data.{1});"""
        field_strs = [fmt_str.format(field.name,
                                     field.name) for field in record.fields]
        return "\n".join(field_strs)

    def generate_serialize(self, record):
        return dedent("""\
bool printf_serialize({0} const & data) {{
\tprintf("{0}:");
{1}
\tprintf("\\n");
\treturn true;
}}""".format(record.name, self.generate_serialize_for_fields(record)))

    def generate_deserialize(self, record):
        pass
