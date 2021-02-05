#############################################
# Game code for The Game of UR ~ v0.3 ~ SAB #
#############################################
#            Twenty_Squares.py              #
#############################################

from random import *

paths = {
	1: {True : ((0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (1,8), (1,7), (100, 100)),
		False: ((0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (3,8), (3,7), (100, 100))},
	2: {True : ((0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7), (100, 100)),
		False: ((0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7), (100, 100))},
	3: {True : (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (1,1), (1,2), (1,3), (1,4), (100, 100)
	),
		False: (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (3,1), (3,2), (3,3), (3,4), (100, 100)
	),
		"flip": 14},
	4: {True : (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (100, 100)
	),
		False: (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (100, 100)
	),
		"flip": 14},
	5: {True : (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (3,1), (3,2), (3,3), (3,4), (100, 100)
	),
		False: (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (1,1), (1,2), (1,3), (1,4), (100, 100)
	),
		"flip": 14},
}

class Piece(object):
	def __init__(self, number, player = None, pathType = 1, breakCounterRules = False):
		if breakCounterRules not in [True, False]:
			print("Error: breakCounterRules not in [True, False]")
			print("Error: "+str(breakCounterRules)+" not in [True, False]")
			raise KeyError(breakCounterRules)

		if breakCounterRules == False:
			if number >= 10:
				print("Error: too many counter")
				print("Error: "+str(number)+" >= 10")
				raise IndexError(number)
			if number < 0:
				print("Error: number of counter must be positive")
				print("Error: "+str(number)+" < 0")
				raise IndexError(number)

		self.posPath = 0
		self.posVect = (0, 0)

		self.player = player
		self.number = number

		if pathType not in paths:
			print("Error: pathType not in paths")
			print("Error: "+str(pathType)+" not in global object paths")
			raise TypeError(pathType)

		if player not in paths[pathType] or player == "flip":
			print("Error: player not in paths[pathType] (or player == 'flip')")
			print("Error: "+str(player)+" not in paths["+str(pathType)+"]")
			raise TypeError(player)
		else:
			self.pathType = pathType
			self.path     = paths[pathType][self.player]
			

		if player == True:
			self.color = "white"
		elif player == False:
			self.color = "black"
		else: 
			print("Error:")
			print("  player must be bool")
			print("  player == True or == False or == None")
			print("")

		self.name = self.color[0].upper() + str(self.number+1)

		self.topSideUp = True

	# returns this when object called
	def __repr__(self):
		return self.name

	def update_posVect(self):
		self.posVect = self.path[self.posPath]

class Board:
	def __init__(self, pathType = 1, firstMove = True, pieceCount = (7, 7), breakCounterRules = False):
		if breakCounterRules not in [True, False]:
			print("Error: breakCounterRules not in [True, False]")
			print("Error: "+str(breakCounterRules)+" not in [True, False]")
			raise KeyError(breakCounterRules)

		if pathType not in paths:
			print("Error:")
			print("  Path type not known")
			print("  pathType not in paths object - default is 1, 2, 3, 4 or 5")
			print("")

		self.turn = firstMove
		self.pathType = pathType
		self.path     = paths[pathType]
		self.placeNames = (
			("a1", "a2", "a3", "a4", "a5", "a6", "a7", "a8"), 
			("b1", "b2", "b3", "b4", "b5", "b6", "b7", "b8"), 
			("c1", "c2", "c3", "c4", "c5", "c6", "c7", "c8")
		)
		self.contence = [
			[" -- ", " -- ", " -- ", " -- ", " xx ", " xx ", " -- ", " -- "], 
			[" -- ", " -- ", " -- ", " -- ", " -- ", " -- ", " -- ", " -- "], 
			[" -- ", " -- ", " -- ", " -- ", " xx ", " xx ", " -- ", " -- "]
		]

		self.pieceCount = {
			True:  pieceCount[0],
			False: pieceCount[1]
		}

		self.pieces = {}
		for player in self.pieceCount:
			tempList = []
			for num in range(self.pieceCount[player]):
				tempList.append(Piece(num, player = player, pathType = self.pathType, breakCounterRules = breakCounterRules))
			#next num
			self.pieces[player] = tempList
		#next player

		self.score = {True: 0, False: 0}

		self.rosette  = [(1, 1), (3, 1), (1, 7), (3, 7), (2, 4)]

	# returns this when object called
	def __repr__(self):
		returnString = ""

		count = 0
		for y in self.contence:
			count += 1
			for x in y:
				returnString += x
			#next i
			if count != 3:
				returnString += "\n"

		return returnString

	def is_legal(self, move):
		if move.initialPosVect == (100, 100):
			print("Piece at end")
			return False

		if move.finalPosVect != (100, 100):
			for piece in self.pieces[self.turn]:
				if move.finalPosVect == piece.posVect:
					print("Piece blocked")
					return False

		if move.finalPosVect in self.rosette:
			for piece in self.pieces[not self.turn]:
				if move.finalPosVect == piece.posVect:
					print("Can't take on rosette")
					return False

		return True

	def moves(self, diceValue):
		moves = []
		for piece in self.pieces[self.turn]:
			move = Move(piece.posPath, diceValue, self.pathType, self.turn)
			moves.append(move)

		return moves

	def legal_moves(self, diceValue):
		legal_moves = []
		for piece in self.pieces[self.turn]:
			move = Move(piece.posPath, diceValue, self.pathType, self.turn)
			if self.is_legal(move):
				legal_moves.append(move)

		return legal_moves

	def do_move(self, move, brakeRules = False):
		if move.player != self.turn:
			print("Error:")
			print("  Not that players turn")
			print("  move.player != self.turn")
			print("")
			return

		if brakeRules:
			moveSet = self.moves(move.diceValue)
		else:
			moveSet = self.legal_moves(move.diceValue)

		#print(move)
		#print(moveSet)

		if move in moveSet:
			#move piece
			for piece in self.pieces[self.turn]:
				if move.initialPosPath == piece.posPath:
					self.pieces[self.turn][piece.number].posPath = move.finalPosPath
					self.pieces[self.turn][piece.number].update_posVect()
					if "flip" in self.path:
						if move.finalPosPath > self.path["flip"]:
							self.pieces[self.turn][piece.number].topSideUp = False
					if move.finalPosVect == (100, 100):
						self.score[self.turn] += 1
					break

			#capture opponent
			if move.finalPosVect not in self.rosette and move.finalPosVect != (100, 100):
				for piece in self.pieces[not self.turn]:
					if move.finalPosVect == piece.posVect:
						print("capture")
						piece.posPath = 0
						piece.update_posVect()
					else: pass

			if move.finalPosVect not in self.rosette:
				self.turn = not self.turn
			else: pass

		else:
			if brakeRules:
				print("Error:")
				print("  Move is not possible")
				print("  move must be in set of board.moves()")
				print("")
				return
			else:
				print("Error:")
				print("  Move is not possible")
				print("  move must be in set of board.legal_moves()")
				print("")
				return

		#Update Board
		for y in range(len(self.contence)):
			for x in range(len(self.contence[y])):
				if y in [0, 2] and x in [4, 5]:
					self.contence[y][x] = " xx "
				else:
					self.contence[y][x] = " -- "


		for player in self.pieces:
			for piece in self.pieces[player]:
				if piece.posVect == (0, 0) or piece.posVect == (100, 100): 
					continue
				if piece.posVect[0] not in [1, 2, 3] or piece.posVect[0] not in [1, 2, 3, 4, 5, 6, 7, 8]:
					print("Error:")
					print(" Pieces must be on board")
					print(" piece.posVect[0] not in [1, 2, 3] or piece.posVect[0] not in [1, 2, 3, 4, 5, 6, 7, 8]")

				#print(piece.posVect)

				self.contence[piece.posVect[0]-1][piece.posVect[1]-1] = " " + piece.name + " "

	def move_name(self, move):
		moveName = ""

		for piece in self.pieces[move.player]:
			if move.initialPosPath == piece.posPath:
				moveName += " " + piece.name
				break

		if moveName == "":
			return "No Such Move"

		if move.finalPosVect == (100, 100):
			moveName += " #"

			if self.score[move.player] == len(self.pieces[move.player]):
				moveName += "#"
			else: pass
		else:
			moveName += self.placeNames[move.finalPosVect[0]-1][move.finalPosVect[1]-1]

		if move.finalPosVect not in self.rosette and move.finalPosVect != (100, 100):
			for piece in self.pieces[not self.turn]:
				if move.finalPosVect == piece.posVect:
					moveName += " X " + piece.name
				else: pass

		return moveName

class Move(object):
	def __init__(self, initialPosPath, diceValue, pathType, player):
		diceValue = abs(diceValue)

		if pathType not in paths:
			print("Error: pathType not in global paths object")
			print("Error: "+str(pathType)+" not in global paths object")
			raise KeyError(pathType)
		elif player not in paths[pathType] or player == "flip":
			print("Error: player not in paths[pathType] (or player == 'flip')")
			print("Error: "+str(player)+" not in paths["+str(pathType)+"]")
			raise KeyError(player)
		else:
			if initialPosPath not in range(len(paths[pathType][player])):
				print("Error: initialPosPath not in range(len(paths[pathType][player]))")
				print("Error: "+str(initialPosPath)+" not in range(len(paths["+str(pathType)+"]["+str(player)+"]))")
				raise IndexError("tuple index out of range")
			else:
				self.initialPosPath = initialPosPath
				self.initialPosVect = paths[pathType][player][initialPosPath]

			if (initialPosPath + diceValue) >= len(paths[pathType][player]):
				self.finalPosPath = len(paths[pathType][player])-1
				self.finalPosVect = paths[pathType][player][-1]

			else:
				self.finalPosPath = initialPosPath + diceValue
				self.finalPosVect = paths[pathType][player][initialPosPath + diceValue]

			self.diceValue = diceValue
			self.pathType  = pathType

			self.player = player

	# returns this when object called
	def __repr__(self):
		return "from:" + str(self.initialPosVect) + " to:" + str(self.finalPosVect)

	def __eq__(self, other):
		if self.initialPosPath == other.initialPosPath:
			if self.finalPosPath   == other.finalPosPath:
				if self.diceValue == other.diceValue:
					if self.pathType  == other.pathType:
						return True
					else: return False
				else: return False
			else: return False
		else: return False

### RUN THIS vvv ###

pathType = choice([1, 2, 3, 4, 5])
print(pathType)
firstMove = choice([True, False])
print(firstMove)
breakCounterRules = choice([True, False])
breakCounterRules = False
print(breakCounterRules)
if breakCounterRules:
	pieceCount = (randint(0, 50), randint(0, 50))
else:
	pieceCount = (choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]), choice([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]))
