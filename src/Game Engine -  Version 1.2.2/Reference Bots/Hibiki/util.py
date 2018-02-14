import pickle


#Global variables accross all files
def init():

	global command_file, place_ship_file, game_state_file, \
			output_path, MAP_SIZE, SHIPS, DIRECTIONS, TO_BE_PLACED, OCCUPIED, \
			SUNK_CELLS, DESTROYED, WEAPONS

	command_file = "command.txt"
	place_ship_file = "place.txt"
	game_state_file = "state.json"
	output_path = '.'

	MAP_SIZE = 10
	SHIPS = [('Battleship', 4),
	             ('Carrier', 5),
	             ('Cruiser', 3),
	             ('Destroyer', 2),
	             ('Submarine', 3)
	             ]
	DIRECTIONS = ['east',
	                  'south'
	                 ]

	TO_BE_PLACED = []
	OCCUPIED = []
	SUNK_CELLS = []
	DESTROYED = []
	WEAPONS = {
		'SingleShot' : 1,
		'DoubleShot' : 2,
		'DoubleShotHorizontal' : 3,
		'CornerShot' : 4,
		'DiagonalCrossShot' : 5,
		'CrossShot' : 6,
		'SeekerMissile' : 7
	}

	with open('destroyed', 'rb') as f:
		DESTROYED = pickle.load(f)

	with open('sunk', 'rb') as f:
		SUNK_CELLS = pickle.load(f)