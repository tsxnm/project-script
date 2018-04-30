import os
import sys
sys.path.append('..')
sys.path.append('../..')
import numpy as np
import random
import argparse
import utils
import networkx as nxj
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
    #convert to numpy matrix
    np_matrix = np.array(adjacency_matrix)

    #convert numpy to nx graphe
    G = nx.from_numpy_matrix(np_matrix)
    clusters = k_clusters(k, dist_dict, starting_kingdom, list_of_kingdom_names) #list of lists representing clusters returned here


    #use tas mst solver on each cluster and output path, conquest
    pathlist1=[]
    pathlist2=[]
    conquests = {}
    for cluster in clusters:
        x = mst_cluster_solver(cluster, adjacency_matrix, list_of_kingdom_names) #returns path, conquest
        pathlist1.append(x[0])

    pathlist2 += pathlist1[0]    

    for i in range len(pathlist1)-1:
        curr_path = pathlist1[i]
        next = pathlist1[i+1]
        connector = shortest_connector(curr_path[len(curr_path)-1], next[0], G)
        adjustedConnector = connector[1:len(connector)-1]
        pathlist2 += (adjustedConnector)
        pathlist2 += next
    lastpath= pathlist1[len(pathlist1)-1]
    connector = shortest_connector(lastpath[len(lastpath)-1], starting_kingdom, G)


        #networkx cluster shortest paths https://networkx.github.io/documentation/networkx-1.10/reference/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html
        #cluster shortest path from a to b
        #min over adjacency((i,j) + (j,j))
        #when making final full path remove first and last nodes
    def shortest_connector(start_node, end_node, G):
    """"
    inputs: start node, end node, full adjacency matrix
    returns shortest path connecting start and end node
    [[a, b, c], [d, e, f]]
    shortest_connector(c, d) --> [c, b, d]
    """
    return nx.shortest_path(G, source = start_node, target = end_node)









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



"""
Returns the path and conquest as list. Params:
    @list_of_subkingdoms: list of kingdoms that are in our subcluster
    @adjacency_matrix: th matrix representation of the graph of the subcluster

Converts adjacency matrix into a networkx graph. Creates a MST from the graph and extracts
the nodes of that MST and places them in a list called list_mst_nodes. For
each node in the MST, we conquer it if it has not been conqured and nor
surrendered. We append it to conquer and path. Next, we check if it has any neighbors
and if they do, then we append all neighbors that have not already surrendered
(placed in path) to path. Return path and conquer as lists.
"""
def mst_cluster_solver(list_of_subkingdoms, adjacency_matrix):
    #convert to numpy matrix
    np_matrix = np.array(adjacency_matrix)

    #convert numpy to nx graph
    G = nx.from_numpy_matrix(np_matrix)
    G_mst = nx.minimum_spanning_tree(G)

    # we can use neighbors on G to find the connected nodes of the MST
    list_mst_nodes = list(G.nodes) #this is the conquered


    # CREATE PATH AND CONQUERED #
    # path: kingdoms we travel through including ones that we do not conquer
    # conquest: kingdoms we explicitly conquer
    path = []
    conquest = []
    for n in list_mst_nodes:
        #if n in path, do not put in conquered
        # else put in conquered and path
        if n not in path:
            path.append(n)
            conquest.append(n)
            neighbors = [G.neighbors(n)]
            for i in neighbors:
                if i not in path:
                    path.append(i)

        # put n's neigbors in path if not in path

    return path, conquest

"""
Returns the adjacency list of a subcluster. Use this to create the
asjacency matrix needed for mst_cluster_solver. Params: 
    @list_of_kingdom_names: list of all kingdom names in graph as a list
    @subcluster: subcluster of kingdom names we want to solve as a list
    @adjacency_matrix: matrix representation of the entire graph as a list of lists

The function uses the subcluster list to identify which indices of the list_of_kingdom_names
they correspond to and place them in a list called kingdom_indices. Given kingdom_indices,
we loop through each element and add all relevent edges and costs from the full
adjacency matrix and place them in mini_matrix and return it as list of lists.
"""
def mini_adj_list(list_of_kingdom_names, subcluster, adjacency_matrix):

    #find then indices of the kingdom names and put them into a list
    kingdom_indices = [len(subcluster)]
    counter = 0
    for n in subcluster:
        for i in range(len(list_of_kingdom_names)):
            if list_of_kingdom_names[i] == n:
                kingdom_indices[counter] = list_of_kingdom_names[i]
                counter = counter + 1

    #given indices, extract edges from them
    mini_matrix = [[]*len(kingdom_indices)]
    for i in kingdom_indices: #this gives the index value
        #we want to index into ith row of adj matrix
        for j in kingdom_indices:
            a = adjacency_matrix[i][j]
            mini_matrix[i].append(a)

    return mini_matrix

def replace_xs(adjacency_matrix):
    """
    TODO: make a function that replaces "x"s with shortest path distance to that node
    use this from networkx: https://networkx.github.io/documentation/latest/reference/algorithms/shortest_paths.html
    """

    #replace x in adj matrix with 0
    copy = adjacency_matrix.deepcopy()
    #convert to numpy matrix
    np_matrix = np.array(adjacency_matrix)

    #convert numpy to nx graph
    G = nx.from_numpy_matrix(np_matrix)


    for i in range(NUM_VERTICES):
        for j in range(NUM_VERTICES):
            if adjacency_matrix[i][j] == 'x':
                # find the shortest path from node[i][i] to node[i][j]


                #  quick note: the shortest path len always is one less than the
                #  optimal answer because that is just how networkx works according
                #  to the documents online
                shortest = 1 + nx.shortest_path_length(G, adjacency_matrix[i][i], adjacency_matrix[i][j])

                copy[i][j] = shortest

    SHORTEST_PATHS_MATRIX = copy
    return SHORTEST_PATHS_MATRIX

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
    output_file = 'test.txt'
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
