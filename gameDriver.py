import time 
import numpy as np
from Player.teamCode import pacmanMove as player1Pacman
from Player.teamCode import ghostMove as player1Ghost
from Adversary.teamCode import pacmanMove as player2Pacman
from Adversary.teamCode import ghostMove as player2Ghost
import pygame 

UNIT = 20

black = (0,0,0)
white = (255,255,255)
blue = (51, 102, 255)
team1=(255, 204, 0)
team2=(230, 0, 172)

coin = pygame.transform.scale( pygame.image.load('img/coin.gif') , (UNIT-5,UNIT-5) )
power = pygame.transform.scale( pygame.image.load('img/power.png') , (UNIT-5,UNIT-5) )

class Grid(object):

	'''
		General class of grid objects
		Contains information about the grid
	'''

	def __init__(self,gridLayout,rows,columns):

		self.gridLayout = gridLayout
		self.rows = rows 
		self.columns = columns

	def randomSpawn(self,p=0.7):

		if(np.random.rand()>p):

			row = int(np.random.rand()*self.rows)
			column = int(np.random.rand()*self.columns)

			if(self.gridLayout[row][column]=='.'):

				self.gridLayout[row][column]='o'

	def validPosition(self,x,y):
	
		return (0<=x and x<self.rows) and (0<=y and y<self.columns) and (self.gridLayout[x][y] != '#')

	def __str__(self):

		printable = ''

		for i in self.gridLayout:

			for j in i:

				printable=printable+j[0]

		return printable

	def show(self,player1PacmanPos,player1GhostPos,player2PacmanPos,player2GhostPos,scoreP1,timePacmanP1,timeGhostP1,scoreP2,timePacmanP2,timeGhostP2):

		leftOffset = 300
		topOffset = 0

		screen.fill(black)

		printable =''
		for i in range(self.rows):
			for j in range(self.columns):
				
				if(self.gridLayout[i][j]=='#'):

					pygame.draw.rect(screen,blue,(j*UNIT+leftOffset,i*UNIT+topOffset,UNIT,UNIT))

				elif(self.gridLayout[i][j]=='o'):

					screen.blit(coin,(2+j*UNIT+leftOffset,2+i*UNIT+topOffset))

				elif(self.gridLayout[i][j]=='O'):

					screen.blit(power,(2+j*UNIT+leftOffset,2+i*UNIT+topOffset))

				chrr = self.gridLayout[i][j]

		pacmanP1.rect.x = leftOffset + player1PacmanPos[1]*UNIT
		pacmanP1.rect.y = topOffset + player1PacmanPos[0]*UNIT

		ghostP1.rect.x = leftOffset + player1GhostPos[1]*UNIT
		ghostP1.rect.y = topOffset + player1GhostPos[0]*UNIT

		pacmanP2.rect.x = leftOffset + player2PacmanPos[1]*UNIT
		pacmanP2.rect.y = topOffset + player2PacmanPos[0]*UNIT

		ghostP2.rect.x = leftOffset + player2GhostPos[1]*UNIT
		ghostP2.rect.y = topOffset + player2GhostPos[0]*UNIT		

		allSpritesList.draw(screen)

		textsurface = gameFont.render('Team 1 : '+player1Name, False, team1)
		screen.blit(textsurface,(10,10))

		textsurface = gameFont.render('Score : '+str(scoreP1), False, team1)
		screen.blit(textsurface,(10,150))

		textsurface = gameFont.render('Pacman time : '+str(round(timePacmanP1,4)), False, team1)
		screen.blit(textsurface,(10,210))

		textsurface = gameFont.render('Ghost time : '+str(round(timeGhostP1,4)), False, team1)
		screen.blit(textsurface,(10,270))

		textsurface = gameFont.render('Team 2 : '+player2Name, False, team2)
		screen.blit(textsurface,(890,10))

		textsurface = gameFont.render('Score : '+str(scoreP2), False, team2)
		screen.blit(textsurface,(890,150))

		textsurface = gameFont.render('Pacman time : '+str(round(timePacmanP2,4)), False, team2)
		screen.blit(textsurface,(890,210))

		textsurface = gameFont.render('Ghost time : '+str(round(timeGhostP2,4)), False, team2)
		screen.blit(textsurface,(890,270))

		pygame.display.flip()

		clock.tick(30)

