import os
import sys
sys.path.append('..')
sys.path.append('../..')
import numpy as np
import random
import argparse
import utils
from student_utils_sp18 import *

"""
======================================================================
  Complete the following function.
======================================================================
"""


def solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=[]):
    """
    Write your algorithm here.
    Input:
        list_of_kingdom_names: An list of kingdom names such that node i of the graph corresponds to name index i in the list
        starting_kingdom: The name of the starting kingdom for the walk
        adjacency_matrix: The adjacency matrix from the input file

    Output:
        Return 2 things. The first is a list of kingdoms representing the walk, and the second is the set of kingdoms that are conquered
    """
    #split into k clusters
    #string together the paths aka find min dist between start of one and end of another
    k = random.randint(5, list_of_kingdom_names)
    dist_dict = distances(list_of_kingdom_names, adjacency_matrix)
    clusters = k_clusters(k, dist_dict, starting_kingdom, list_of_kingdom_names) #list of lists representing clusters returned here

    #use tas mst solver on each cluster and output path, conquest
    pathlist=[]
    conquests = {}
    for cluster in clusters:
        x = mst_cluster_solver(cluster, adjacency_matrix, list_of_kingdom_names) #returns path, conquest
        pathlist.append(x[0])
    pathlist = [, , ]







"""
TODO: implement k-clusters using this distance (done)
TODO: determine node would be best to determine as start center; for now, just use start node
TODO: write algorithm to conquer mini-clusters using MSTs
"""

def k_clusters(k, dist_dict, start, list_of_kingdom_names):
    """returns list of lists, representing clusters"""
    curr_node = start
    centers = [start]
    while len(centers) < k:
        cum_dists = [0]*len(list_of_kingdom_names)
        for center in centers:
            dists = dist_dict[center]
            for i in range in len(dists):
                cum_dists[i] += dists[i]
        max_cum_dist_ind = 0
        max_cum_dist = 0
        for i in range(len(cum_dists)):
            if cum_dists[i] > max_cum_dist:
                max_cum_dist = cum_dists[i]
                max_cum_dist_ind = i
        centers.append(list_of_kingdom_names[max_cum_dist_ind])
    clusters = {}
    for kingdom in dist_dict:
        if kingdom not in centers:
            closest_dist = sys.maxsize
            closest_center = centers[0]
            dists = dist_dict[kingdom]
            for center in centers:
                c_ind = list_of_kingdom_names.index(center)
                if dists[c_ind] < closest_dist:
                    closest_dist = dists[c_ind]
                    closest_center = center
            if closest_center in clusters:
                clusters[closest_center].append(kingdom)
            else:
                clusters[closest_center] = [kingdom]
    cluster_list = map(list, clusters.items())
    return list(cluster_list)

def replace_xs(adjacency_matrix):
    """
    TODO: make a function that replaces "x"s with shortest path distance to that node
    use this from networkx: https://networkx.github.io/documentation/latest/reference/algorithms/shortest_paths.html
    """
    #implement here

def distances(list_of_kingdom_names, adjacency_matrix):
    """
    input: list of kingdom names; adjacency matrix
    output: dictionary mapping kingdom name to array representing distances to other kingdoms 
    """
    x_replaced_adj = replace_xs(adjacency_matrix)
    adj_list = x_replaced_adj.tolist()
    ret_dict = {}
    kingdom_ind = 0
    for kingdom_ind in range(len(list_of_kingdom_names)):
        curr_kingdom_list = adj_list[kingdom_ind]
        curr_kingdom_list[kingdom_ind] = 0
        ret_dict[list_of_kingdom_names[kingdom_ind]] = curr_kingdom_list
        kingdom_ind += 1
    return ret_dict



"""
======================================================================
   No need to change any code below this line
======================================================================
"""


def solve_from_file(input_file, output_directory, params=[]):
    print('Processing', input_file)
    
    input_data = utils.read_file(input_file)
    number_of_kingdoms, list_of_kingdom_names, starting_kingdom, adjacency_matrix = data_parser(input_data)
    closed_walk, conquered_kingdoms = solve(list_of_kingdom_names, starting_kingdom, adjacency_matrix, params=params)

    basename, filename = os.path.split(input_file)
    output_filename = utils.input_to_output(filename)
    output_file = f'{output_directory}/{output_filename}'
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    utils.write_data_to_file(output_file, closed_walk, ' ')
    utils.write_to_file(output_file, '\n', append=True)
    utils.write_data_to_file(output_file, conquered_kingdoms, ' ', append=True)


def solve_all(input_directory, output_directory, params=[]):
    input_files = utils.get_files_with_extension(input_directory, 'in')

    for input_file in input_files:
        solve_from_file(input_file, output_directory, params=params)


if __name__=="__main__":
    parser = argparse.ArgumentParser(description='Parsing arguments')
    parser.add_argument('--all', action='store_true', help='If specified, the solver is run on all files in the input directory. Else, it is run on just the given input file')
    parser.add_argument('input', type=str, help='The path to the input file or directory')
    parser.add_argument('output_directory', type=str, nargs='?', default='.', help='The path to the directory where the output should be written')
    parser.add_argument('params', nargs=argparse.REMAINDER, help='Extra arguments passed in')
    args = parser.parse_args()
    output_directory = args.output_directory
    if args.all:
        input_directory = args.input
        solve_all(input_directory, output_directory, params=args.params)
    else:
        input_file = args.input
        solve_from_file(input_file, output_directory, params=args.params)
