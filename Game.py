import random as rng
#board 0=free, 1=food, 2=poison 3=player
#player_dir -1=left 0=up 1=right
class game:
	board = []
	player_dir = 0
	player_pos = [0,0]

	def __init__(self,board=None,player_dir=0, player_pos=[0,0]):
		# Constructor for pre-generated board
		self.board = board
		self.player_dir = player_dir
		self.player_pos = player_pos

	def generateBoard(self,foodProb,poisonProb,length):
		self.board = [[0 for x in range(length)] for k in range(length) ]
		player_placed = False
		for k in range(length):
			for i in range(length):
				foodRng = rng.random()
				poisonRng = rng.random()
				if rng.random()>foodProb and foodRng>poisonRng:
					self.board[i][k] = 1
				elif rng.random()>poisonProb and poisonRng>foodRng:
					self.board[i][k] = 2
				if player_placed==False and self.board[i][k]==0:
					self.board[i][k] = 3
					player_placed=True
					self.player_pos=[k,i]


	def getNearbyTiles(self):
		# Returns in order of facing: left, up, right
		length = len(self.board)
		player_dir = self.player_dir
		player_pos = self.player_pos
		nearby = []
		if player_dir == 0:  #UP
			tile2Y = player_pos[0]-1
			tile2X = player_pos[1]

			tile1Y = player_pos[0]
			tile1X = player_pos[1]-1

			tile3Y = player_pos[0]+1
			tile3X = player_pos[1]

			print (player_pos)
			print (tile1X,tile1Y," value: ",self.board[tile1X][tile1Y])
			print (tile2X,tile2Y," value: ",self.board[tile2X][tile2Y])
			print (tile3X,tile3Y," value: ",self.board[tile3X][tile3Y])
			'''
			if tile1Y<0:
				tile1Y=length+tile1Y
			if tile2X<0:
				tile2X=length+tile2X
			if tile3X>(length-1):
				tile3X=tile3X-(length)
			print ("Adjusting")
			print (tile1X,tile1Y," value: ",self.board[tile1X][tile1Y])
			print (tile2X,tile2Y," value: ",self.board[tile2X][tile2Y])
			print (tile3X,tile3Y," value: ",self.board[tile3X][tile3Y])
			'''
			nearby.append(self.board[tile2X][tile2Y])
			nearby.append(self.board[tile1X][tile1Y])
			nearby.append(self.board[tile3X][tile3Y])
		if player_dir == 1:
			pass
		if player_dir == -1:
			pass
		return nearby




if __name__ == '__main__':
	b = game()
	b.generateBoard((1/3),(1/3),6)
	for i in range(len(b.board)):
		print (b.board[i])
	print (b.getNearbyTiles())