CPP="g++"
CPP_FLAGS="-std=c++11"
COG="cog.py"
COG_FLAGS="-d"

all: example-01.o example-02.o

.PRECIOUS: %.cpp

%.o: %.cpp
	$(CPP) $(CPPFLAGS) -o $@ $<

%.cpp: %.cpp.cog
	$(COG) $(COG_FLAGS) -o $@ $<

clean:
	rm *.o *.cpp
