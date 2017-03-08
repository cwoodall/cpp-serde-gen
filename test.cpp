#include <iostream>

//+mpack-serializable
struct GroupStatus {
  uint8_t handedness; ///<
  uint8_t outerlink;  ///<
  uint8_t patient;    ///<
  uint8_t estop;      ///<
};

//+mpack-serializable
struct WowSoCool {
  float32_t cool; ///<
  float32_t lol;
  std::array<wow, 2, 3> foo;
  const char *wow;
  char foo[10];
};

/*[[[cog
from  cog_struct import *
import clang.cindex
def srcrangestr(x):
    return '%s:%d:%d - %s:%d:%d' % (x.start.file, x.start.line, x.start.column,
x.end.file, x.end.line, x.end.column)
from ctypes.util import find_library
clang.cindex.Config.set_library_file(find_library('clang-3.8'))

structs = []
struct_entry_workspace = {"type": "", "name": ""}
type_str = []
index = clang.cindex.Index.create()
tu = index.parse(cog.inFile)
cog.msg(tu.spelling)
parse_state = "IDLE"

prev = None
for x in tu.cursor.get_tokens():
  if parse_state is "IDLE":
    struct_entry_workspace = {}
    type_str = []
    if x.kind == clang.cindex.TokenKind.COMMENT:
      if x.spelling == "//+mpack-serializable":
        parse_state = "FIND_STRUCT"
  elif parse_state == "FIND_STRUCT":
    if (x.kind == clang.cindex.TokenKind.KEYWORD and x.spelling == "struct"):
      parse_state = "GET_NAME"
    elif (x.kind != clang.cindex.TokenKind.COMMENT):
      cog.msg("ERROR")
      parse_state = "IDLE"
  elif parse_state == "GET_NAME":
    if (x.kind == clang.cindex.TokenKind.IDENTIFIER ):
      structs.append(CppStruct(x.spelling))
      cog.msg("Adding struct: {0}".format(x.spelling))
      parse_state = "FIND_START_BRACE"
    elif (x.kind != clang.cindex.TokenKind.COMMENT):
      cog.msg("ERROR")
      parse_state = "IDLE"
  elif parse_state == "FIND_START_BRACE":
    if (x.kind == clang.cindex.TokenKind.PUNCTUATION and x.spelling == "{"):
      parse_state = "GET_TYPE"
    elif (x.kind != clang.cindex.TokenKind.COMMENT):
      cog.msg("ERROR")
      parse_state = "IDLE"
  elif parse_state == "GET_TYPE":
    if (x.kind == clang.cindex.TokenKind.PUNCTUATION and x.spelling == ";"):
      cog.msg(str(type_str))
      c = type_str.pop().strip()
      if (c == "]"):
        while (c != "["):
          c = type_str.pop().strip()
        c = type_str.pop().strip()
        type_str += ["[", "]"]

      struct_entry_workspace["name"] = c
      struct_entry_workspace["type"] = "".join(type_str).strip()
      structs[-1].append_entry(**struct_entry_workspace)
      struct_entry_workspace = {}
      type_str = []
      parse_state = "GET_TYPE"
    elif (x.kind == clang.cindex.TokenKind.PUNCTUATION and x.spelling == "}"):
      parse_state = "IDLE"
    elif (x.kind !=  clang.cindex.TokenKind.COMMENT):
      if (x.kind != clang.cindex.TokenKind.PUNCTUATION
        and prev != clang.cindex.TokenKind.PUNCTUATION
        and prev):
        type_str.append(" " + x.spelling)
      else:
        type_str.append(x.spelling)
      prev = x.kind

for s in structs:
  s.generate_serialize()
]]]*/

/**
 * Serialize the GroupStatus type into the format:
 *
 *    {
 *      "handedness": <uint8_t>,
 *			"outerlink": <uint8_t>,
 *			"patient": <uint8_t>,
 *			"estop": <uint8_t>,
 *    }
 *
 * @param writer  mpack_writer_t to serialize the message into
 * @param data    A GroupStatus to serialize.
 */
static inline void mpack_serialize(mpack_writer_t *writer,
                                   GroupStatus const &data) {
  mpack_start_map(writer, 4);
  mpack_write_cstr(writer, "handedness");
	mpack_serialize(writer, *(data.handedness));
	mpack_write_cstr(writer, "outerlink");
	mpack_serialize(writer, *(data.outerlink));
	mpack_write_cstr(writer, "patient");
	mpack_serialize(writer, *(data.patient));
	mpack_write_cstr(writer, "estop");
	mpack_serialize(writer, *(data.estop));
  mpack_finish_map(writer);
}