class Characters(pygame.sprite.Sprite):
	"""
	This class represents the Pacman amd the Ghost.
	It derives from the "Sprite" class in Pygame.
	"""
 
	def __init__(self, image,posX,posY,size=UNIT):
		""" Constructor. Pass in the color of the block,
		and its x and y position. """
 
		# Call the parent class (Sprite) constructor
		super().__init__()
 
		self.rect = pygame.Rect(posX*size, posY*size, size, size)
		self.image = pygame.transform.scale( pygame.image.load(image) , (size,size) )


pygame.init()
pygame.font.init()
gameFont = pygame.font.SysFont('Comic Sans MS', 30)
screen_width = 1200
screen_height = 700
screen = pygame.display.set_mode([screen_width, screen_height])

clock = pygame.time.Clock()

pacmanP1 = Characters('img/pacman1.png',1,1)
pacmanP2 = Characters('img/pacman2.png',5,1)
ghostP1 = Characters('img/ghost1.png',1,30)
ghostP2 = Characters('img/ghost2.png',5,30)

allSpritesList = pygame.sprite.Group()
allSpritesList.add(pacmanP1)
allSpritesList.add(pacmanP2)
allSpritesList.add(ghostP1)
allSpritesList.add(ghostP2)
allSpritesList.draw(screen)
pygame.display.flip()

player1Name = open('Player/teamName.txt','r').readline().rstrip('\n')
player2Name = open('Adversary/teamName.txt','r').readline().rstrip('\n')



def loadGrid(file):

	'''
		This function will read a grid layout from a file
	'''

	f = open(file,'r')

	lines=f.readlines()	
	grid = []
	
	for line in lines:

		li = []

		for i in line:

			li.append(str(i))

		grid.append(np.array(li))

	gridLayout = np.array(grid)
	rows = len(gridLayout)
	columns = len(gridLayout[0])

	print(gridLayout[1][5])

	return Grid(gridLayout=gridLayout,rows=rows-1,columns=columns-1)

def movement(grid,currentPos,move):

	'''
			0 : go UP
			1 : go DOWN
			2 : go LEFT
			3 : go RIGHT

			Return tuple (new row , new column)

			If possible movement then return newpos
			else return currentpos
	'''

	if(move==0): # Go Up
		newPos = (currentPos[0]-1,currentPos[1])
	elif(move==1): # Go Down
		newPos = (currentPos[0]+1,currentPos[1])	
	elif(move==2): # Go Left
		newPos = (currentPos[0],currentPos[1]-1)
	else: # Go Right
		newPos = (currentPos[0],currentPos[1]+1)

	##### grid.gridLayout[currentPos[0]][currentPos[1]]='.'

	if(grid.validPosition(newPos[0],newPos[1])):	

		return newPos

	else:

		return currentPos

def getMove(grid,myPacmanPos,myGhostPos,enemyPacmanPos,enemyGhostPos,mode):

	t1 = time.time()

	if(mode=='player1Pacman'):

		move = player1Pacman(grid,myPacmanPos,myGhostPos,enemyPacmanPos,enemyGhostPos)

	elif(mode=='player1Ghost'):

		move = player1Ghost(grid,myPacmanPos,myGhostPos,enemyPacmanPos,enemyGhostPos) 

	elif(mode=='player2Pacman'):

		move = player2Pacman(grid,myPacmanPos,myGhostPos,enemyPacmanPos,enemyGhostPos)

	else:

		move = player2Ghost(grid,myPacmanPos,myGhostPos,enemyPacmanPos,enemyGhostPos) 

	t2 = time.time()
	
	return (move,t2-t1)

