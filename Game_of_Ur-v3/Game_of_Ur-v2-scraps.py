###########################################
# Game code for The Game of UR ~ v2 ~ SAB #
###########################################

### Imports ###
import random

### Class ###
class Player(object):
	def __init__(self, name):
		# name of player - "A" or "B"
		self.name = name

		# What is the algorithm used in this player
		#"Human", "Gilg", "Enk" or "random"
		self.AICheck = ("P" + self.name + "_Algo")
		self.algo = settings[self.AICheck] 

		# create a list of counter objects
		# NB - there is a counter 0 that should never be referred to
		self.cntrs = [Counter(0, self)]
		for x in range(1, settings["CntrNum"]+1):
			self.cntrs.insert(x, Counter(x, self))
		#next x

		# determining the players path round the track
		self.path = []
		i = 0
		while settings["Path"][i][0] != 1:
			i += 1
		#end while

		pathName = (settings["Path"][i][1] + self.name)
		self.path = paths[pathName]

	def _defOther(self):
		# define a variable that contains a deference to the other player object
		# PA.notMe = PB and PB.notMe = PA
		self.notMe = otherPlayer[self.name]

	# a method used that returns one of the players counters
	def _inputCntr(self, roll):
		if self.algo == "Human":
			# if Human loop till there is an appropriate output
			playerInputLoop = True
			while playerInputLoop == True:
				print("Input counter to move - number between 1 and " + str(settings["CntrNum"]))
				playerInput = input("Input: ")

				#Create a list of numbers from 1 to x where x is the number of counters this player has
				checkCntrSet = []
				for x in range(1, settings["CntrNum"]+1):
					checkCntrSet.insert(x, str(x))
				#next x

				# is the player input a counter that this player owns
				if playerInput in checkCntrSet: #if yes
					# return that counter
					return self.cntrs[int(playerInput)]
					playerInputLoop = False
				else: #if no
					#tell the player to input another counter and loop till they input a good counter
					print("Invalid Input - counter must be between 1 and " + str(settings["CntrNum"]))
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

	# this method redefines most of the players variables
	# to ensure the settings are correct and each game starts fresh
	def _gameInitialisation(self):
		# What is the algorithm used in this player
		#"Human", "Gilg", "Enk" or "random"
		self.AICheck = ("P" + self.name + "_Algo")
		self.algo = settings[self.AICheck] 

		# create a list of counter objects
		# NB - there is a counter 0 that should never be referred to
		self.cntrs = [Counter(0, self)]
		for x in range(1, settings["CntrNum"]+1):
			self.cntrs.insert(x, Counter(x, self))
		#next x

		# determining the players path round the track
		self.path = []
		i = 0
		while settings["Path"][i][0] != 1:
			i += 1
		#end while

		pathName = (settings["Path"][i][1] + self.name)
		self.path = paths[pathName]

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

		# set default board position and canMove value
		self.pathPOS = 0
		self.boardPOS = (0,0)
		self.canMove = {"bool":  True, "reason": "", "capture": {"bool": False, "counter": self}}

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
								if cntr.boardPOS in rosette:
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
def _diceRoll():
	score = 0	# Dice score
	#for all dice
	for x in range(0, settings["DiceNum"]):
		roll = random.randint(0, 1) # roll the dice
		score = score + roll 		# and add the number to the total dice score
	# return the total number rolled
	return score

def _board(do):
	# reset the board
	row1 = [0, "00","00","00","00","XX","XX","00","00"]
	row2 = [0, "00","00","00","00","00","00","00","00"]
	row3 = [0, "00","00","00","00","XX","XX","00","00"]
	board = [0, row1, row2, row3]

	# for all of Player A's counters
	for cntr in PA.cntrs:
		# they they are on the board
		if cntr.boardPOS[0] != 0 and cntr.boardPOS[1] != 100:
			# 'write' them in that position
			board[cntr.boardPOS[0]][cntr.boardPOS[1]] = (cntr.master.name + str(cntr.num))
	# for all of Player B's counters
	for cntr in PB.cntrs:
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

def _whosTurn(isPAsTurn):
	# if it is player A's turn
	if isPAsTurn:
		# return player A
		return PA
	# if it is player B's turn
	else:
		# return player B
		return PB

