# cpp-serde-gen:
> Use Python To Parse The C++ AST and Generate Serializing Functions

**Table of Contents**:

<!-- TOC depthFrom:2 depthTo:6 withLinks:1 updateOnSave:1 orderedList:0 -->

- [Installation](#installation)
- [Usage](#usage)
	- [Running The Examples](#running-the-examples)
	- [Running The Tests](#running-the-tests)
	- [How To Mark A Struct For `serde`](#how-to-mark-a-struct-for-serde)
	- [Writing a Serializer](#writing-a-serializer)
- [Resources](#resources)

<!-- /TOC -->

## Installation

This library requires:

- Python 2.7 and is not tested with Python 3.0.
- pip (for installing dependencies)
- libclang 3.8

To install:

```sh
$ git clone https://github.com/cwoodall/cpp-serde-gen.git
$ cd cpp-serde-gen
$ sudo pip install .
```

## Usage
### Running The Examples

```sh
$ cd examples
$ make
$ ./example-01.o

Foo:
	bar1: 222
	bar2: 3.141590
	bar3: [1.000000, 2.000000, 3.000000, 5.000000]
Baz::MyStruct:
	a: 1
	b: [2.000000, 3.000000, 4.000000, 5.000000]
```

After running make you can look at the `.cpp` files generated by the `.cpp.cog`
files. `cog` is a way of writing python inline in `C`/`C++` and then embedding
the results. You can also run the examples.

Description of examples:

- [`example-01`][example-01]: Run the example `printf` serializer, on two structs, one of
                which is in a namespace.
- [`example-02`][example-02]: Create and register a custom serializer called `my_new`.

[example-01]: examples/example-01.cpp.cog
[example-02]: examples/example-02.cpp.cog

### Running The Tests

```sh
$ nosetests
```

### How To Mark A Struct For `serde`

To run the generators you mark the structs with a comment of the form:
`//+serde(<serializer_keys>)`, where `<serializer_keys>` is a comma seperated
list of registered serializers you want to run the generation code of.

So for example you can make a `struct Foo` and mark it for the `printf`
serializer, which just prints the struct (from
`examples/example-01.cpp.cog`):

```c++
//+serde(printf)
struct Foo {
  uint8_t bar1; ///<
  float bar2; ///<
  std::array<float, 4> bar3; ///<
};
```

If we then run the following code inline using cog
(see `examples/example-01.cpp.cog`):

```py
from cpp_serde_gen import *

tu = get_clang_TranslationUnit(cog.inFile)
serializables = find_serializable_types(tu)
registery = SerdeRegistry([PrintfSerdeGenerator()])

for serializable in serializables:
  for key in serializable.serdes:
    try:
      cog.outl(registery.generate_serialize(key, serializable))
      cog.outl()
    except Exception as e:
      cog.msg("Could not serialize {}".format(serializable.name))

    try:
      cog.outl(registery.generate_deserialize(key, serializable))
      cog.outl()
    except:
      cog.msg("Could not deserialize {}".format(serializable.name))
```

This will generate the following code. Note that the `printf` serializser
requires that all of the `struct`'s field types have a `printf_serialize`
function written for them, this is a flexible method since you can embed
complicated types inside of one another:

```c++
bool printf_serialize(Foo const & data) {
	printf("Foo:");
	printf("\n\tbar1: ");
	printf_serialize(data.bar1);
	printf("\n\tbar2: ");
	printf_serialize(data.bar2);
	printf("\n\tbar3: ");
	printf_serialize(data.bar3);
	printf("\n");
	return true;
}
```

A shorthand method of doing this is also provided, the following code will
achieve the same goal:

```python
from cpp_serde_gen import serdes, generate_serde_code

cog.outl(generate_serde_code(cog.inFile, [PrintfSerdeGenerator()]))
```

### Writing a Serializer

Writing a new serializer is rather easy, we need to inherit from
`GenericSerdeGenerator` and implement `generate_serialize(record)` and
`generate_deserialize(record)`, which each take a `Record` type.

So for example we can implement `MyNewSerializer` which uses the serde
key `my_new`:

```py
from .generic import GenericSerdeGenerator
from textwrap import dedent


class MyNewSerializer(GenericSerdeGenerator):

    def __init__(self, key="my_new"):
        GenericSerdeGenerator.__init__(self, key)

    def generate_serialize(self, record):
        return dedent("""\
void my_new_serializer({0} const &data) {{ return; }}
""".format(record.name))

    def generate_deserialize(self, record):
        return dedent("""\
void my_new_deserializer({0} *data) {{ return; }}
""".format(record.name))
```

Which will generate (see `examples/example-02`):

```c++
void my_new_serializer(Foo const &data) { return; }
void my_new_deserializer(Foo *data) { return; }
```

## Resources

- http://eli.thegreenplace.net/2011/07/03/parsing-c-in-python-with-clang
- https://nedbatchelder.com/code/cog/
- https://clang.llvm.org/doxygen/group__CINDEX.html
- https://github.com/llvm-mirror/clang/blob/master/bindings/python/clang/cindex.py
- http://stackoverflow.com/questions/19079070/retrieving-comments-using-python-libclang
- http://blog.glehmann.net/2014/12/29/Playing-with-libclang/
- https://www.fun4jimmy.com/2013/05/01/finding-all-includes-in-a-file-using-libclang-and-python.html
- http://stackoverflow.com/questions/37098725/parsing-with-libclang-unable-to-parse-certain-tokens-python-in-windows/37100397