def update(grid,newPlayer1PacmanPos,newPlayer1GhostPos,newPlayer2PacmanPos,newPlayer2GhostPos,player1PacmanVul,player1GhostVul,player2PacmanVul,player2GhostVul,player1PacmanSuper,player2PacmanSuper,player1Score,player2Score):

	newPlayer1PacmanVul = player1PacmanVul
	newPlayer1GhostVul = player1GhostVul
	newPlayer2PacmanVul = player2PacmanVul
	newPlayer2GhostVul = player2GhostVul
	newPlayer1PacmanSuper = player1PacmanSuper
	newPlayer2PacmanSuper = player2PacmanSuper
	newPlayer1Score = player1Score
	newPlayer2Score = player2Score

	# 'o'

	if(grid.gridLayout[newPlayer1PacmanPos[0]][newPlayer1PacmanPos[1]]=='o'):

		newPlayer1Score += 1
		grid.gridLayout[newPlayer1PacmanPos[0]][newPlayer1PacmanPos[1]]='.'

	elif(grid.gridLayout[newPlayer1PacmanPos[0]][newPlayer1PacmanPos[1]]=='O'):

		newPlayer1Score += 1
		newPlayer1PacmanSuper = 11
		grid.gridLayout[newPlayer1PacmanPos[0]][newPlayer1PacmanPos[1]]='.'

	if(newPlayer1PacmanPos[0]==newPlayer2GhostPos[0]) and (newPlayer1PacmanPos[1]==newPlayer2GhostPos[1]):	

		if(player1PacmanSuper>0):

			if(player2GhostVul==5):

				newPlayer2GhostVul = 0
				newPlayer1Score += 10

		else:

			if(player1PacmanVul==5):

				newPlayer1PacmanVul = 0
				newPlayer2Score += 10



	if(grid.gridLayout[newPlayer2PacmanPos[0]][newPlayer2PacmanPos[1]]=='o'):

		newPlayer2Score += 1
		grid.gridLayout[newPlayer2PacmanPos[0]][newPlayer2PacmanPos[1]]='.'

	elif(grid.gridLayout[newPlayer2PacmanPos[0]][newPlayer2PacmanPos[1]]=='O'):

		newPlayer2Score += 1
		newPlayer2PacmanSuper = 11
		grid.gridLayout[newPlayer2PacmanPos[0]][newPlayer2PacmanPos[1]]='.'

	if(newPlayer2PacmanPos[0]==newPlayer1GhostPos[0]) and (newPlayer2PacmanPos[1]==newPlayer1GhostPos[1]):	

		if(player2PacmanSuper>0):

			if(player1GhostVul==5):

				newPlayer1GhostVul = 0
				newPlayer2Score += 10

		else:

			if(player2PacmanVul==5):

				newPlayer2PacmanVul = 0
				newPlayer1Score += 10


	## grid layout updates

	#grid.gridLayout[newPlayer1GhostPos[0]][newPlayer1GhostPos[1]]='G'
	#grid.gridLayout[newPlayer2GhostPos[0]][newPlayer2GhostPos[1]]='g'
	#grid.gridLayout[newPlayer1PacmanPos[0]][newPlayer1PacmanPos[1]]='P'
	#grid.gridLayout[newPlayer2PacmanPos[0]][newPlayer2PacmanPos[1]]='p'


	## iterative updates
	newPlayer1PacmanVul = min(5,newPlayer1PacmanVul+1)
	newPlayer1GhostVul = min(5,newPlayer1GhostVul+1)
	newPlayer2PacmanVul = min(5,newPlayer2PacmanVul+1)
	newPlayer2GhostVul = min(5,newPlayer2GhostVul+1)
	newPlayer1PacmanSuper = max(0,newPlayer1PacmanSuper-1)
	newPlayer2PacmanSuper = max(0,newPlayer2PacmanSuper-1)

	return (newPlayer1PacmanVul,newPlayer1GhostVul,newPlayer2PacmanVul,newPlayer2GhostVul,newPlayer1PacmanSuper,newPlayer2PacmanSuper,newPlayer1Score,newPlayer2Score)

