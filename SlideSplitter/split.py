#!/usr/bin/env python
from splithalfh import splithalfh
from splitquarterhor import splitquarterhor
from splitquartervert import splitquartervert
print(20*"=")
print("Quick PDF Splitter for Slides")
print(20*"=")
print("\n")
print("How do your slides look?")
print(
"+-------+  +-------+  +-------+\n|   1   |  | 1 | 2 |  | 1 | 3 |\n|-------|  |---+---|  |---+---|\n|   2   |  | 3 | 4 |  | 2 | 4 |\n+-------+  +-------+  +-------+")
print("   (1)        (2)        (3)")
mode = input("Insert a number here or 'a' to abort: ")
if mode not in ["a", "1", "2", "3"]:
    print("Invalid mode, aborting!")
    quit()
if mode == "a":
    print("Bye!")
    quit()
else:
    filename = input("Insert the file name (without .pdf): ")
    if mode == "1":
        splithalfh(filename)
    elif mode == "2":
        splitquarterhor(filename)
    elif mode == "3":
        splitquartervert(filename)
