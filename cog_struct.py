import cog

class CppStructEntry():
  def __init__(self, name, type, description=""):
    self.name = name
    self.type = type
    self.description = description

  def cog_struct_str(self):
    return "{0} {1}; ///< {2}".format(self.type, self.name, self.description)

  def cog_serialize_str(self):
    return "mpack_write_cstr(writer, \"{0}\");\n\tmpack_serialize(writer, *(data.{0}));".format(self.name)

  def cog_deserialize_str(self):
    return """
  mpack_node_t inode = mpack_node_map_cstr(node, "{0}");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {{
    return err;
  }}

  err = mpack_deserialize(inode, &(item->{0}));
  if (err != mpack_ok) {{
    return err;
  }}""".format(self.name)

  def cog_comment_str(self):
      return "\"{0}\": <{1}>,".format(self.name, self.type)

class CppStruct():
  def __init__(self, name, entries=None):
    self.name = name
    if entries:
        self.entries = entries
    else:
        self.entries = []

  def append_entry(self, name="", type="", description=""):
      self.entries.append(CppStructEntry(name, type, description))

  def cog_str(self):
    entries_str = "\n\t".join([e.cog_struct_str() for e in self.entries])
    return """
struct {0} {{
  {1}
}};""".format(self.name, entries_str)

  def mpack_serialize(self):
    entries_str = "\n\t".join([e.cog_serialize_str() for e in self.entries])
    entries_comment_str = "\n *\t\t\t".join([e.cog_comment_str() for e in self.entries])
    return """
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
""".format(self.name, len(self.entries), entries_str, entries_comment_str)

  def mpack_deserialize(self):
    entries_str = "\n\t".join([e.cog_deserialize_str() for e in self.entries])
    entries_comment_str = "\n *\t\t\t".join([e.cog_comment_str() for e in self.entries])

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
  """.format(self.name, len(self.entries), entries_str, entries_comment_str)

  def generate_all(self):
    cog.outl(self.cog_str())
    cog.outl(self.mpack_serialize())
    cog.outl(self.mpack_deserialize())

  def generate_serialize(self):
    cog.out(self.mpack_serialize(), dedent=True)
    cog.out(self.mpack_deserialize(), dedent=True)