print(pieceCount)

board = Board(pathType = pathType, firstMove = firstMove, pieceCount = pieceCount, breakCounterRules = breakCounterRules)

number = 7
player = None
pathType = 1
brakeRules = False

piece = Piece(number = 4, player = True, pathType = 1, breakCounterRules = False)

pathType  = choice([1, 2, 3, 4, 5])
player    = choice([True, False])
diceValue = choice([0, 1, 2, 3, 4])
initialPosPath = choice(range(len(paths[pathType][player])))

move  = Move(initialPosPath = initialPosPath, diceValue = diceValue, pathType = pathType, player = player)

if True:
	#print(board)
	#print(board.pieces)

	#print("")
	#print(piece)
	#print("")
	#print(move)
	#print("")
	#print(board.legal_moves(1))

	#print(board)
	#print("")

	#board.do_move(Move(0, 1, 1, True))
	#board.do_move(Move(0, 1, 1, False))

	#print("")
	#print(board)

	
	print(board)
	print("")

	moveSet = [1]

	while board.score[not board.turn] != len(board.pieces[not board.turn]):
		roll = choice([1, 2, 3, 4])
		print("roll: " + str(roll))
		print("turn: " + str(board.turn))
		moveSet = board.legal_moves(roll)
		print("There are " + str(len(moveSet)) + " legal moves")
		if len(moveSet) == 0:
			for i in board.pieces[board.turn]:
				print(i.posVect)
			board.turn = not board.turn
		else:
			move = choice(moveSet)
			print("move: " + board.move_name(move))

			board.do_move(move)

		print(board)
		print("player " + str(not board.turn) +"'s score:" + str(board.score[not board.turn]))
		print("")
	#next while
	

