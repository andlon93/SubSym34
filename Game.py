import random as rng
#board 0=free, 1=food, 2=poison 3=player
#player_dir -1=left 0=up 1=right 2=down
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
		for i in range(length):
			for k in range(length):
				foodRng = rng.random()
				poisonRng = rng.random()
				if rng.random()>foodProb and foodRng>poisonRng:
					self.board[i][k] = 1
				elif rng.random()>poisonProb and poisonRng>foodRng:
					self.board[i][k] = 2
				if player_placed==False and self.board[i][k]==0:
					self.board[i][k] = 3
					player_placed=True
					self.player_pos=[i,k]

	def move(self,dir):
		#dir: -1=left, 0=forward, 1=right
		player_dir = self.player_dir
		player_pos = self.player_pos
		if player_dir==-1:
			if dir==-1:
				player_dir=2
			elif dir==1:
				player_dir=0
		if player_dir==0:
			if dir==-1:
				player_dir=-1
			elif dir==1:
				player_dir=1
		if player_dir==1:
			if dir==-1:
				player_dir=0
			elif dir==1:
				player_dir=2
		if player_dir==2:
			if dir==-1:
				player_dir=1
			elif dir==1:
				player_dir=-1
		if player_dir==-1:
			self.board[player_pos[0]][player_pos[1]]=0
			player_pos[0]=player_pos[0]-1
			self.board[player_pos[0]][player_pos[1]]=3
		if player_dir==0:
			self.board[player_pos[0]][player_pos[1]]=0
			player_pos[1]=player_pos[1]+1
			self.board[player_pos[0]][player_pos[1]]=3
		if player_dir==1:
			self.board[player_pos[0]][player_pos[1]]=0
			player_pos[0]=player_pos[0]+1
			self.board[player_pos[0]][player_pos[1]]=3
		if player_dir==2:
			self.board[player_pos[0]][player_pos[1]]=0
			player_pos[1]=player_pos[1]-1
			self.board[player_pos[0]][player_pos[1]]=3
		self.player_pos = player_pos
		self.player_dir = player_dir

	def getNearbyTiles(self):
		# Returns in order of facing: left, up, right
		length = len(self.board)
		player_dir = self.player_dir
		player_pos = self.player_pos
		nearby = []
		if player_dir == 0:  #up
			tile1X = player_pos[0]
			tile1Y = player_pos[1]-1
			tile2X = player_pos[0]-1
			tile2Y = player_pos[1]
			tile3X = player_pos[0]
			tile3Y = player_pos[1]+1
		if player_dir == 1: #Right
			tile1X = player_pos[0]-1
			tile1Y = player_pos[1]
			tile2X = player_pos[0]
			tile2Y = player_pos[1]+1
			tile3X = player_pos[0]+1
			tile3Y = player_pos[1]
		if player_dir == -1: #Left
			tile1X = player_pos[0]+1
			tile1Y = player_pos[1]
			tile2X = player_pos[0]
			tile2Y = player_pos[1]-1
			tile3X = player_pos[0]-1
			tile3Y = player_pos[1]
		if player_dir == 2: #Down
			tile1X = player_pos[0]
			tile1Y = player_pos[1]+1
			tile2X = player_pos[0]+1
			tile2Y = player_pos[1]
			tile3X = player_pos[0]
			tile3Y = player_pos[1]-1

		if tile1X>length-1:
			tile1X=tile1X-length
		if tile1Y>length-1:
			tile1Y=tile1Y-length
		if tile2X>length-1:
			tile2X=tile2X-length
		if tile2Y>length-1:
			tile2Y=tile2Y-length
		if tile3X>length-1:
			tile3X=tile3X-length
		if tile3Y>length-1:
			tile3Y=tile3Y-length

		nearby.append(self.board[tile1X][tile1Y])
		nearby.append(self.board[tile2X][tile2Y])
		nearby.append(self.board[tile3X][tile3Y])
		return nearby




if __name__ == '__main__':
	b = game()
	b.generateBoard((1/3),(1/3),6)
	b.player_dir=2
	for i in range(len(b.board)):
		print (b.board[i])
	print (b.getNearbyTiles())
	print (b.player_pos)
	# b.move(0)
	# for i in range(len(b.board)):
	# 	print (b.board[i])
	# print (b.getNearbyTiles())
	# print (b.player_pos)
