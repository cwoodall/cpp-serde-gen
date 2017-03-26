from .. import *
import clang.cindex as cl
import unittest
from ..serdes.printf import *
from ..serdes.mpack import *
from ..serde_registry import *
# Get the matching clang library file (.so)
cl.Config.set_library_file(find_library('clang-3.8'))

UUT_FILE_ONE_H = """
#include <iostream>
#include <array>
#include <vector>
#include <stdint.h>

typedef float float32_t;

//+serde(printf, mpack)
struct Foo {
  uint8_t bar1; ///<
  uint8_t bar2;  ///<
  uint8_t bar3;    ///<
  uint8_t bar4;      ///<
};

namespace outer_test {

//+serde(printf)
struct InNS {
  float32_t param;
};

namespace test {

//+serde(printf)
struct DeepNS {
  float32_t param;
};

//+serde(printf)
class MyClass {
public:
  //+serde(printf, mpack)
  struct InMyClass {
    int param;
  };
  int public_param;
protected:
  int protected_param;
private:
  int private_param;
};

}
}

//+serde(A, B)
struct MoreComplicatedTypes {
  std::array<int, 2> my_std_array;
  const char * my_cstr;
  int my_c_array[10];
  std::vector<int> my_vec;
}

int main() {
  int a;

  return 0;
}
"""


class TestFindSerializableTypes(unittest.TestCase):

    def setUp(self):
        self.tu = get_clang_TranslationUnit("temp.h", in_str=UUT_FILE_ONE_H)
        self.serializables = find_serializable_types(self.tu)
        self.registery = SerdeRegistry(
            [PrintfSerdeGenerator(), PrintfSerdeGenerator("A"), PrintfSerdeGenerator("B"),
             MpackSerdeGenerator()])

    def test_find_struct_Foo(self):
        assert(self.serializables[0].name == "Foo")
        assert(self.serializables[0].fields[0]
               == RecordField("bar1", "uint8_t"))
        assert(self.serializables[0].fields[1]
               == RecordField("bar2", "uint8_t"))
        assert(self.serializables[0].fields[2]
               == RecordField("bar3", "uint8_t"))
        assert(self.serializables[0].fields[3]
               == RecordField("bar4", "uint8_t"))

    def test_find_struct_InNS(self):
        assert(self.serializables[1].name == "outer_test::InNS")
        assert(self.serializables[1].fields[0] ==
               RecordField("param", "float32_t"))

    def test_find_struct_DeepNS(self):
        assert(self.serializables[2].name == "outer_test::test::DeepNS")
        assert(self.serializables[2].fields[0] ==
               RecordField("param", "float32_t"))

    def test_find_struct_MyClass(self):
        assert(self.serializables[3].name == "outer_test::test::MyClass")
        assert(self.serializables[3].fields[0] ==
               RecordField("public_param", "int", "PUBLIC"))
        assert(self.serializables[3].fields[1] == RecordField(
            "protected_param", "int", "PROTECTED"))
        assert(self.serializables[3].fields[2] == RecordField(
            "private_param", "int", "PRIVATE"))

    def test_find_struct_InMyClass(self):
        assert(self.serializables[4].name ==
               "outer_test::test::MyClass::InMyClass")
        assert(self.serializables[4].serdes[0] == "printf")
        assert(self.serializables[4].serdes[1] == "mpack")
        assert(self.serializables[4].fields[0] ==
               RecordField("param", "int", "PUBLIC"))

    def test_find_struct_MoreComplicatedTypes(self):
        assert(self.serializables[5].name == "MoreComplicatedTypes")
        assert(self.serializables[5].serdes[0] == "A")
        assert(self.serializables[5].serdes[1] == "B")
        assert(self.serializables[5].fields[0] == RecordField(
            "my_std_array", "std::array<int, 2>", "PUBLIC"))
        assert(self.serializables[5].fields[1] == RecordField(
            "my_cstr", "const char *", "PUBLIC"))
        assert(self.serializables[5].fields[2] == RecordField(
            "my_c_array", "int [10]", "PUBLIC"))
        assert(self.serializables[5].fields[3] == RecordField(
            "my_vec", "std::vector<int>", "PUBLIC"))
