#############################################
# Game code for The Game of UR ~ v0.1 ~ SAB #
#############################################

'''
TO DO:
- End of track/finishing machanics
- Menu - incudes rule controles
'''

### imports ###
import random	# allows the creation of random numbers

### variables ###
turn_isPlayerAsTurn = None	# Is it player A's turn? - controls who's turn it is - True = player A turn, False = player B turn, initialised to Null
win_playerAWin = None		# Has player A win? - controls who has won - True = player A won, False = player B won, initialised to Null

diceNum = 4		# how many dice are in play - TO DO game option
diceRules = 1	# what are the current dice rules - TO DO game option

counterNum = 7	# How many counters in play - TO DO game 

turn = 0 # what turn is it

### routes ###
# 1. Short path 
path = 1
r1_A = [[0, 0], [1,4], [1,3], [1,2], [1,1], [2,1], [2,2], [2,3], [2,4], [2,5], [2,6], [2,7], [2,8], [1,8], [1,7], [0, 100], [0, 100], [0, 100], [0, 100]]
r1_B = [[0, 0], [3,4], [3,3], [3,2], [3,1], [2,1], [2,2], [2,3], [2,4], [2,5], [2,6], [2,7], [2,8], [3,8], [3,7], [0, 100], [0, 100], [0, 100], [0, 100]]

#others (TO DO different paths and game options)
r2_A = [[],[]]
r3_A = [[],[]]
r4_A = [[],[]]
r5_A = [[],[]]

### Classes ###
# Clases all start with a capital letter 
# ___init___ is the function call when an object is instanciated
# _properties is a function that lists the details of an object

# The Player Class
class Player(object):
	def __init__(self, name):
		self.name = name	# Players name - definied on instanciation
		self.score = 0		# What is the players score
		self.counters = []	# A list containing counter objects beloning to the player

		#Sets the route this player will take - detemined by the players name and the previously set game rule - TO DO game options
		if name == "Player A":
			if path == 1:
				self.route = r1_A
			elif path == 2:
				pass
			elif path == 3:
				pass
			elif path == 4:
				pass
			elif path == 5:
				pass 
		if name == "Player B":
			if path == 1:
				self.route = r1_B
			elif path == 2:
				pass
			elif path == 3:
				pass
			elif path == 4:
				pass
			elif path == 5:
				pass

		# Creates all the counters in the self.counters list
		i = 0
		while i < counterNum:
			i = i + 1
			self.counters.insert(i, Counter(i, self)) 
			# ^ insert a counter in the ith position of the list self.counters - with master self

	# Function to set all this players counters to can move 
	# this is done at the start of each round - canMove is set to false if a couter can't move this turn
	# set to true becouse it might be able to move next turn
	def _resetCounters(self):
		for counter in self.counters:
			counter.canMove = True

	# Function to check if this player has won
	def _hasWon(self):
		pass
		# TO DO - end game machaincs
		# self.score exists

	def _properties(self):
		i = 0
		for counter in self.counters:
			i = i + 1
			counter._properties(i)

# The Counter Class
class Counter(object):
	def __init__(self, number, master):
		self.master = master	# Player Object - what player does this belong too
		self.number = number	# "name" of the counter
		self.space = 0			# What is position of this counter on the path
		self.blankSide = False 	# what way up is this counter - TO DO different paths
		self.canMove = True 	# can this counter move - has it already bean checked
		self.isFinished = False # has this counter finished the path - is off board at the end

	# Function to check if this counter can move
	def _canMove(self, roll):
		DiceScore = roll
		newPosition = _newPosition(self.master, self, roll)

		# print("Position: " + str(position))

		if self.number <= counterNum: #if counter is in play
			#print()
			#print("is in play")
			if self.canMove == True: #and counter can move
				#print("can move")
				if self.space < len(self.master.route): #and counter hasn't finished
					#print("hasn't finished")
					#does the new position contain a friendly counter
					#print()
					#print(self.master.counters)
					for counter in self.master.counters:
						if counter != self:
							#print()
							#print(str(newPosition) + " " + str(self.master.name) + " " + str(self.number) + " " + str(roll))
							#print(str(_position(counter.master, counter)) + " " + str(counter.master.name) + " " + str(counter.number))
							#print()
							if newPosition == _position(counter.master, counter):#if yes
								self.canMove = False
								print("Tile is occupied by friendly")
								return False
							else:#if no
								#print("place doesn't contain a friendly counter")
								#does my new position contain an enemy counter ON A ROSETTE
								if self.master == playerA:
									for counter in playerB.counters:
										if newPosition == _position(counter.master, counter) and board._isOnRosette(counter):#if yes
											self.canMove = False
											print("Tile is occupied but an enemy and they are safe")
											return False
										else:#if no
											#print("place doesn't contain an enemy counter ON A ROSETTE")
											pass
								elif self.master == playerB:
									for counter in playerA.counters:
										if newPosition == _position(counter.master, counter) and board._isOnRosette(counter):#if yes
											self.canMove = False
											print("Tile is occupied but an enemy and they are safe")
											return False
										else:#if no
											#print("place doesn't contain an enemy counter ON A ROSETTE")
											pass					
				else:
					self.canMove = False
					print("Counter has finished")
					return False
			else:
				self.canMove = False
				print("Counter has already been checked and can't move")
				return False
		else:
			self.canMove = False
			print("Counter is no in play")
			return False

		return True

	def _properties(self, number):
		if self.blankSide == False:
			face = "blank side up"
		else: 
			face = "spot side up"

		if self.isFinished == False:
			finish = "not finished."
		else:
			finish = "finished."
		if self.master == playerA or self.master == playerB:
			print(self.master.name + "'s counter " + str(number) + " is at " + str(_position(self.master, self)) + ". It is " + face + " and has " + finish)
		else:
			print("Counter " + str(number) + " is at " + str(_position(self.master, self)) + ". It is " + face + " and has " + finish)

