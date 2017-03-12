from .. import *
import clang.cindex as cl

UUT_FILE_ONE_H = """
#include <iostream>
#include <array>
#include <stdint.h>

typedef float float32_t;
//+serde()
struct GroupStatus {
  uint8_t handedness; ///<
  uint8_t outerlink;  ///<
  uint8_t patient;    ///<
  uint8_t estop;      ///<
};

namespace outer_test {
namespace test {

//+serde()
struct InNS {
  float32_t cool; ///<
  float32_t lol;
  std::array<int, 2> foo;
  const char *wow;
  char bar[10];
};

//+serde()
class MyClass {
public:
  //+serde(mpack)
  struct InClass {
    float32_t cool; ///<
  };
private:
  int a;
};

}
}

//+serde(A, B)
struct OutOfNS {
  uint8_t handedness; ///<
  uint8_t outerlink;  ///<
  uint8_t patient;    ///<
  uint8_t estop;      ///<
};

int main() {
  int a;

  return 0;
}
"""

def test_serializable_types():
    tu = get_clang_TranslationUnit("temp.h", in_str=UUT_FILE_ONE_H)
    serializables = find_serializable_types(tu)
    for serializable in serializables:
        print(serializable)

    assert(False)
