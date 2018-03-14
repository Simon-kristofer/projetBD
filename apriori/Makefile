objects = aprioritest.o Item.o AprioriSets.o Data.o
Cpp = g++
flags = -O6 -Wall

apriori : $(objects) Makefile
	$(Cpp) $(flags) $(objects) -o apriori

aprioritest.o : aprioritest.cpp AprioriSets.h
	$(Cpp) -c $(flags) aprioritest.cpp

Item.o : Item.cpp Item.h
	$(Cpp) -c $(flags) Item.cpp

AprioriSets.o : AprioriSets.cpp AprioriSets.h Data.h Item.h
	$(Cpp) -c $(flags) AprioriSets.cpp

Data.o : Data.cpp Data.h
	$(Cpp) -c $(flags) Data.cpp

clean :
	rm -f $(objects) apriori