/**
 * Deserializes the raw msgpack format of a GroupStatus type into a struct:
 *
 *    {
 *      "handedness": <uint8_t>,
 *			"outerlink": <uint8_t>,
 *			"patient": <uint8_t>,
 *			"estop": <uint8_t>,
 *    }
 *
 * @param node   mpack_node_t to deserialize with, points to a node on the
 *               msgpack tree.
 * @param item   A GroupStatus to deserialize into.
 */
mpack_error_t mpack_deserialize(mpack_node_t node,
                                GroupStatus *item) {
  assert(item != nullptr);
  if (mpack_node_map_count(node) != 4) {
    return mpack_error_invalid;
  }

  
  mpack_node_t inode = mpack_node_map_cstr(node, "handedness");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->handedness));
  if (err != mpack_ok) {
    return err;
  }
	
  mpack_node_t inode = mpack_node_map_cstr(node, "outerlink");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->outerlink));
  if (err != mpack_ok) {
    return err;
  }
	
  mpack_node_t inode = mpack_node_map_cstr(node, "patient");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->patient));
  if (err != mpack_ok) {
    return err;
  }
	
  mpack_node_t inode = mpack_node_map_cstr(node, "estop");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->estop));
  if (err != mpack_ok) {
    return err;
  }

  return mpack_ok;
}
  
/**
 * Serialize the WowSoCool type into the format:
 *
 *    {
 *      "cool": <float32_t>,
 *			"lol": <float32_t>,
 *			"foo": <std::array<wow,2,3>>,
 *			"wow": <const char*>,
 *			"foo": <char[]>,
 *    }
 *
 * @param writer  mpack_writer_t to serialize the message into
 * @param data    A WowSoCool to serialize.
 */
static inline void mpack_serialize(mpack_writer_t *writer,
                                   WowSoCool const &data) {
  mpack_start_map(writer, 5);
  mpack_write_cstr(writer, "cool");
	mpack_serialize(writer, *(data.cool));
	mpack_write_cstr(writer, "lol");
	mpack_serialize(writer, *(data.lol));
	mpack_write_cstr(writer, "foo");
	mpack_serialize(writer, *(data.foo));
	mpack_write_cstr(writer, "wow");
	mpack_serialize(writer, *(data.wow));
	mpack_write_cstr(writer, "foo");
	mpack_serialize(writer, *(data.foo));
  mpack_finish_map(writer);
}

/**
 * Deserializes the raw msgpack format of a WowSoCool type into a struct:
 *
 *    {
 *      "cool": <float32_t>,
 *			"lol": <float32_t>,
 *			"foo": <std::array<wow,2,3>>,
 *			"wow": <const char*>,
 *			"foo": <char[]>,
 *    }
 *
 * @param node   mpack_node_t to deserialize with, points to a node on the
 *               msgpack tree.
 * @param item   A WowSoCool to deserialize into.
 */
mpack_error_t mpack_deserialize(mpack_node_t node,
                                WowSoCool *item) {
  assert(item != nullptr);
  if (mpack_node_map_count(node) != 5) {
    return mpack_error_invalid;
  }

  
  mpack_node_t inode = mpack_node_map_cstr(node, "cool");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->cool));
  if (err != mpack_ok) {
    return err;
  }
	
  mpack_node_t inode = mpack_node_map_cstr(node, "lol");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->lol));
  if (err != mpack_ok) {
    return err;
  }
	
  mpack_node_t inode = mpack_node_map_cstr(node, "foo");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->foo));
  if (err != mpack_ok) {
    return err;
  }
	
  mpack_node_t inode = mpack_node_map_cstr(node, "wow");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->wow));
  if (err != mpack_ok) {
    return err;
  }
	
  mpack_node_t inode = mpack_node_map_cstr(node, "foo");
  mpack_error_t err = mpack_node_error(inode);
  if (err != mpack_ok) {
    return err;
  }

  err = mpack_deserialize(inode, &(item->foo));
  if (err != mpack_ok) {
    return err;
  }

  return mpack_ok;
}
  
//[[[end]]]

int main() {
  int a;

  return 0;
}
