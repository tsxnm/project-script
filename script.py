#!/usr/local/bin/python

import sys
sys.path.append('..')
sys.path.append('../..')
import argparse
import utils
import networkx as nx
import numpy as np
from part1_utils import *
# from utils_sp18 import *
from student_utils_sp18 import *
# import planarity

# Function to create a test matrix.
def dummy_matrix():
    dummy_graph = np.array = ([[1  , 'x', 'x', 'x', 'x', 'x', 'x',   1],
                               ['x',   1,   1, 'x', 'x', 'x', 'x',   1],
                               ['x',   1,   1, 'x', 'x', 'x',   1,   1],
                               ['x', 'x', 'x',   1, 'x', 'x',   1,   1],
                               ['x', 'x', 'x', 'x',   1, 'x',   1,   1],
                               ['x', 'x', 'x', 'x', 'x',   1,   1,   1],
                               ['x', 'x',   1,   1, 'x',   1,   2, 'x'],
                               [1  ,   1,   1,   1,   1,   1, 'x', 100]])

    return dummy_graph


# Open file and write the adjancency matrix in it and then close it
def format_file(input_file, num_vertex, small_graph_dim) :
    file_object = open("input_file", "w")


    num_copies = num_vertex // small_graph_dim
    total_nodes = num_copies * small_graph_dim
    file_object.write(str(total_nodes) + "\n")

    #func that takes in tptal nodes and outputs correct names
    kingdom_names = names(small_graph_dim, num_copies)
    for kingdom_name in kingdom_names:
        file_object.write(str(kingdom_name) + " ")

    file_object.write("\n")
    file_object.write("1") #starting node will always be 1 (i think lol)
    matrix = dummy_matrix()

    #note this is list of lists
    output_matrix = matrix_join(matrix, num_copies)
    #print(output_matrix)

    for i in range(len(output_matrix)):
        file_object.write("\n")
        for j in range(len(output_matrix)):
            node = output_matrix[i][j]
            file_object.write(str(node) + " ")



    # CLOSE FILE AFTER OPENING
    file_object.close()

#naming kingdoms
def names(input_matrix_size, num_copies):
    kname=97
    retlist = []
    for i in range(num_copies):
        for j in range(0,input_matrix_size):
            if i == 0:
                name = chr(kname)
            else:
                name = chr(kname) + str(i)
            retlist.append(name)
            kname += 1
        kname = 97
    return retlist

# Main function
def main():
    parser = argparse.ArgumentParser(description="Parsing nodes...")
    parser.add_argument('integer', type=int)
    vertex = int(''.join(sys.argv[1:2]))

    format_file("input.txt", vertex, 8)


# Keep for script
if __name__ == '__main__':
    main()
