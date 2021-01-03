###########################################
# Game code for The Game of UR ~ v2 ~ SAB #
###########################################
#           Game Settings Code            #
###########################################

# this gameData function will do a series of boolean while loops to do menus
# saving the gameData in a the dictionary variable "gameData"
# it then returns the gameData variables
# read the prints to determine what each input does
def SETTINGS(gameData):
	gameDataLoop = True
	while gameDataLoop == True:
		print("Settings Menu:")
		print("For player gameData     - press 1")
		print("For path gameData       - press 2")
		print("For counter gameData    - press 3")
		print("For dice gameData       - press 4")
		print("For auto play gameData  - press 5")
		print("To set default gameData - press 6")
		print()
		print("To quit gameData menu  - press Q")
		print("Q to quit works in all gameData")
		playerInput = input("Input: ")
		print()
		if playerInput == "Q" or playerInput == "q":
			return gameData
		elif playerInput == "1":
			playerSettingsLoop = True
			while playerSettingsLoop == True:
				print("Player Settings Menu:")
				print("To change Player A's algorithm - press 1")
				print("To change Player B's algorithm - press 2")
				print()
				print("To quit gameData menu - press Q")
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
							gameData["PA_Algo"] = "Human"
							playerSettingsLoopA = False
						elif playerInput == "2":
							gameData["PA_Algo"] = "Gilg"
							playerSettingsLoopA = False
						elif playerInput == "3":
							gameData["PA_Algo"] = "Enk"
							playerSettingsLoopA = False
						elif playerInput == "4":
							gameData["PA_Algo"] = "Random"
							playerSettingsLoopA = False
						elif playerInput == "Q" or playerInput == "q":
							gameData["PA_Algo"] = "Random"
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
							gameData["PB_Algo"] = "Human"
							playerSettingsLoopB = False
						elif playerInput == "2":
							gameData["PB_Algo"] = "Gilg"
							playerSettingsLoopB = False
						elif playerInput == "3":
							gameData["PB_Algo"] = "Enk"
							playerSettingsLoopB = False
						elif playerInput == "4":
							gameData["PB_Algo"] = "Random"
							playerSettingsLoopB = False
						elif playerInput == "Q" or playerInput == "q":
							gameData["PB_Algo"] = "Random"
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
				print("To quit gameData menu  - press Q")
				playerInput = input("Input number: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					pathSettingsLoop = False
				elif playerInput == "1":
					gameData["Path"][0][0] = 1
					gameData["Path"][1][0] = 0
					gameData["Path"][2][0] = 0
					gameData["Path"][3][0] = 0
					gameData["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "2":
					gameData["Path"][0][0] = 0
					gameData["Path"][1][0] = 1
					gameData["Path"][2][0] = 0
					gameData["Path"][3][0] = 0
					gameData["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "3":
					gameData["Path"][0][0] = 0
					gameData["Path"][1][0] = 0
					gameData["Path"][2][0] = 1
					gameData["Path"][3][0] = 0
					gameData["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "4":
					gameData["Path"][0][0] = 0
					gameData["Path"][1][0] = 0
					gameData["Path"][2][0] = 0
					gameData["Path"][3][0] = 1
					gameData["Path"][4][0] = 0
					pathSettingsLoop = False
				elif playerInput == "5":
					gameData["Path"][0][0] = 0
					gameData["Path"][1][0] = 0
					gameData["Path"][2][0] = 0
					gameData["Path"][3][0] = 0
					gameData["Path"][4][0] = 1
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
				print("To quit gameData menu  - press Q")
				playerInput = input("Input: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					counterSettingsLoop = False
				elif playerInput.isnumeric() and int(playerInput) != 0:
					if int(playerInput) < 10:
						gameData["CntrNum"] = int(playerInput)
						counterSettingsLoop = False
					else:
						print("Invalid input - Number to big (< 10)")
						print()
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
				print("To quit gameData menu - press Q")
				playerInput = input("Input: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					diceSettingsLoop = False
				elif playerInput.isnumeric() and int(playerInput) != 0:
					gameData["DiceNum"] = int(playerInput)
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
				print("To quit gameData menu - press Q")
				playerInput = input("Input: ")
				print()
				if playerInput == "Q" or playerInput == "q":
					autoSettingsLoop = False
				elif playerInput == "Y" or playerInput == "y" and (gameData["PA_Algo"] == "Human" or gameData["PB_Algo"] == "Human"):
					print("CANNOT AUTO PLAY WHEN A PLAYER HAS A HUMAN ALGORITHEM")
					print()
				elif playerInput == "Y" or playerInput == "y":
					gameData["AutoPlayOn"] = True
					autoSettingsLoop2 = True
					while autoSettingsLoop2 == True:
						print("How many games do you want played")
						print("To quit gameData menu - press Q")
						playerInput = input("Input number: ")
						print()
						if playerInput == "Q" or playerInput == "q":
							autoSettingsLoop2 = False
						elif playerInput.isnumeric():
							gameData["AutoPlayLoops"] = int(playerInput)
							autoSettingsLoop3 = True
							while autoSettingsLoop3 == True:
								print("Do you want to auto play to print event - y/n")
								print("To quit gameData menu - press Q")
								playerInput = input("Input: ")
								print()
								if playerInput == "Q" or playerInput == "q":
									autoSettingsLoop3 = False
								elif playerInput == "Y" or playerInput == "y":
									gameData["AutoPlayOutput"] = True
									print("Auto play will start now")
									input("Press Enter to continue")
									return gameData
									gameDataLoop = False
								elif playerInput == "N" or playerInput == "n":
									gameData["AutoPlayOutput"] = False
								else:
									print("Invalid input")
									print()
						else:
							print("Invalid input")
							print()
				elif playerInput == "N" or playerInput == "n":
					gameData["AutoPlayOn"] = False
					autoSettingsLoop = False
				else:
					print("Invalid input")
					print()
		elif playerInput == "6":
			gameData = {
				"PA_Algo": "Random",
				"PB_Algo": "Random",
				"Path":	[[1, "Short "], [0, "Long "], [0, "There and Back Again "], [0, "Exit Gate Path "], [0, "Invasion "]],
				"CntrNum": 7,
				"DiceNum": 4,
				"AutoPlayOn": False,
				"AutoPlayLoops": 1,
				"AutoPlayOutput": True,
				"rosette": ((1, 1), (3, 1), (1, 7), (3, 7), (2, 4))
			}
			return gameData
		else:
			print("Invalid input")
			print()