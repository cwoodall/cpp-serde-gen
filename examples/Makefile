CPP="g++"
CPP_FLAGS="-std=c++11"
COG="cog.py"
COG_FLAGS="-d"

example-01: example-01.cpp
	$(CPP) $(CPPFLAGS) -o $@ $<

%.cpp: %.cpp.cog
	$(COG) $(COG_FLAGS) -o $@ $< 

clean:
	rm example-01 example-01.cpp
