###########################################
# Game code for The Game of UR ~ v2 ~ SAB #
###########################################
#                 Main.py                 #
###########################################

from Game.UR import *
from Game.Settings import *
from Game.Data import paths, gameData

# Start
print()
print("THE ROYAL GAME OF UR")
print()

gameLoop = True
while gameLoop == True:

	# if auto play is on
	if gameData["AutoPlayOn"] == True:
		# run x games - where x a number determined by gameData
		for x in range(0, gameData["AutoPlayLoops"]):
			print("Auto Playing - Count: " + str(x+1))
			print()
			#GAME(gameData)
		#next x
		gameData["AutoPlayOn"] = False
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
			GAME(paths, gameData)
		elif playerInput == "2":
			gameData = SETTINGS(gameData)
			# print(str(gameData))
		elif playerInput == "3":
			print("quit")
			gameLoop = False
		else:
			print("Invalid Input - Restarting Menu")
			print()
#end while