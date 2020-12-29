###########################################
# Game code for The Game of UR ~ v2 ~ SAB #
###########################################

### Imports ###
import random

### Class ###
class Player(object):
	def __init__(self, name):
		self.name = name
		self.AICheck = ("P" + self.name + "_Algo")
		self.algo = settings[self.AICheck] 

		self.cntrs = [Counter(0, self)]
		for x in range(1, settings["CntrNum"]+1):
			self.cntrs.insert(x, Counter(x, self))
		#next x

		self.path = []
		i = 0
		while settings["Path"][i][0] != 1:
			i += 1
		#end while

		pathName = (settings["Path"][i][1] + self.name)
		self.path = paths[pathName]

	def _defOther(self):
		self.notMe = otherPlayer[self.name]

	def _inputCntr(self):
		if self.algo == "Human":
			playerInputLoop = True
			while playerInputLoop == True:
				print("Input counter to move - number between 1 and " + str(settings["CntrNum"]))
				playerInput = input("Input: ")

				checkCntrSet = []
				for x in range(1, settings["CntrNum"]+1):
					checkCntrSet.insert(x, str(x))
				#next x

				if playerInput in checkCntrSet:
					return self.cntrs[int(playerInput)]
					playerInputLoop = False
				else:
					print("Invalid Input - counter must be between 1 and " + str(settings["CntrNum"]))
			#end while
		elif self.algo == "Gilg":
			pass
		elif self.algo == "Enk":
			pass
		else:
			return self.cntrs[random.randint(1, settings["CntrNum"])]

	def _turnInitialisation(self):
		for cntr in self.cntrs:
			cntr.canMove = {"bool":  True, "capture": {"bool": False, "counter": self}}

	def _show(self):
		#self.cntrs[7]._show()

		for cntr in self.cntrs:
			cntr._show()


class Counter(object):
	def __init__(self, number, master):
		self.num = number
		self.master = master
		self.pathPOS = 0
		self.boardPOS = (0,0)
		self.canMove = {"bool":  True, "capture": {"bool": False, "counter": self}}

	def _boardPOS(self):
		self.boardPOS = self.master.path[self.pathPOS]

	def _canMove(self, roll):
		self.newPathPOS = self.pathPOS + roll
		self.newBoardPOS = self.master.path[self.newPathPOS]

		if self.canMove["bool"] == True:
			for cntr in self.master.cntrs:
				if cntr.boardPOS == self.newBoardPOS:
					print("Tile occupied by own counter")
					self.canMove["bool"] = False
				else:
					pass
			#next cntr
			for cntr in self.master.notMe.cntrs:
				if cntr.boardPOS == self.newBoardPOS:
					if cntr.boardPOS in rosette:
						print("Tile occupied by oponents counter AND they are on a rosette")
						self.canMove["bool"] = False
					else:
						print("Capture!")
						self.canMove["capture"] = {"bool": True, "counter": cntr}
				else:
					pass
			#next cntr
		else:
			print("Tile has already tried to move")

		return self.canMove

	def _show(self):
		print("Player " + self.master.name + "'s counter " + str(self.num) + " is in position " + str(self.boardPOS) + " (space " + str(self.pathPOS) + ")")

### Functions ###
def _diceRoll():
	score = 0	# Dice score
	#for all dice
	for x in range(0, settings["DiceNum"]):
		roll = random.randint(0, 1) # roll the dice
		score = score + roll 		# and add the number to the total dice score
	return score

def _board():
	row1 = [0, "00","00","00","00","XX","XX","00","00"]
	row2 = [0, "00","00","00","00","00","00","00","00"]
	row3 = [0, "00","00","00","00","XX","XX","00","00"]
	board = [0, row1, row2, row3]

	for cntr in PA.cntrs:
		if cntr.boardPOS[0] != 0:
			board[cntr.boardPOS[0]][cntr.boardPOS[1]] = (cntr.master.name + str(cntr.num))
	for cntr in PB.cntrs:
		if cntr.boardPOS[0] != 0:
			board[cntr.boardPOS[0]][cntr.boardPOS[1]] = (cntr.master.name + str(cntr.num))

	print(board[1][1:8 +1])
	print(board[2][1:8 +1])
	print(board[3][1:8 +1])

	#PA._show()
	#PB._show()

