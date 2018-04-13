import numpy as np

CONNECTOR_WEIGHT = 'FILL_ME_IN'

"""
input_adj: adjacency matrix of smaller graph; dimension nxn np.array
num_copies: number of times to copy this graph to compose the final graph;
	copies will be linked by edges of weight CONNECTOR_WEIGHT. By default,
	the connector will go from the last node of one copy to the first node of
	the next
returns output matrix, which is a list of lists representing the new
	adjacency matrix; it will be dimension (n*num_copies)x(n*num_copies)
"""
def matrix_join(input_adj, num_copies):
	input_matrix = input_adj.tolist()
	n = len(input_matrix)
	
	output_dim = n*num_copies
	output_matrix = [['x']*output_dim for i in range(output_dim)]
	counter = 0
	#first, add in input matrices on diagonal
	while counter < output_dim:
		for i in range(n):
			for j in range(n):
				output_matrix[counter+i][counter+j] = input_matrix[i][j]
		counter += n

	x_counter = 0
	y_counter = 0
	#now add in connector weights
	while x_counter < output_dim:
		while y_counter < output_dim:
			if x_counter%n == 0 and y_counter + 1 == x_counter:
				output_matrix[x_counter][y_counter] = CONNECTOR_WEIGHT
			elif y_counter%n == 0 and x_counter + 1 == y_counter:
				output_matrix[x_counter][y_counter] = CONNECTOR_WEIGHT
			y_counter += 1
		y_counter = 0
		x_counter += 1

	return output_matrix
			