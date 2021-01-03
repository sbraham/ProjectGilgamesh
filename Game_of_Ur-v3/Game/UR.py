###########################################
# Game code for The Game of UR ~ v2 ~ SAB #
###########################################
#             Main Game Code              #
###########################################

### Imports ###
import random

### Class ###
class Player(object):
	def __init__(self, name, paths, gameData):
		# name of player - "A" or "B"
		self.name = name
		self.gameData = gameData

		# What is the algorithm used in this player
		#"Human", "Gilg", "Enk" or "random"
		self.AICheck = ("P" + self.name + "_Algo")
		self.algo = self.gameData[self.AICheck] 

		# create a list of counter objects
		# NB - there is a counter 0 that should never be referred to
		self.cntrs = [Counter(0, self)]
		for x in range(1, self.gameData["CntrNum"]+1):
			self.cntrs.insert(x, Counter(x, self))
		#next x

		# determining the players path round the track
		self.path = []
		i = 0
		while self.gameData["Path"][i][0] != 1:
			i += 1
		#end while

		pathName = (self.gameData["Path"][i][1] + self.name)
		self.path = paths[pathName]

	def _defOther(self, otherPlayer):
		# define a variable that contains a deference to the other player object
		# PA.notMe = PB and PB.notMe = PA
		self.notMe = otherPlayer["not " + self.name]

	# a method used that returns one of the players counters
	def _inputCntr(self, roll):
		if self.algo == "Human":
			# if Human loop till there is an appropriate output
			playerInputLoop = True
			while playerInputLoop == True:
				print("Input counter to move - number between 1 and " + str(self.gameData["CntrNum"]))
				playerInput = input("Input: ")

				#Create a list of numbers from 1 to x where x is the number of counters this player has
				checkCntrSet = []
				for x in range(1, self.gameData["CntrNum"]+1):
					checkCntrSet.insert(x, str(x))
				#next x

				# is the player input a counter that this player owns
				if playerInput in checkCntrSet: #if yes
					# return that counter
					return self.cntrs[int(playerInput)]
					playerInputLoop = False
				else: #if no
					#tell the player to input another counter and loop till they input a good counter
					print("Invalid Input - counter must be between 1 and " + str(self.gameData["CntrNum"]))
					print()
			#end while
		elif self.algo == "Gilg":
			# to do in V3
			# for now return counter 1
			return self.cntrs[1]
			pass
		elif self.algo == "Enk":
			# to do in V3
			# for now return counter 1
			return self.cntrs[1]
			pass
		else:
			# create a list of all counters that can move
			randCntr = []			
			for cntr in self.cntrs:
				if cntr.num != 0 and cntr._canMove(roll)["bool"]:
					randCntr.append(cntr)
			# then pick randomly from that list
			randomInput = random.choice(randCntr)
			return randomInput

	# this method resets all counters so they think they can move
	# this means that if a counter couldn't move last turn and can now
	# it becomes able to move and will be considered appropriately
	def _turnInitialisation(self):
		# set all counters self.canMove to default
		for cntr in self.cntrs:
			cntr.canMove = {"bool":  True, "capture": {"bool": False, "counter": self}}

	# Method returns true if the player has won
	def _hasWon(self):
		# for every counter this player owns
		for cntr in self.cntrs:
			# if there is a counter that isn't at the end of the track (not including counter 0)
			if cntr.num != 0 and cntr.boardPOS[1] != 100:
				# that player hasn't won
				return False
				#end function
			else: pass
		#next cntr

		# if false has not been returned then all counters are at the end
		# therefore the player has won
		return True

	# return this players counter details - debug method, not used in the program
	def _show(self):
		#self.cntrs[7]._show()
		for cntr in self.cntrs:
			cntr._show()

