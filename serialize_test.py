#!python
from cpp_serde_gen import *

tu = get_clang_TranslationUnit("test.cpp")
serializables = find_serializable_types(tu)
for serializable in serializables:
    print(serializable)
