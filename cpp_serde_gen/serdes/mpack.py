from .generic import GenericSerdeGenerator
from textwrap import dedent


class MpackSerdeGenerator(GenericSerdeGenerator):

    def __init__(self, key="mpack"):
        GenericSerdeGenerator.__init__(self, key)

    def field_comment_str(self, field):
        return "\"{0}\": <{1}>,".format(field.name, field.type)

    def generate_serialize_for_field(self, field):
        return """\
  mpack_write_cstr(writer, "{0}");
  mpack_serialize(writer, *(data.{0}));""".format(field.name)

    def generate_serialize(self, record):
        entries_str = "\n\t".join([self.generate_serialize_for_field(field)
                                   for field in record.fields])
        entries_comment = "\n *      ".join([self.field_comment_str(field)
                                             for field in record.fields])

        return """\
/**
 * Serialize the {0} type into the format:
 *
 *    {{
 *      {3}
 *    }}
 *
 * @param writer  mpack_writer_t to serialize the message into
 * @param data    A {0} to serialize.
 */
static inline void mpack_serialize(mpack_writer_t *writer,
                                   {0} const &data) {{
  mpack_start_map(writer, {1});
{2}
  mpack_finish_map(writer);
}}
""".format(record.name, len(record.fields), entries_str, entries_comment)

    def generate_deserialize_for_field(self, field):
        return """
  mpack_node_t inode = mpack_node_map_cstr(node, "{0}");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {{
    return err;
  }}

  err = mpack_deserialize(inode, &(item->{0}));
  if (err != mpack_ok) {{
    return err;
  }}""".format(field.name)

    def generate_deserialize(self, record):
        entries_str = "\n\t".join([self.generate_deserialize_for_field(field)
                                   for field in record.fields])
        entries_comment = "\n *      ".join([self.field_comment_str(field)
                                             for field in record.fields])

        return """
/**
 * Deserializes the raw msgpack format of a {0} type into a struct:
 *
 *    {{
 *      {3}
 *    }}
 *
 * @param node   mpack_node_t to deserialize with, points to a node on the
 *               msgpack tree.
 * @param item   A {0} to deserialize into.
 */
mpack_error_t mpack_deserialize(mpack_node_t node,
                                {0} *item) {{
  assert(item != nullptr);
  if (mpack_node_map_count(node) != {1}) {{
    return mpack_error_invalid;
  }}

  {2}

  return mpack_ok;
}}
  """.format(record.name, len(record.fields), entries_str, entries_comment)