def game(gridFile):

	player1PacmanVul = 5
	player2PacmanVul = 5
	player1PacmanSuper = 0
	player2PacmanSuper = 0
	player1GhostVul = 5
	player2GhostVul = 5

	player1Score = 0 
	player2Score = 0 

	grid = loadGrid(gridFile)

	player1PacmanPos = (None,None)
	player1GhostPos = (None,None)
	player2PacmanPos = (None,None)
	player2GhostPos = (None,None)

	#print(grid.gridLayout)
	#print(grid.gridLayout[1][1])

	for i in range(grid.rows):
		#print(grid.gridLayout[i])
		for j in range(grid.columns):
			#print(i,j)
			if(grid.gridLayout[i][j]=='P'):
				player1PacmanPos = (i,j)
				grid.gridLayout[i][j]='.'
			elif(grid.gridLayout[i][j]=='p'):
				player2PacmanPos = (i,j)
				grid.gridLayout[i][j]='.'
			elif(grid.gridLayout[i][j]=='G'):
				player1GhostPos = (i,j)
				grid.gridLayout[i][j]='.'
			elif(grid.gridLayout[i][j]=='g'):
				player2GhostPos = (i,j)
				grid.gridLayout[i][j]='.'

	turns = 500

	while(turns>=0 or player1Score == player2Score ):

		# Events
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT: 
				turns=-1
				break

		## Get Move

		# Get move for player 1 pacman
		(player1PacmanMove,p1PacmanTime) = getMove(grid,player1PacmanPos,player1GhostPos,player2PacmanPos,player2GhostPos,'player1Pacman')

		# Get move for player 1 ghost
		(player1GhostMove,p1GhostTime) = getMove(grid,player1PacmanPos,player1GhostPos,player2PacmanPos,player2GhostPos,'player1Ghost')
		
		# Get move for player 2 pacman
		(player2PacmanMove,p2PacmanTime) = getMove(grid,player2PacmanPos,player2GhostPos,player1PacmanPos,player1GhostPos,'player2Pacman')
		
		# Get move for player 2 ghost
		(player2GhostMove,p2GhostTime) = getMove(grid,player2PacmanPos,player2GhostPos,player1PacmanPos,player1GhostPos,'player2Ghost')
		
		## Make Movement

		# Move Player 1 Pacman	
		newPlayer1PacmanPos = movement(grid,player1PacmanPos,player1PacmanMove)

		# Move Player 1 Ghost
		newPlayer1GhostPos = movement(grid,player1GhostPos,player1GhostMove)

		# Move Player 2 Pacman		
		newPlayer2PacmanPos = movement(grid,player2PacmanPos,player2PacmanMove)
		
		# Move Player 2 Ghost
		newPlayer2GhostPos = movement(grid,player2GhostPos,player2GhostMove)

		## Update

		(player1PacmanVul,player1GhostVul,player2PacmanVul,player2GhostVul,player1PacmanSuper,player2PacmanSuper,player1Score,player2Score) = update(grid,newPlayer1PacmanPos,newPlayer1GhostPos,newPlayer2PacmanPos,newPlayer2GhostPos,player1PacmanVul,player1GhostVul,player2PacmanVul,player2GhostVul,player1PacmanSuper,player2PacmanSuper,player1Score,player2Score)

		player1PacmanPos = (newPlayer1PacmanPos[0],newPlayer1PacmanPos[1])
		player1GhostPos = (newPlayer1GhostPos[0],newPlayer1GhostPos[1])
		player2PacmanPos = (newPlayer2PacmanPos[0],newPlayer2PacmanPos[1])
		player2GhostPos = (newPlayer2GhostPos[0],newPlayer2GhostPos[1])
	
		
		grid.show(player1PacmanPos,player1GhostPos,player2PacmanPos,player2GhostPos,player1Score,p1PacmanTime,p1GhostTime,player2Score,p2PacmanTime,p2GhostTime)
		print('Player 1 points : '+str(player1Score))
		print('Player 2 points : '+str(player2Score))
		print('Player 1 time : '+str(p1PacmanTime)+' '+str(p1GhostTime))
		print('Player 2 time : '+str(p2PacmanTime)+' '+str(p2GhostTime))
		#print(grid)

		turns -= 1

	textsurface = gameFont.render( (player1Name if player1Score>player2Score else player2Name)+' Wins', False, white)
	screen.blit(textsurface,(550,650))
	pygame.display.flip()
	
	closed=False

	while not closed:
		for event in pygame.event.get(): 
			if event.type == pygame.QUIT:
				closed=True 
				break

if __name__ == '__main__':
	
	game('pacmanGrid.txt')