class Counter(object):
	def __init__(self, number, master):
		# set the counters name (number), its master (the player that owns it)
		self.num = number
		self.master = master

		self.gameData = self.master.gameData

		# set default board position and canMove value
		self.pathPOS = 0
		self.boardPOS = (0,0)
		self.canMove = {"bool":  True, "reason": "Counter CAN move", "capture": {"bool": False, "counter": self}}

	# update the board position (board position vector)
	def _boardPOS(self):
		self.boardPOS = self.master.path[self.pathPOS]

	# Method returns a canMove object telling you
	# self.canMove = {"bool":  If the counter can move, "reason": if it can't, why?, 
	# "capture": {"bool": does it capture a counter, "counter": and if so, which counter}}
	def _canMove(self, roll):
		# if I am not counter 0
		if self.num != 0:
			# and I think I can move
			if self.canMove["bool"] == True:
				# and I have not finished
				if self.boardPOS[1] != 100:

					# determine what my new board position will be
					self.newPathPOS = self.pathPOS + roll

					# if the new position is still on the board
					if self.newPathPOS < len(self.master.path):
						# find the new position
						self.newBoardPOS = self.master.path[self.newPathPOS]

						# for all of the friendly counters
						for cntr in self.master.cntrs:
							# if they are in my now board position
							if cntr.boardPOS == self.newBoardPOS and cntr.boardPOS[1] != 100:
								# I can't move
								self.canMove["reason"] = "Tile occupied by own counter"
								self.canMove["bool"] = False
							else: pass
						#next cntr

						# if I still think I can move
						if self.canMove["bool"] == True:
							# for all of the opponents counters
							for cntr in self.master.notMe.cntrs:
								# if they are in my now board position
								if cntr.boardPOS == self.newBoardPOS:
									# and they are on a rosette
									if cntr.boardPOS in self.gameData["rosette"]:
										# I can't move
										self.canMove["reason"] = "Tile occupied by opponents counter AND they are on a rosette"
										self.canMove["bool"] = False
									# if they are not a rosette
									else:
										# then I can capture them
										self.canMove["reason"] = "Capture!"
										self.canMove["capture"] = {"bool": True, "counter": cntr}
								else: pass
							#next cntr
						else: pass

					# if the new position is off the board
					# they can always move
					else: pass
				# if I have finished
				else: 
					#I can't move
					self.canMove["reason"] = "Counter has finished"
					self.canMove["bool"] = False
			# if I don't think I can move
			else:
				# I can't move
				self.canMove["reason"] = "Counter has already tried to move"
				self.canMove["bool"] = False
		# if I am counter 0
		else:
			# I can't move
			self.canMove["reason"] = "Error - checked counter 0"
			self.canMove["bool"] = False

		# return the situation
		return self.canMove

	# return this counters details - debug method, not used in the program
	def _show(self):
		print("Player " + self.master.name + "'s counter " + str(self.num) + " is in position " + str(self.boardPOS) + " (space " + str(self.pathPOS) + ")")

### Functions ###
def _diceRoll(gameData):
	score = 0	# Dice score
	#for all dice
	for x in range(0, gameData["DiceNum"]):
		roll = random.randint(0, 1) # roll the dice
		score = score + roll 		# and add the number to the total dice score
	# return the total number rolled
	return score

def _board(do, players, gameData):
	# reset the board
	row1 = [0, "00", "00", "00", "00", "XX", "XX", "00", "00"]
	row2 = [0, "00", "00", "00", "00", "00", "00", "00", "00"]
	row3 = [0, "00", "00", "00", "00", "XX", "XX", "00", "00"]
	board = [0, row1, row2, row3]

	# for all of Player A's counters
	for cntr in players["A"].cntrs:
		# they they are on the board
		if cntr.boardPOS[0] != 0 and cntr.boardPOS[1] != 100:
			# 'write' them in that position
			board[cntr.boardPOS[0]][cntr.boardPOS[1]] = (cntr.master.name + str(cntr.num))
	# for all of Player B's counters
	for cntr in players["B"].cntrs:
		# they they are on the board
		if cntr.boardPOS[0] != 0 and cntr.boardPOS[1] != 100:
			# 'write' them in that position
			board[cntr.boardPOS[0]][cntr.boardPOS[1]] = (cntr.master.name + str(cntr.num))

	# if the board should be printed
	if do == "print":
		#Print the board
		print(board[1][1:8 +1])
		print(board[2][1:8 +1])
		print(board[3][1:8 +1])
	# if the board should be returned
	elif do == "return":
		return board
	else: pass

	#for debug - ignore
	#PA._show()
	#PB._show()

