'''
	Contestants should only modify this file and leave other files as it is.

	This code contains the AI logic of pacman and ghost movement

	For both pacman and ghost the following convention should be used

	0 : go UP
	1 : go DOWN
	2 : go LEFT
	3 : go RIGHT

	input :
		both functions receives the grid object which contains 
			gridLayout = the grid layout as a numpy array
			rows = number of rows
			columns = number of columns 

		Also each function receives a tuple named position which represents
		the postion of the pacman or ghost

			1st element denotes the row number in grid 
			2nd element denotes the column number in grid


	output:
		return one of these four values from both the functions below 
'''

import numpy as np

def pacmanMove(grid,pacmanPostion,ghostPosition,enemyPacmanPosition,enemyGhostPosition):

	'''
		Inputs: 
			grid = Grid object which contains 
				gridLayout = the grid layout as a numpy array
				rows = number of rows
				columns = number of columns 

			pacmanPosition = position of our pacman, a tuple
				1st element = row number
				2nd element = column number

			ghostPosition = position of our ghost, a tuple
				1st element = row number
				2nd element = column number
			
			enemyPacmanPosition = position of enemy pacman, a tuple
				1st element = row number
				2nd element = column number

			enemyGhostPosition = position of enemy ghost, a tuple
				1st element = row number
				2nd element = column number

		Output:
			pacman move

			return
				0 : go UP
				1 : go DOWN
				2 : go LEFT
				3 : go RIGHT
	'''

	return int(np.random.rand()*4)

def ghostMove(grid,pacmanPostion,ghostPosition,enemyPacmanPosition,enemyGhostPosition):

	'''
		Inputs: 
			grid = Grid object which contains 
				gridLayout = the grid layout as a numpy array
				rows = number of rows
				columns = number of columns 

			pacmanPosition = position of our pacman, a tuple
				1st element = row number
				2nd element = column number

			ghostPosition = position of our ghost, a tuple
				1st element = row number
				2nd element = column number
			
			enemyPacmanPosition = position of enemy pacman, a tuple
				1st element = row number
				2nd element = column number

			enemyGhostPosition = position of enemy ghost, a tuple
				1st element = row number
				2nd element = column number

		Output:
			pacman move

			return
				0 : go UP
				1 : go DOWN
				2 : go LEFT
				3 : go RIGHT
	'''

	return int(np.random.rand()*4)