import argparse
import json
import os
from random import choice
from operator import itemgetter, attrgetter, methodcaller

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
kebutuhan = "kebutuhan.txt"
output_path = '.'
map_size = 0


def main(player_key):
    global map_size
    # Retrieve current game state
    with open(os.path.join(output_path, game_state_file), 'r') as f_in:
        state = json.load(f_in)
    map_size = state['MapDimension']
    if state['Phase'] == 1:
        place_ships()
    else:
        fire_shot(state)


def output_shot(x, y):
    move = 1  # 1=fire shot command code
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

def isMentok(x, y):
    if ()


def fire_shot(gamestate):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)

    cells = gamestate['OpponentMap']['Cells']
    # currEnergy = gamestate['PlayerMap']['Owner']['Energy']
    # size = gamestate['MapDimension']
    #
    # lastShot = [elem for elem in cells if elem.Damaged || elem.Missed][-1]
    #
    # try:

    #
    # else:
    #     x = lastShot['X']
    #     y = lastShot['Y']
    #
    #     if(x + 2 < size):
    #         x += 2
    #     else:
    #         x = 0
    #         y ++
    #
    #     if(y >= size):
    #         AlternateRandomShot(gamestate)
    #

    targets = []
    for cell in cells:
        if not cell['Damaged'] and not cell['Missed']:
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)
    target = choice(targets)
    lastShot = {"Kembali":(2,3),"Sekarang":(1,3),"kiri":0,"kanan":0,"atas":0,"bawah":0,"fase":1,"jumlahhancur":0}
    with open(os.path.join(output_path, "..\..\data.txt"), 'w') as f_out:
	       json.dump(lastShot,f_out)
    output_shot(*target)
    return


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west
# S : Submarine (3), Singleshot (1), SeekerMissle (36)
# B : Battleship (4), Singleshot (1), DiagonalCrossShot (36) x
# C : Carrier (5), Singleshot (1), CornerShot (30) pojok doang
# R : Cruser (3), Singleshot (1), CrossShot (42) +
# D : Destroyer (2), Singleshot (1), DoubleShot (24)
    if (map_size == 7):
        ships = ['Battleship 3 1 East',
             'Carrier 2 6 East',
             'Cruiser 0 3 north',
             'Destroyer 5 3 East',
             'Submarine 2 2 north'
             ]
    elif (map_size == 10):
        ships = ['Battleship 5 8 East',#
             'Carrier 8 1 north',#
             'Cruiser 2 1 north',#
             'Destroyer 5 1 north',#
             'Submarine 1 7 East'#
             ]
    else:
        ships = ['Battleship 11 3 north',#
             'Carrier 8 11 East',#
             'Cruiser 2 3 north',#
             'Destroyer 1 11 East',#
             'Submarine 5 10 north'#
             ]

    with open(os.path.join(output_path, place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
