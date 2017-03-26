from .record import *
from .serde_registry import *
from .serdes import *
import clang.cindex as cl
from ctypes.util import find_library
import ccsyspath
import re


def get_clang_TranslationUnit(path="t.cpp", in_args=[], in_str="", options=0):
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

    # Make sure we are parsing as std c++11
    args = '-x c++ --std=c++11'.split()
    # Add the include files for the standard library.
    syspath = ccsyspath.system_include_paths('clang++')
    incargs = [b'-I' + inc for inc in syspath]
    # turn args into a list of args (in_args may contain more includes)
    args = args + incargs + in_args

    # Create a clang index to parse into
    index = cl.Index.create()

    unsaved_files = None
    # If we are parsing from a string instead
    if in_str:
        unsaved_files = [(path, in_str)]
    return index.parse(path, args=args, options=options,
                       unsaved_files=unsaved_files)


def get_current_scope(cursor):
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
    # Get the parent of the current cursor
    parent = cursor.lexical_parent
    # If the parent is a declartaion type then add it to the end of our scope
    # list otherwise return an empty list
    if (parent.kind.is_declaration()):
        return get_current_scope(parent) + [parent.spelling]
    else:
        return []


def find_serializable_types(tu, match_str="//\+serde\(([A-Za-z\s,_]*)\)"):
    """
    Iterate through all tokens in the current TranslationalUnit looking for comments
    which match the match_str. If the comment match look for the next struct or
    class declaration, start extracting the scope by looking at the lexical parents
    of the declaration. This will let you extract the name, then extract all of the
    fields.

    Parameters ::
        - tu: The TranslationalUnit to search over
        - match_str: The comment string to match.

    Returns ::
        - A List of Records.
    """
    match_types = [cl.CursorKind.STRUCT_DECL, cl.CursorKind.CLASS_DECL]

    tokens = tu.cursor.get_tokens()

    found = False
    serializables = []
    serdes = []
    # iterate through all tokens, looking for the match_str in a comment. If
    # found the name, and fields are extracted from the next struct or class
    # definition. After extracting these declaration the parser continues to
    # look for more Comment otkens matching match_str.
    for token in tokens:
        match = re.match(match_str, token.spelling)
        if found:
            cursor = cl.Cursor().from_location(tu, token.location)
            if cursor.kind in match_types:
                # Extract the name, and the scope of the cursor and join them
                # to for the full C++ name.
                name = "::".join(get_current_scope(cursor) + [cursor.spelling])
                # Extract all of the fields (including access_specifiers)
                fields = [RecordField(field.spelling, field.type.spelling,
                                      field.access_specifier.name) for field in cursor.type.get_fields()]
                serializables.append(Record(name, fields, serdes))
                # Start searching for more comments.
                found = False
                # Clear the list of registered serdes for this Record.
                serdes = []
        elif (token.kind == cl.TokenKind.COMMENT) and match:
            serdes = [x.strip() for x in match.groups()[0].split(",")]
            found = True  # Start looking for the struct/class declaration

    return serializables
