#include <iostream>
#include <array>
#include <stdint.h>

typedef float float32_t;
//+mpack-serializable
struct GroupStatus {
  uint8_t handedness; ///<
  uint8_t outerlink;  ///<
  uint8_t patient;    ///<
  uint8_t estop;      ///<
};

namespace outer_test {
namespace test {

//+mpack-serializable
struct InNS {
  float32_t cool; ///<
  float32_t lol;
  std::array<int, 2> foo;
  const char *wow;
  char bar[10];
};

//+mpack-serializable
class MyClass {
public:
  //+mpack-serializable
  struct InClass {
    float32_t cool; ///<
  };
private:
  int a;
};

}
}

//+mpack-serializable
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
