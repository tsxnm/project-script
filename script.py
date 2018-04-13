#!/usr/local/bin/python

import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import networkx as nx
import numpy as np
# from utils_sp18 import *
from student_utils_sp18 import *
# import planarity

# Function to algorithmically write matrix

# Open file and write the adjancency matrix in it and then close it
def test(input_file) :
    file_object = open("input_file", "w")

    ####### REPLACE TWO LINES WITH ACTUAL MATRIX CODE ########
    file_object.write("hello world\n")
    file_object.write("this is our new text file")
    ##########################################################



    # CLOSE FILE AFTER OPENING
    file_object.close()



# Main function
def main():
    test("input.txt")


# Keep for script
if __name__ == '__main__':
    main()