# THe Board Class
class Board(object):
	def __init__(self):
		# creates 3 lists of rows and on list of rows to make a Python array - list of lists
		self.row1 = [["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0]]
		self.row2 = [["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0]]
		self.row3 = [["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0]]
		self.board = [self.row1, self.row2, self.row3]
		# Where are the rossetes on this board
		self.rosettes = [[1, 1], [3, 1], [1, 7], [3, 7], [2, 4]]

	# Function to print an "image" of the board showing were all the counters are
	def _show(self, playerA, playerB):
		# Initialise the board to clear
		self.row1 = [["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0]]
		self.row2 = [["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0]]
		self.row3 = [["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0], ["0",0]]
		self.board = [self.row1, self.row2, self.row3]

		# Where are all the counters
		for counter in playerA.counters:
			i = 0
			for row in self.board:
				i = i + 1
				# If they are in a space
				if _position(playerA, counter)[0] == i:
					row = _position(playerA, counter)[0]
					columb = _position(playerA, counter)[1]
					# "Draw" them in that space
					self.board[row -1][columb -1] = ["A", counter.number]

		# Where are all the counters
		for counter in playerB.counters:
			i = 0
			for row in self.board:
				i = i + 1
				if _position(playerB, counter)[0] == i:
					row = _position(playerB, counter)[0]
					columb = _position(playerB, counter)[1]
					# "Draw" them in that space
					self.board[row -1][columb -1] = ["B", counter.number]

		# Print the board
		print(self.board[1 -1][0:8])
		print(self.board[2 -1][0:8])
		print(self.board[3 -1][0:8])

	# Is a given counter on a rosette
	def _isOnRosette(self, counter):
		for aRosetteTile in self.rosettes:
			if _position(counter.master, counter) == aRosetteTile:
				return True
			else:
				return False

### Functions ###
# all functions start with an underscore

# dice role function
def _diceRole():
	score = 0	# Dice score
	i = 0		# Dice counter
	#for all dice
	while i < diceNum:
		i = i + 1
		roll = random.randint(0, 1) # roll the dice
		score = score + roll 		# and add the number to the total dice score
		# Prints for test perposes
		#print("Role " + str(i) + ":")
		#print("role = " + str(role))
		#print("score = " + str(score))
	return score
#print("Dice score: " + str(_diceRole()))

# Function to determin who does first
def _goesFirst():
	# Each player rolls the dice
	startScore_playerA = _diceRole()
	startScore_playerB = _diceRole()
	#print(startScore_playerA)
	#print(startScore_playerB)

	if startScore_playerA == startScore_playerB: 	# If the dice rolls are the same
		turn_isPlayerAsTurn = _goesFirst()			# Role again
	elif startScore_playerA > startScore_playerB:	# If A rolled higher - they go first
		turn_isPlayerAsTurn = True 					
	elif startScore_playerA < startScore_playerB:	# If B rolled higher - they go first 
		turn_isPlayerAsTurn = False
	return turn_isPlayerAsTurn						# Return who goes first

# what is the position vector of a counter - returns list, [row, columb]
def _position(player, counter):
	space = player.counters[(counter.number-1)].space
	return player.route[space]

# what is the position vector of a counter after it has moved - returns list, [row, columb]
def _newPosition(player, counter, roll):
	space = player.counters[(counter.number-1)].space
	return player.route[space + roll]

# Runs when human player needs to input a counter pick - also includes debug controles
def _help(playerInput, player, diceScore):
	if playerInput in ["1", "2", "3", "4", "5", "6", "7", "h", "H"]:
		# the H input can be used to output some information heling with debugging
		# reading the printed information can be used to tell what does what
		if playerInput in ["h", "H"]:
			print("Help Menu")
			print("- Input must be between number between 1 and 7")
			print("- this is used to determin which counter moves")
			print("- To input again input 1")
			print("- To view board press 2")
			print("- To view a counters position press 3")
			print("- To quit press 4")
			print("- default input is 1")
			whatDo = input("What do you want to do: ")
			if whatDo not in ["1", "2", "3", "4"]:
				return _help(playerInput, player, diceScore)
			else:
				if whatDo == "1":
					return _pickCounterToMove(player, diceScore)
				elif whatDo == "2":
					board._show(playerA, playerB)
					return _help(playerInput, player, diceScore)
				elif whatDo == "3":
					showCounter = ""
					showCounterPlayer = ""
					while showCounterPlayer not in ["Q", "q"]:
						showCounter = ""
						showCounterPlayer = ""
						showCounterPlayer = input("What player are we looking at, A or B (Q for quit): ")
						if showCounterPlayer in ["A","a","B","b"]:
							while showCounter not in ["Q", "q"]:
								print("Looking at Player " + showCounter)
								showCounter = ""
								showCounter = input("What counter do you want to see - num between 1 and 7 (Q for quit): ")
								if showCounter in ["1", "2", "3", "4", "5", "6", "7"]:
									if showCounterPlayer in ["a", "A"]:
										print("Player " + showCounterPlayer + "'s counter " + showCounter + " is at " + str(_position(player, player.counters[(int(showCounter) -1)])))
									elif showCounterPlayer in ["b", "B"]:
										print("Player " + showCounterPlayer + "'s counter " + showCounter + " is at " + str(_position(player, player.counters[(int(showCounter) -1)])))
									else:
										pass
								else:
									pass
						else:
							pass
				elif whatDo == "4":
					print("quit")
					#quit()
					print("No quiting during test")
					return _help(playerInput, player, diceScore)
				else:
					return _help(playerInput, player, diceScore)
		else:
			return int(playerInput)
	else:
		print("Invalid input - Input must be between number between 1 and 7 - Input H for help menu")
		return _pickCounterToMove(player, diceScore)

# which counter is going to move
def _pickCounterToMove(player, diceScore):
	if player == playerB:
		pickedCounter = random.randint(1, 7)  #pick a random counter to move for test perposes
	elif player == playerA:
		pickedCounter = random.randint(1, 7)  #pick a random counter to move for test perposes
		'''
		playerInput = input('Pick a counter to move (H - help): ') # Player inputs a counter to move
		#pickedCounter = random.randint(1, 7)  #pick a random counter to move for test perposes

		pickedCounter = _help(playerInput, player, diceScore)
		'''

	print("pickedCounter is " + str(pickedCounter)) # Print the counter picked

	# If the coutner cannot move
	if player.counters[pickedCounter-1]._canMove(diceScore) == False:
		print("counter can't move")								# Tell them
		pickedCounter = _pickCounterToMove(player, diceScore) 	# Pick a new counter
		return pickedCounter 									# return new counter picked
	else:														# else
		return pickedCounter 									# return counter picked

# Do a turn function
def _Turn(player, turn):
	player._resetCounters()		# Reset counters

	turn = turn + 1		# Incroment the turn counter
	print()
	board._show(playerA, playerB) 	# Show the board
	print()
	print(player.name + "'s turn - Turn: " + str(turn))	# Say who's turn it is

	diceScore = _diceRole()					# Roll the dice 	
	print()									# and
	print("You rolled a " + str(diceScore))	# print result

	if diceScore == 0:						# if you rolled a 0
		if player == playerA:				# turn ends 
			return _Turn(playerB, turn)		# and other player takes a turn
		if player == playerB:				#
			return _Turn(playerA, turn)		#

	# pick a counter
	pickedCounter = _pickCounterToMove(player, diceScore)

	# move that counter a number of spaces equal to the dice score
	player.counters[pickedCounter -1].space = player.counters[pickedCounter -1].space + diceScore
	
	# check if the counter landed on an enemy counter
	if player == playerA:
		for counter in playerB.counters:
			if _position(player, player.counters[pickedCounter -1]) == _position(playerB, counter): # if yes
				print("Enemy counter captured")														# tell player
				counter.space = 0																	# and enemy coutner returns to the start
				print("Enemy counter " + str(counter.number) + " is now in position " + str(_position(counter.master, counter)))
	elif player == playerB:
		for counter in playerA.counters:
			if _position(player, player.counters[pickedCounter -1]) == _position(playerA, counter): # if yes
				print("Enemy counter captured")														# tell player
				counter.space = 0																	# and enemy coutner returns to the start
				print("Enemy counter " + str(counter.number) + " is now in position " + str(_position(counter.master, counter)))

	# is counter new position a rosette
	if board._isOnRosette(player.counters[(pickedCounter -1)]):	# if yes
		return _Turn(player, turn)								# go again
	else:														# if no
		if player == playerA:									# other player goes
			return _Turn(playerB, turn)
		if player == playerB:
			return _Turn(playerA, turn)

### Initialise Objects ###
playerA = Player("Player A")
playerB = Player("Player B")
board = Board()

# playerA._properties()
# playerB._properties()

### Decide who does first ###
turn_isPlayerAsTurn = _goesFirst()

if turn_isPlayerAsTurn == True:
	print("Player A goes first")
else:
	print("Player B goes first")

# Function to start game
def _game(playerA, playerB, turn_isPlayerAsTurn):
	if turn_isPlayerAsTurn == True:
		return _Turn(playerA, turn)
	else:
		return _Turn(playerB, turn)

# start the game and see who wins
win_playerAWin = _game(playerA, playerB, turn_isPlayerAsTurn)

'''
TO DO: 
- End of track/finishing machanics
- Menu - incudes rule controles
'''