def _whosTurn():
	if PAsTurn == True:
		return PA
	elif PAsTurn == False:
		return PB
	else:
		return "!!! Error - Player not yet determined !!!"

def GAME():
	while PAsTurn == None:
		PAsRoll = _diceRoll()
		PBsRoll = _diceRoll()
		if PAsRoll != PBsRoll:
			PAsTurn = (PAsRoll > PBsRoll)
	#end while

	turnLoop = True
	while turnLoop == True:
		turn += 1
		player = _whosTurn()
		player._turnInitialisation()
		print("Turn " + str(turn) + " - Player " + player.name + "'s turn")

		_board()
		print()

		roll = _diceRoll()
		print("You rolled - " + str(roll))

		if roll == 0:
			PAsTurn = not PAsTurn
		else:
			moveLoop = True
			while moveLoop == True:
				cntrPick = (player._inputCntr())
				print("Counter picked " + str(cntrPick.num))

				canMove = cntrPick._canMove(roll)

				if canMove["bool"]:
					cntrPick.pathPOS += roll
					cntrPick._boardPOS()
					moveLoop = False
					if canMove["capture"]["bool"]:
						canMove["capture"]["counter"].pathPOS = 0
						canMove["capture"]["counter"]._boardPOS()
				else:
					pass

			if cntrPick.boardPOS in rosette:
				pass
			else:
				PAsTurn = not PAsTurn

		print()

		################
		### END GAME ###
		################

	#end while

def SETTINGS():
	pass

### Variables ###
gameLoop = None
turnLoop = None
playerInputLoop = None
firstTurnLoop = None
moveLoop = None

turn = 0
PAsTurn = None

row1 = ["00","00","00","00","XX","XX","00","00"]
row2 = ["00","00","00","00","00","00","00","00"]
row3 = ["00","00","00","00","XX","XX","00","00"]
board = [row1, row2, row3]

paths = {
	"Short A": ((0, 0), (1,4), (1,3), (1,2), (1,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (1,8), (1,7), (0, 100)),
	"Short B": ((0, 0), (3,4), (3,3), (3,2), (3,1), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7), (2,8), (3,8), (3,7), (0, 100)),
	"Long A": (),
	"Long B": ()
}

rosette = ((1, 1), (3, 1), (1, 7), (3, 7), (2, 4))

# settings is a python dictionary containing the game settings
settings = {
	"PA_Algo": "Random",
	"PB_Algo": "Random",
	"Path":	((1, "Short "), (0, "Long "), (0, "There and Back Again "), (0, "Exit Gate Path "), (0, "Invasion ")),
	"CntrNum": 7,
	"DiceNum": 4,
	"DiceRules": 1,
	"AutoPlayOn": False,
	"AutoPlayLoops": 1
}

# Stats

# Initialise Objects
PA = Player("A")
PB = Player("B")
otherPlayer = {"B": PA, "A": PB}
PA._defOther()
PB._defOther()

# Start
print()
print("THE ROYAL GAME OF UR")
print()

gameLoop = True
while gameLoop == True:
	if settings["AutoPlayOn"]:
		for x in range(0, settings[AutoPlayLoops]):
			print("Auto Playing - Count: " + str(x+1))
			print()
			GAME()
		#next x
		settings["AutoPlayOn"] = False
		print()
	else:
		print("Menu:")
		print("Press 1 to start new game")
		print("Press 2 to for game settings")
		print("Press 3 to quit")
		playerInput = input("Input: ")
		print()

	if playerInput == "1":
		GAME()
		gameLoop = False
	elif playerInput == "2":
		SETTINGS()

	elif playerInput == "3":
		print("quit")
		gameLoop = False
	else:
		print("Invalid Input - Restarting Menu")
#end while