def _whosTurn(isPAsTurn, players):
	# if it is player A's turn
	if isPAsTurn:
		# return player A
		return players["A"]
	# if it is player B's turn
	else:
		# return player B
		return players["B"]

def GAME(paths, gameData):
	# Initialize the players settings and counters
	PA = Player("A", paths, gameData)
	PB = Player("B", paths, gameData)

	# dictionary used to define Player.notMe and refere to player specific data
	players = {"A": PA, "B": PB, "not B": PA, "not A": PB}

	PA._defOther(players)
	PB._defOther(players)

	# determine who goes first
	# repeat until a player is determined
	isPAsTurn = None
	while isPAsTurn == None:
		# each player rolls a dies
		PAsRoll = _diceRoll(gameData)
		PBsRoll = _diceRoll(gameData)
		# if the rolls are different
		if PAsRoll != PBsRoll:
			# player A goes first if their roll is higher
			isPAsTurn = (PAsRoll > PBsRoll)
			# other wise it is not player A's turn
		# if the rolls are the same do this loop again
		else: pass
	#end while
	
	# keep track of what turn we are on
	turn = 0

	# for each turn
	turnLoop = True
	while turnLoop == True:
		# increment the turn counter
		turn += 1
		# work out who's turn it is
		player = _whosTurn(isPAsTurn, players)
		# and initialize that player
		player._turnInitialisation()

		# say what turn it is, who's turn it is - (and what auto play round it is)
		print("Turn " + str(turn) + " - Player " + player.name + "'s turn - auto play round " + str(gameData["AutoPlayLoops"] + 1))

		# print the board
		_board("print", players, gameData)
		print()

		# roll the dice and say what was rolled
		roll = _diceRoll(gameData)
		print("You rolled - " + str(roll))

		# if a 0 was rolled  
		if roll == 0:
			if player.algo == "Human":
				# tell the human player
				Print("Turn Lost: Press Enter to continue")
			else: pass
			# change the turn
			isPAsTurn = not isPAsTurn
		# if the roll wasn't a 0
		else:
			# move a counter
			moveLoop = True
			while moveLoop == True:
				# check if any counter can move
				count = 0
				for cntr in player.cntrs:
					if cntr._canMove(roll)["bool"] == False or cntr.num == 0:
						count += 1
					else: pass
				# next cntr

				# if no counters can move
				if count == (gameData["CntrNum"] + 1):
					#say so and change the turn
					print("No counters can move")
					isPAsTurn = not isPAsTurn
					moveLoop = False
				# if there are counters that can move
				else:
					# pick a counter to move
					cntrPick = (player._inputCntr(roll))
					print("Counter picked " + str(cntrPick.num))
					print()

					# see if that counter can move (and the situation of the move)
					canMove = cntrPick._canMove(roll)

					# if it can move
					if canMove["bool"]:
						# move it that much along that path
						cntrPick.pathPOS += roll
						# update the position vector of the counter
						if cntrPick.pathPOS < len(cntrPick.master.path):
							cntrPick._boardPOS()
						else: #new position is off board (at end):
							cntrPick.boardPOS = (0,100)
						moveLoop = False
						# if the counter captured a counter
						if canMove["capture"]["bool"]:
							# set the captured counters position to the start
							canMove["capture"]["counter"].pathPOS = 0
							# and update the position vector of captured counter
							canMove["capture"]["counter"]._boardPOS()
					# if the counter can't move
					else:
						# say why
						print(canMove["reason"])

					# if the counters new position is not a rosette
					if cntrPick.boardPOS not in gameData["rosette"]:
						# change the players turn
						isPAsTurn = not isPAsTurn
					# if it is - take another turn
					else: pass

		# at the end of each turn
		# if the current player has won
		if player._hasWon():
			# say so
			print("Player " + player.name + " has Won - Yay")
			print()
			# and print the final board state
			_board("print", players, gameData)
			print()
			# if there is a human player
			if player.algo == "Human" or player.notMe.algo == "Human":
				# allow them to hold the game before the menu
				input("Press Enter to continue")
			else: pass
			# don't do a next turn
			turnLoop = False
		else: pass
	#end while

# Start test
# from Data import paths, gameData

# GAME(paths, gameData)