import clang.cindex as cl
import logging
from ctypes.util import find_library
import ccsyspath

logging.basicConfig()
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


"""
Get the TranslationalUnit for the input fule listed:

Parameters ::
    - path: The path of the file to parse (not read if in_str is set)
    - in_args: additional arguments to pass to clang
    - in_str: input string to parse instead of the file path.
    - options: clang.cindex.Options

Returns ::
    - A TranslationalUnits
"""
def get_clang_TranslationUnit(path="tmp.cpp", in_args=[], in_str="", options=0):
    # Get the matching clang library file (.so)
    cl.Config.set_library_file(find_library('clang-3.8'))

    # Make sure we are parsing as std c++11
    args    = '-x c++ --std=c++11'.split()
    # Add the include files for the standard library.
    syspath = ccsyspath.system_include_paths('clang++')
    incargs = [ b'-I' + inc for inc in syspath ]
    # turn args into a list of args (in_args may contain more includes)
    args    = args + incargs + in_args

    # Create a clang index to parse into
    index = cl.Index.create()

    unsaved_files = None
    # If we are parsing from a string instead
    if in_str:
        unsaved_files = [(path, in_str)]
    return index.parse(path, args=args, options=options,
                       unsaved_files=unsaved_files)

"""
Get the current scope of the current cursor.

For example:
```
namespace A {
namespace B {

class C {
    <CURSOR IS IN HERE>
};

}
}
```

will return: ["A", "B", "C"] and can be joined to be "A::B::C"

Parameters ::
  - cursor: A clang.cindex.Cursor to loop for declaration parents of.

Returns ::
  - A list of names of the scopes.
"""
def get_current_scope(cursor):
    # Get the parent of the current cursor
    parent = cursor.lexical_parent
    # If the parent is a declartaion type then add it to the end of our scope
    # list otherwise return an empty list
    if (parent.kind.is_declaration()):
        return get_current_scope(parent) + [parent.spelling]
    else:
        return []

class SerializableField(object):
    def __init__(self, name, t="void", access=cl.AccessSpecifier.PUBLIC):
        self.name = name
        self.type = t
        self.access = access

    def __str__(self):
        return "{0}, {1}, {2}".format(self.name, self.type, self.access)

class SerializableType(object):
    def __init__(self, name, fields=[]):
        self.name = name
        self.fields = fields

    def append_field(self, field):
        self.fields.append(field)

    def __str__(self):
        return "name: {0}\nfields: {1}".format(self.name, [str(field) for field in self.fields])

"""
"""
def find_serializable_types(tu, match_str="//+mpack-serializable"):
    tokens = tu.cursor.get_tokens()

    found = False
    serializables = []
    # iterate through all tokens, looking for the match_str in a comment. If
    # found the name, and fields are extracted from the next struct or class
    # definition. After extracting these declaration the parser continues to
    # look for more Comment otkens matching match_str.
    for token in tokens:
        if found:
          cursor = cl.Cursor().from_location(tu, token.location)
          if cursor.kind in [cl.CursorKind.STRUCT_DECL, cl.CursorKind.CLASS_DECL]:
              name = "::".join(get_current_scope(cursor) + [cursor.spelling])
              fields = [SerializableField(field.spelling, field.type.spelling, field.access_specifier) for field in cursor.type.get_fields()]
              s = SerializableType(name, fields)
              serializables.append(s)
              found = False
        elif (token.kind == cl.TokenKind.COMMENT) and (token.spelling == match_str):
            found = True

    return serializables

tu = get_clang_TranslationUnit("test.cpp")
serializables = find_serializable_types(tu)
for serializable in serializables:
    print(serializable)
