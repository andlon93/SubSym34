import pygame, sys
from pygame.locals import *
#constants representing colours
BLACK = (0, 0, 0 )
BLACKK = (10, 10, 10 )
BROWN = (153, 76, 0 )
GREEN = (0, 255, 0 )
BLUE = (0, 0, 255)
YELLOW = (0 ,255 , 255)
import time
#constants representing the different resources
DIRT = 0
GRASS = 1
WATER = 2
COAL = 3


#a dictionary linking resources to colours
colours = {
			DIRT : BROWN,
			GRASS : GREEN,
			WATER : BLUE,
			COAL : BLACK
			}
#a list representing our tilemap
tilemap = [
			[COAL, COAL, COAL ],
			[COAL, COAL, COAL],
			[COAL, COAL, COAL],
			[COAL, COAL, COAL ],
			[COAL, COAL, COAL ]
			]
#useful game dimensions
TILESIZE = 40
MAPWIDTH = 10
MAPHEIGHT = 10
#set up the display
pygame.init()
DISPLAYSURF = pygame.display.set_mode((MAPWIDTH*TILESIZE,MAPHEIGHT*TILESIZE))

fo = open("test.txt", "r")
board = [[0 for x in range(10)] for k in range(10) ]
for i in range(10):
	temp = fo.readline()
	for k in range(len(temp)-1):
		board[i][k] = int(temp[k])

for i in range(len(board)):
	for k in range(len(board)):
		if (board[i][k]==0):
			board[i][k]=BLACK
		elif (board[i][k]==1):
			board[i][k]=BLUE
		elif (board[i][k]==2):
			board[i][k]=BROWN
		elif (board[i][k]==3):
			board[i][k]=YELLOW

actions = [[0 for x in range(2)] for k in range(60) ]
for i in range(60):
	temp = fo.readline()
	actions[i][0] = temp[4]
	actions[i][1] = temp[1]
for a in board:
	print (a)

delay = 1

while True:
	#get all the user events
	for event in pygame.event.get():
		#if the user wants to quit
		if event.type == QUIT:
			#and the game and close the window
			pygame.quit()
			sys.exit()
	# #loop through each row
	# for row in range(MAPHEIGHT):
	# 	#loop through each column in the row
	# 	for column in range(MAPWIDTH):
	# 		#draw the resource at that position in the tilemap, using the correct colour
	# 		pass
	# 		pygame.draw.rect(DISPLAYSURF, YELLOW, (column*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))
	time.sleep(delay)
	for row in range(10):
		for til in range(10):
			pygame.draw.rect(DISPLAYSURF, board[row][til], (til*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))
	pygame.display.update()
	time.sleep(delay)
	last = None
	for i in range(len(actions)):
		if not last==None:
			pygame.draw.rect(DISPLAYSURF,BLACKK, (last[0]*TILESIZE,last[1]*TILESIZE,TILESIZE,TILESIZE))
		til = int(actions[i][0])
		row = int(actions[i][1])
		last = (til,row)
		print(til, row)
		pygame.draw.rect(DISPLAYSURF,YELLOW, (til*TILESIZE,row*TILESIZE,TILESIZE,TILESIZE))
		pygame.display.update()
		time.sleep(0.05)
	pygame.display.update()
