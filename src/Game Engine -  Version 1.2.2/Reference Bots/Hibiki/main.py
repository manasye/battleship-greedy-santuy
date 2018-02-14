import argparse
import json
import os
from random import choice
import shield as shi
import ship as sh
import attack as at
import util
from atomic import en_Matrix
from atomic import p_Matrix
import pickle


#Main function
def main(player_key):
    with open(os.path.join(util.output_path, util.game_state_file), 'r') as f_in:
        util.state = json.load(f_in)

    util.MAP_SIZE = util.state['MapDimension']

    op_ships = util.state['OpponentMap']['Ships']

    for ship in op_ships:
        if ship['Destroyed'] and ship not in util.DESTROYED:
            util.DESTROYED.append(ship)
            with open('destroyed', 'wb') as f:
                pickle.dump(util.DESTROYED, f)

            for size in util.SHIPS:
                if size[0] == ship['ShipType']:
                    length = size[1]
                    break

            mark_hit_as_invalid(util.state['OpponentMap']['Cells'], length)

    if util.state['Phase'] == 1:
        with open('destroyed', 'wb') as f:
            pickle.dump([], f)

        with open('sunk', 'wb') as f:
            pickle.dump([], f)
        place_ships()
    else:
        PState = p_Matrix(util.state['PlayerMap']['Cells'],util.MAP_SIZE)
        targetCell,shieldScore = shi.shieldOn(PState)
        if ((shieldScore >= 0.5) and (util.state['PlayerMap']['Owner']['Shield']['CurrentCharges'] >= 3)) :
            turn_on_shield(*targetCell)
        else :
            fire_shot(util.state['OpponentMap']['Cells'])
        
#Write attack command to command file
def output_shot(x, y, weapon):
    move = str(util.WEAPONS[weapon['WeaponType']])
    with open(os.path.join(util.output_path, util.command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass

#Write shield command
def turn_on_shield(x,y) :
    with open(os.path.join(util.output_path, util.command_file), 'w') as f_out:
        f_out.write('8,{},{}'.format( x, y))
        f_out.write('\n')
    pass

#Mark destroyed cells as invalid (not to be recognized as damaged cells)
def mark_hit_as_invalid(opponent_map, length):
    en_map = en_Matrix(opponent_map, util.MAP_SIZE)
    for cell in opponent_map:
        if cell['Damaged'] and not (cell['X'], cell['Y']) in util.SUNK_CELLS:
            east, cell_east = check_sunk_ship(cell['X'], cell['Y'], en_map, length, 'east')
            west, cell_west = check_sunk_ship(cell['X'], cell['Y'], en_map, length, 'west')
            north, cell_north = check_sunk_ship(cell['X'], cell['Y'], en_map, length, 'north')
            south, cell_south = check_sunk_ship(cell['X'], cell['Y'], en_map, length, 'south')

            if not(east or west or north or south):
                continue

            if east:
                util.SUNK_CELLS += cell_east
            elif west:
                util.SUNK_CELLS += cell_west
            elif north:
                util.SUNK_CELLS += cell_north
            else:
                util.SUNK_CELLS += cell_south

            util.SUNK_CELLS += [(cell['X'], cell['Y'])]

    with open('YEYEYE', 'w') as f:
        f.write('HEHEHEH')

            
    with open('sunk', 'wb') as f:
        pickle.dump(util.SUNK_CELLS, f)


def check_sunk_ship(x : int, y : int, en_map, length : int, direction : str):
    result = []
    cells = []
    for i in range(length):
        if (direction == 'east') and (x+i+1 < util.MAP_SIZE) and \
            (x+i+1, y) not in util.SUNK_CELLS:
            result.append(en_map.cellDmgdStat(x+i+1, y))
            cells.append((x+i+1, y))

        elif (direction == 'west') and (x-i-1 >= 0) and \
            (x-i-1, y) not in util.SUNK_CELLS:
            result.append(en_map.cellDmgdStat(x-i-1, y))
            cells.append((x-i-1, y))

        elif (direction == 'north') and (y+i+1 < util.MAP_SIZE) and \
            (x, y+i+1) not in util.SUNK_CELLS:
            result.append(en_map.cellDmgdStat(x, y+i+1))
            cells.append((x, y+i+1))

        elif (direction == 'south') and (y-i-1 >= 0) and \
            (x, y-i-1) not in util.SUNK_CELLS:
            result.append(en_map.cellDmgdStat(x, y-i-1))
            cells.append((x, y-i-1))

        else:
            result.append(False)

    with open('YEYEYEXX', 'w') as f:
        f.write('HEHEHEH')

    for r in result[:-1]:
        if  not r:
            return False, []

    return (len(cells) == length and not result[-1]), cells[:-1]



#Attack
def fire_shot(opponent_map):
    EnState = en_Matrix(opponent_map,util.MAP_SIZE)

    target, weapon = at.single_attack(EnState)
    output_shot(*target, weapon)

#This should be obvious
def place_ships():
    ships = sh.place_everything()

    with open(os.path.join(util.output_path, util.place_ship_file), 'w') as f_out:
        for ship in ships:
            f_out.write(ship)
            f_out.write('\n')
    return

#Initialize all files and states
#Run the main function
if __name__ == '__main__':
    util.init()
    parser = argparse.ArgumentParser()
    parser.add_argument('PlayerKey', nargs='?', help='Player key registered in the game')
    parser.add_argument('WorkingDirectory', nargs='?', default=os.getcwd(), help='Directory for the current game files')
    args = parser.parse_args()
    assert (os.path.isdir(args.WorkingDirectory))
    util.output_path = args.WorkingDirectory
    main(args.PlayerKey)
