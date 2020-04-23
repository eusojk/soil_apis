# makefile for water balance model for gfortran
# 2019-12-28 by Honda
FC = gfortran
FCFLAGS =  -ffree-line-length-none -O

# executable name
PROGRAM = dotSolAPI2.a

# compile and link at once to generate the exeutable 
all: $(PROGRAM)

SRCs = dotSolAPIMain.f90  inpoly.f90  What_tex.f90  What_tex_4HC.f90

$(PROGRAM): $(SRCs)
	$(FC) $(FCFLAGS) -o $@ $^

clean:
	rm -f *.o dotSolAPI2.a

clean-all:
	rm -f *.o $(PROGRAM)

# execute the program with test parameter
test: $(PROGRAM) $(PARM_FILE_TEST)
	./$(PROGRAM) $(PARM_FILE_TEST)

# a parameter fiile for testing
PARM_FILE_TEST = param_srisaket.txt


