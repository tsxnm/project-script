def is_symmetric(list_of_lists):
	for i in range(len(list_of_lists)):
		for j in range(len(list_of_lists)):
			if list_of_lists[i][j] != list_of_lists[j][i]:
				print("not symmetric at " +str(i)+ " "+str(j))
				print("This is regular matrix: " + str(list_of_lists[i][j]))
				print("This is the transpose: " + str(list_of_lists[j][i]) + "\n")
