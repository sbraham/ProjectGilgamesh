# ProjectGilgamesh
The project is a pesonal project I am attempting in my free time. The aim is to create the Royal Game of Ur (Game of 20 Square) in code and then attempt to develop and optomise a number of AIs that are capable of playing the game well.

A write up of the porject can be found at https://docs.google.com/document/d/1b853IG8McpPnswgVL88rs1z0igc1P0tiQFxjRv27MUs/edit?usp=sharing

The file Game_of_Ur-v1.py contains the initial version of the game - although notobly lacks any end game handling or menu
This was developed with the aim of finding out how the game will run and gain some intuitian about the program

The file Game_of_Ur-v2.py contains the second version of the game (WORK IN PROGRESS) - built better and runs better with a compleat menu and end of game handling
This version of the game allows for a fully functional game with human input or random input as will as a auto play feature to instantly run X number of games (only with random inputs) - this version does not yet have AI functionality

The direcotry Game_of_Ur-v3.py contains the python files that are used to run the 3rd version of this project 
this is largely a re-write as between this and v2, I worked on my ChessAI project in which I use a chess librery. This chess librery focuses largely on a Board object that stores most of the information. This is much easier then storing information in two player objects.
This program also users piece objects as well as move objects. 
These objects are defined in the script 20squares.py which itself is desinged to act as the main place for the logic of the UR game. This is imported into to main.py.
IN DEVELOPMENT v
main.py will also import Tkinter which, in a similar way to other projects, will be used to create a user interface for the player to play the game
also to be made are 
gilgamesh-gold.py
gilgamesh-gold_learingenvironment.py
