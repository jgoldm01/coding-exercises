Solution to the talko coding exercise

example execution of program:
	python wordChange.py start brain
	python concurentWordChange.py start brain

program takes in two 5 letter words as arguments and outputs the shortest 
path from one to the other by changing one letter to make another word that 
exists in the wordlist (of dictionary defined words). 

Data structures used are explained in the program itself. two solutions are
provided, one which uses no threads, and one which uses 4, to mimic the 4
cores of a quad-core cpu. 


Test cases: 
start brain
brain start
s q (will give an error message)
globs foxes
adobe allay
start ambit (no path between the two)