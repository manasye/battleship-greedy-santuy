import argparse
import json
import os
from random import choice
from pathlib import Path

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
        if os.path.isfile('test.txt'):
            os.remove('test.txt')
        place_ships()
    else:
        fire_shot(state['OpponentMap']['Cells'])


def output_shot(move, x, y):
    with open(os.path.join(output_path, command_file), 'w') as f_out:
        f_out.write('{},{},{}'.format(move, x, y))
        f_out.write('\n')
    pass


def fire_shot(opponent_map):
    # To send through a command please pass through the following <code>,<x>,<y>
    # Possible codes: 1 - Fireshot, 0 - Do Nothing (please pass through coordinates if
    #  code 1 is your choice)
    if not os.path.exists("test.txt"):
        # File not found
        targets = []
        for cell in opponent_map:
            if not cell['Damaged'] and not cell['Missed']:
                valid_cell = cell['X'], cell['Y']
                targets.append(valid_cell)
        # randomize target from targets
        move = 1
        target = choice(targets)
        to_file = [target]
        with open('test.txt', 'w') as fp:
            fp.write('\n'.join('%d %d' % x for x in to_file))
        fp.close()
        output_shot(move, *target)
        return
    else:
        # File found
        res = []
        with open('test.txt', 'r') as fo:
            for i in fo.readlines():
                tmp = i.split(" ")
                try:
                    res.append((int(tmp[0]), int(tmp[1])))
                except:
                    pass
        last_shot = res.pop()
<<<<<<< HEAD
        # access map: last_shot[1]+last_shot[0]*map_size]
        if opponent_map[last_shot[1] + (last_shot[0] * map_size)]['Damaged']:
            # append 4 more targets
            # x+1 , y
            if last_shot[0]+1 < map_size and not (opponent_map[last_shot[1] + (last_shot[0]+1)*map_size]['Damaged']) and not (opponent_map[last_shot[1] + (last_shot[0]+1)*map_size]['Missed']):
                res.append((last_shot[0] + 1, last_shot[1]))
            # x-1, y
            if last_shot[0]-1 >= 0 and not (opponent_map[last_shot[1] + (last_shot[0]-1)*map_size]['Damaged']) and not (opponent_map[last_shot[1] + (last_shot[0]-1)*map_size]['Missed']):
                res.append((last_shot[0] - 1, last_shot[1]))
            # x, y+1
            if last_shot[1]+1 < map_size and not (opponent_map[last_shot[1]+1 + (last_shot[0])*map_size]['Damaged']) and not (opponent_map[last_shot[1]+1 + (last_shot[0])*map_size]['Missed']):
                res.append((last_shot[0], last_shot[1] + 1))
            # x, y-1
            if last_shot[1]-1 >= 0 and not (opponent_map[last_shot[1]-1 + (last_shot[0])*map_size]['Damaged']) and not (opponent_map[last_shot[1]-1 + (last_shot[0])*map_size]['Missed']):
=======
        # access map: last_shot[1]+last_shot[0]*10]
        if opponent_map[last_shot[1] + (last_shot[0] * 10)]['Damaged']:
            # append 4 more targets
            # x+1 , y
            if last_shot[0]+1 < map_size and not (opponent_map[last_shot[1] + (last_shot[0]+1)*10]['Damaged']) and not (opponent_map[last_shot[1] + (last_shot[0]+1)*10]['Missed']):
                res.append((last_shot[0] + 1, last_shot[1]))
            # x-1, y
            if last_shot[0]-1 > 0 and not (opponent_map[last_shot[1] + (last_shot[0]-1)*10]['Damaged']) and not (opponent_map[last_shot[1] + (last_shot[0]-1)*10]['Missed']):
                res.append((last_shot[0] - 1, last_shot[1]))
            # x, y+1
            if last_shot[1]+1 < map_size and not (opponent_map[last_shot[1]+1 + (last_shot[0])*10]['Damaged']) and not (opponent_map[last_shot[1]+1 + (last_shot[0])*10]['Missed']):
                res.append((last_shot[0], last_shot[1] + 1))
            # x, y-1
            if last_shot[1]-1 > 0 and not (opponent_map[last_shot[1]-1 + (last_shot[0])*10]['Damaged']) and not (opponent_map[last_shot[1]-1 + (last_shot[0])*10]['Missed']):
>>>>>>> 51b029e902633992f98aede3ada23a42bf613069
                res.append((last_shot[0], last_shot[1] - 1))
            move = 1
            if len(res) == 0:
                targets = []
                for cell in opponent_map:
                    if not cell['Damaged'] and not cell['Missed']:
                        valid_cell = cell['X'], cell['Y']
                        targets.append(valid_cell)
                # randomize target from targets
                move = 1
                target = choice(targets)
                res.append(target)
                with open('test.txt', 'w') as fp:
                    fp.write('\n'.join('%d %d' % x for x in res))
                fp.close()
                output_shot(move, *target)
                return
            else:
                target = res[len(res) - 1]
                with open('test.txt', 'w') as fp:
                    fp.write('\n'.join('%d %d' % x for x in res))
                fp.close()
                output_shot(move, *target)
                return
        else:
            if len(res) == 0:
                targets = []
                for cell in opponent_map:
                    if not cell['Damaged'] and not cell['Missed']:
                        valid_cell = cell['X'], cell['Y']
                        targets.append(valid_cell)
                # randomize target from targets
                move = 1
                target = choice(targets)
                res.append(target)
                with open('test.txt', 'w') as fp:
                    fp.write('\n'.join('%d %d' % x for x in res))
                fp.close()
                output_shot(move, *target)
                return
            else:
                # use top as new target
                move = 1
                target = res[len(res)-1]
                with open('test.txt', 'w') as fp:
                    fp.write('\n'.join('%d %d' % x for x in res))
                fp.close()
                output_shot(move, *target)
                return


def place_ships():
    # Please place your ships in the following format <Shipname> <x> <y> <direction>
    # Ship names: Battleship, Cruiser, Carrier, Destroyer, Submarine
    # Directions: north east south west
    # x = 0 di kiri
    # y = 0 di bawah
    # north ke atas, south ke bawah
    # west ke kiri, east ke kanan
<<<<<<< HEAD
    if map_size == 10:
        ships = ['Battleship 1 0 north',
                 'Carrier 3 1 East',
                 'Cruiser 4 2 north',
                 'Destroyer 7 3 north',
                 'Submarine 1 8 East'
                 ]
    elif map_size == 7:
        ships = ['Battleship 1 2 north',
                 'Carrier 0 0 East',
                 'Cruiser 6 2 north',
                 'Destroyer 4 5 north',
                 'Submarine 3 3 East'
                 ]
=======
    ships = ['Battleship 1 0 north',
             'Carrier 3 1 East',
             'Cruiser 4 2 north',
             'Destroyer 7 3 north',
             'Submarine 1 8 East'
             ]
>>>>>>> 51b029e902633992f98aede3ada23a42bf613069

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
