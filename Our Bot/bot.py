import argparse
import json
import os
from random import choice
from operator import itemgetter, attrgetter, methodcaller

command_file = "command.txt"
place_ship_file = "place.txt"
game_state_file = "state.json"
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


def fire_shot(gamestate):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)

    # Game selector
    cells = gamestate['OpponentMap']['Cells']
    currEnergy = gamestate['PlayerMap']['Owner']['Energy']
    size = gamestate['MapDimension']

    # Check if the file is exist(for initial purposes)
    if (os.path.exists(os.path.join(output_path, "..\..\data.txt")) == False):
        # Dummy variable
        lastShot = {"Track":(-1,-1),"Attack":(-1,-1),"kiri":0,"kanan":0,"atas":0,"bawah":0,"fase":1,"jumlahhancur":0,"default" = 1}
        with open(os.path.join(output_path, "..\..\data.txt"), 'w') as f_out:
            json.dump(lastShot,f_out)

    # Read the file
    with open(os.path.join(output_path,"..\..\data.txt","r")) as f_in:
        data = json.load(f_in)

    # Selector
    (x1,y1) = data["Track"]
    (x2,y2) = data["Attack"]
    bKiri = data["kiri"]
    bKanan = data["kanan"]
    bAtas = data["atas"]
    bBawah = data["bawah"]
    phase = data["fase"]
    cDes = data["jumlahhancur"]
    bDefault = data["default"]

    # The initial time(skip the dummy variable)
    if (x1 == -1 and y1 == -1):
        x1 += 1
        y1 += 1
        x2 += 1
        y2 += 1

    else:
        # Search the cell
        for cell in cells:
            if (cell['X'] == x1 and cell['Y'] == y1):
                cellTrack = cell

            if (cell['X'] == x2 and cell['Y'] == y2):
                cellAttack = cell


        # if (not cellTrack['Damaged'] and not cellAttack['Damaged']):
        #     target = cellTrack['X'], cellTrack['Y']
        # else:
        #     if (cellTrack['Damaged']):

        # If hit,do the greedy to search the ship until number of opponent's map destroyed changed
        if(cellTrack['Damaged']):
            bDefault = 0

        # If we missed,move based on the Phase
        # 1: diagonal(northeast)
        # 2: diagonal(northwest)
        # 3: vertical
        # 4: horizontal
        # 5: random search
        if(bDefault):
            if(phase == 1):
                x1 += 1
                x2 += 1
                y1 += 1
                y2 += 1
                if(x1 > map_size):
                    phase = 2
                    x1 = map_size - 1
                    x2 = map_size - 1
                    y1 = 0
                    y2 = 0
            elif(phase == 2):
                x1 -= 1
                x2 -= 1
                y1 += 1
                y2 += 1
                if(y1 > map_size):
                    phase = 3
                    x1 = map_size/2
                    x2 = map_size/2
                    y1 = 0
                    y2 = 0
            elif(phase == 3):
                y1 += 1
                y2 += 1
                if(y1 > map_size):
                    phase = 4
                    y1 = map_size/2
                    y2 = map_size/2
                    x1 = 0
                    x2 = 0
            elif(phase == 4):
                x1 += 1
                x2 += 1
                if(x1 > map_size):
                    phase = 5
            else:
                (x1,y1) = randomShot(gamestate)
                (x2,y2) = randomShot(gamestate)

        else:
            if
                if (cellTrack['Missed']):
                    if (not bKiri) :
                        bKiri = 1
                    elif (not bAtas) :
                        bAtas = 1
                    elif (not bKanan) :
                        bKanan = 1
                    elif (not bBawah) :
                        bBawah = 1
                if (not bKiri):
                    x2 -= 1
                elif (not bAtas):
                    y2 += 1
                elif (not bKanan):
                    x2 += 1
                elif (not bBawah):
                    y2 -= 1


    # targets = []
    # for cell in cells:
    #     if not cell['Damaged'] and not cell['Missed']:
    #         valid_cell = cell['X'], cell['Y']
    #         targets.append(valid_cell)
    # target = choice(targets)
    if os.path.exists(os.path.join(output_path, "..\..\data.txt")) == False:
        lastShot = {"Kembali":(2,3),"Sekarang":(1,3),"kiri":0,"kanan":0,"atas":0,"bawah":0,"fase":1,"jumlahhancur":0}
        with open(os.path.join(output_path, "..\..\data.txt"), 'w') as f_out:
    	       json.dump(lastShot,f_out)

    targets = []
    for cell in cells:
        if not cell['Damaged'] and not cell['Missed']:
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)
    target = choice(targets)
    output_shot(*target)

    return

# Function to calculate destroyed opponent's ship
def hitung_hancur(gamestate):
    count = 0
    ships = gamestate['OpponentMap']['Ships']
    for ship in ships:
        if ship['Destroyed']:
            count += 1

    return count

# Function to do random shooting after the greedy part
def randomShot(gamestate):

    cells = gamestate['OpponentMap']['Cells']

    targets = []
    for cell in cells:
        if not cell['Damaged'] and not cell['Missed']:
            valid_cell = cell['X'], cell['Y']
            targets.append(valid_cell)
    target = choice(targets)

    return target

# Function to place the ship in phase 1
def place_ships():
    
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

# The main program
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    output_path = args.WorkingDirectory
    main(args.PlayerKey)