def GAME(isPAsTurn, autoPlayCount):
	# Initialize the players settings and counters
	PA._gameInitialisation()
	PB._gameInitialisation()

	# determine who goes first
	# repeat until a player is determined
	isPAsTurn = None
	while isPAsTurn == None:
		# each player rolls a dies
		PAsRoll = _diceRoll()
		PBsRoll = _diceRoll()
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
		player = _whosTurn(isPAsTurn)
		# and initialize that player
		player._turnInitialisation()

		# say what turn it is, who's turn it is - (and what auto play round it is)
		print("Turn " + str(turn) + " - Player " + player.name + "'s turn - auto play round " + str(autoPlayCount + 1))

		# print the board
		_board("print")
		print()

		# roll the dice and say what was rolled
		roll = _diceRoll()
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
				if count == (settings["CntrNum"] + 1):
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
						cntrPick._boardPOS()
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
					if cntrPick.boardPOS not in rosette:
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
			_board("print")
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

# this settings function will do a series of boolean while loops to do menus
# saving the settings in a the dictionary variable "settings"
# it then returns the settings variables
# read the prints to determine what each input does
def SETTINGS(settings):
	settingsLoop = True
	while settingsLoop == True:
		print("Settings Menu:")
		print("For player settings     - press 1")
		print("For path settings       - press 2")
		print("For counter settings    - press 3")
		print("For dice settings       - press 4")
		print("For auto play settings  - press 5")
		print("To set default settings - press 6")
		print()
		print("To quit settings menu  - press Q")
		print("Q to quit works in all settings")
		playerInput = input("Input: ")
		print()
		if playerInput == "Q" or playerInput == "q":
			return settings
		elif playerInput == "1":
			playerSettingsLoop = True
			while playerSettingsLoop == True:
				print("Player Settings Menu:")
				print("To change Player A's algorithm - press 1")
				print("To change Player B's algorithm - press 2")
				print()
				print("To quit settings menu - press Q")
				playerInput = input("Input: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					playerSettingsLoop = False
				elif playerInput == "1":
					playerSettingsLoopA = True
					while playerSettingsLoopA == True:
						print("Set Player A's algorithm")
						print("1: Human")
						print("2: Gilgamesh")
						print("3: Enkidu")
						print("4: Random")
						playerInput = input("Input: ")
						print()
						if playerInput == "1":
							settings["PA_Algo"] = "Human"
							playerSettingsLoopA = False
						elif playerInput == "2":
							settings["PA_Algo"] = "Gilg"
							playerSettingsLoopA = False
						elif playerInput == "3":
							settings["PA_Algo"] = "Enk"
							playerSettingsLoopA = False
						elif playerInput == "4":
							settings["PA_Algo"] = "Random"
							playerSettingsLoopA = False
						elif playerInput == "Q" or playerInput == "q":
							settings["PA_Algo"] = "Random"
							playerSettingsLoopA = False
						else:
							print("Invalid input")
							print()
				elif playerInput == "2":
					playerSettingsLoopB = True
					while playerSettingsLoopB == True:
						print("Set Player B's algorithm")
						print("1: Human")
						print("2: Gilgamesh")
						print("3: Enkidu")
						print("4: Random")
						playerInput = input("Input: ")
						print()
						if playerInput == "1":
							settings["PB_Algo"] = "Human"
							playerSettingsLoopB = False
						elif playerInput == "2":
							settings["PB_Algo"] = "Gilg"
							playerSettingsLoopB = False
						elif playerInput == "3":
							settings["PB_Algo"] = "Enk"
							playerSettingsLoopB = False
						elif playerInput == "4":
							settings["PB_Algo"] = "Random"
							playerSettingsLoopB = False
						elif playerInput == "Q" or playerInput == "q":
							settings["PB_Algo"] = "Random"
							playerSettingsLoopB = False
						else:
							print("Invalid input")
							print()
				else:
					print("Invalid input")
					print()
		elif playerInput == "2":
			pathSettingsLoop = True
			while pathSettingsLoop == True:
				print("Path Settings Menu:")
				print("Which path is wanted:")
				print("1: Short")
				print("2: Long")
				print("3: There and Back Again")
				print("4: Exit Gate Path")
				print("5: Invasion")
				print()
				print("To quit settings menu  - press Q")
				playerInput = input("Input number: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					pathSettingsLoop = False
				elif playerInput == "1":
					settings["Path"][0][0] = 1
					settings["Path"][1][0] = 0
					settings["Path"][2][0] = 0
					settings["Path"][3][0] = 0
					settings["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "2":
					settings["Path"][0][0] = 0
					settings["Path"][1][0] = 1
					settings["Path"][2][0] = 0
					settings["Path"][3][0] = 0
					settings["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "3":
					settings["Path"][0][0] = 0
					settings["Path"][1][0] = 0
					settings["Path"][2][0] = 1
					settings["Path"][3][0] = 0
					settings["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "4":
					settings["Path"][0][0] = 0
					settings["Path"][1][0] = 0
					settings["Path"][2][0] = 0
					settings["Path"][3][0] = 1
					settings["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "5":
					settings["Path"][0][0] = 0
					settings["Path"][1][0] = 0
					settings["Path"][2][0] = 0
					settings["Path"][3][0] = 0
					settings["Path"][4][0] = 1
					pathSettingsLoop = False
				else:
					print("Invalid input")
					print()
		elif playerInput == "3":
			counterSettingsLoop = True
			while counterSettingsLoop == True:
				print("Counter Settings Menu:")
				print("Input the number of counters you want to play with")
				print("The default is 7")
				print()
				print("To quit settings menu  - press Q")
				playerInput = input("Input: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					counterSettingsLoop = False
				elif playerInput.isnumeric() and int(playerInput) != 0:
					settings["CntrNum"] = int(playerInput)
					counterSettingsLoop = False
				else:
					print("Invalid input")
					print()
		elif playerInput == "4":
			diceSettingsLoop = True
			while diceSettingsLoop == True:
				print("Dice Settings Menu:")
				print("Input the number of dice you want to play with")
				print("The default is 4")
				print()
				print("To quit settings menu - press Q")
				playerInput = input("Input: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					diceSettingsLoop = False
				elif playerInput.isnumeric() and int(playerInput) != 0:
					settings["DiceNum"] = int(playerInput)
					diceSettingsLoop = False
				else:
					print("Invalid input")
					print()
		elif playerInput == "5":
			autoSettingsLoop = True
			while autoSettingsLoop == True:
				print("Auto Play Settings Menu:")
				print("Auto play is mainly used for testings and AI learning")
				print("Do you want to start auto play - y/n")
				print()
				print("To quit settings menu - press Q")
				playerInput = input("Input: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					autoSettingsLoop = False
				elif playerInput == "Y" or playerInput == "y" and (settings["PA_Algo"] == "Human" or settings["PB_Algo"] == "Human"):
					print("CANNOT AUTO PLAY WHEN A PLAYER HAS A HUMAN ALGORITHEM")
					print()
				elif playerInput == "Y" or playerInput == "y":
					settings["AutoPlayOn"] = True
					autoSettingsLoop2 = True
					while autoSettingsLoop2 == True:
						print("How many games do you want played")
						print("To quit settings menu - press Q")
						playerInput = input("Input number: ")
						print()
						if playerInput == "Q" or playerInput == "q":
							autoSettingsLoop2 = False
						elif playerInput.isnumeric():
							settings["AutoPlayLoops"] = int(playerInput)
							autoSettingsLoop3 = True
							while autoSettingsLoop3 == True:
								print("Do you want to auto play to print event - y/n")
								print("To quit settings menu - press Q")
								playerInput = input("Input: ")
								print()
								if playerInput == "Q" or playerInput == "q":
									autoSettingsLoop3 = False
								elif playerInput == "Y" or playerInput == "y":
									settings["AutoPlayOutput"] = True
									print("Auto play will start now")
									input("Press Enter to continue")
									return settings
									settingsLoop = False
								elif playerInput == "N" or playerInput == "n":
									settings["AutoPlayOutput"] = False
								else:
									print("Invalid input")
									print()
						else:
							print("Invalid input")
							print()
				elif playerInput == "N" or playerInput == "n":
					settings["AutoPlayOn"] = False
					autoSettingsLoop = False
				else:
					print("Invalid input")
					print()
		elif playerInput == "6":
			settings = {
				"PA_Algo": "Random",
				"PB_Algo": "Random",
				"Path":	[[1, "Short "], [0, "Long "], [0, "There and Back Again "], [0, "Exit Gate Path "], [0, "Invasion "]],
				"CntrNum": 7,
				"DiceNum": 4,
				"AutoPlayOn": False,
				"AutoPlayLoops": 1,
				"AutoPlayOutput": True
			}
			return settings
		else:
			print("Invalid input")
			print()

### Variables ###
# NB - some of the valuables defined here are NOT the same as the ones used in functions (global vs local)
#      they are mainly here to show how they are formated

#these boolean while loop variables work as such

#Loop = True
#while Loop == True:
#	# do some things
#	If you want to do this loop again:
#		Pass
#	Else:
#		Loop = False
# 		#this will cause the loop to not continue
#end while

gameLoop = None
turnLoop = None
playerInputLoop = None
randomInputLoop = None
firstTurnLoop = None
moveLoop = None
settingsLoop = None

# turn counter 
turn = 0
# bool to detriment whose turn it is
# if isPAsTurn = true, it is player A's turn - else it is player B's turn
isPAsTurn = None

# shows how the board is formated
row1 = ["00","00","00","00","XX","XX","00","00"]
row2 = ["00","00","00","00","00","00","00","00"]
row3 = ["00","00","00","00","XX","XX","00","00"]
board = [row1, row2, row3]

# the path dictionary stores the list of tiles in each path - stores as tuples
# each path has a path A and path B for each player respectively
paths = {
	"Short A": (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (1,8), (1,7), (1, 100), (2, 100), (3, 100), (4, 100)
		),
	"Short B": (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (3,8), (3,7), (1, 100), (2, 100), (3, 100), (4, 100)
		),
	"Long A": (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7), (1, 100), (2, 100), (3, 100), (4, 100)
		),
	"Long B": (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7), (1, 100), (2, 100), (3, 100), (4, 100)
		),
	"There and Back Again A": (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (1,1), (1,2), (1,3), (1,4), (1, 100), (2, 100), (3, 100), (4, 100)
	),
	"There and Back Again B": (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (3,1), (3,2), (3,3), (3,4), (1, 100), (2, 100), (3, 100), (4, 100)
	),
	"Exit Gate Path A": (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (1, 100), (2, 100), (3, 100), (4, 100)
	),
	"Exit Gate Path B": (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (1, 100), (2, 100), (3, 100), (4, 100)
	),
	"Invasion A": (
		(0,0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (3,7), (3,8), (2,8), (1,8), (1,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (3,1), (3,2), (3,3), (3,4), (1, 100), (2, 100), (3, 100), (4, 100)
	),
	"Invasion B": (
		(0,0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (1,7), (1,8), (2,8), (3,8), (3,7),
		(2,7), (2,6), (2,5), (2,4), (2,3), (2,2), (2,1), (1,1), (1,2), (1,3), (1,4), (1, 100), (2, 100), (3, 100), (4, 100)
	),
}

# which tiles are rosettes
rosette = ((1, 1), (3, 1), (1, 7), (3, 7), (2, 4))

# settings is a dictionary containing the game settings
settings = {
	"PA_Algo": "Random",
	"PB_Algo": "Random",
	"Path":	[[1, "Short "], [0, "Long "], [0, "There and Back Again "], [0, "Exit Gate Path "], [0, "Invasion "]],
	"CntrNum": 7,
	"DiceNum": 4,
	"AutoPlayOn": False,
	"AutoPlayLoops": 1,
	"AutoPlayOutput": True
}

### Initialize Objects ###
PA = Player("A")
PB = Player("B")

# dictionary used to define Player.notMe 
otherPlayer = {"B": PA, "A": PB}
PA._defOther()
PB._defOther()

# Start
print()
print("THE ROYAL GAME OF UR")
print()


gameLoop = True
while gameLoop == True:
	# if auto play is on
	if settings["AutoPlayOn"] == True:
		# run x games - where x a number determined by settings
		for x in range(0, settings["AutoPlayLoops"]):
			print("Auto Playing - Count: " + str(x+1))
			print()
			GAME(isPAsTurn, x)
		#next x
		settings["AutoPlayOn"] = False
	# if normal play
	else:
		#print menu options
		print("Menu:")
		print("Press 1 to start new game")
		print("Press 2 to for game settings")
		print("Press 3 to quit")
		playerInput = input("Input: ")
		print()

		# do inputted action
		if playerInput == "1":
			GAME(isPAsTurn, 0)
		elif playerInput == "2":
			settings = SETTINGS(settings)
			# print(str(settings))
		elif playerInput == "3":
			print("quit")
			gameLoop = False
		else:
			print("Invalid Input - Restarting Menu")
			print()
#end while