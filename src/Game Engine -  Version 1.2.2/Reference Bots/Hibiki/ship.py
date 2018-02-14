#Greedy Ship Placing
#Stima

from random import choice, randint
import util

#Check if position is available for placing ship
def check_position(x : int, y: int, direction : str, ship : (str, int)) -> bool:
    assert direction in util.DIRECTIONS

    check_x, check_y = x, y

    if direction == 'south':
        check_y -= ship[1]-1
    elif direction == 'east':
        check_x += ship[1]-1

    return check_x >= 0 and \
           check_y >= 0 and \
           check_x < util.MAP_SIZE and \
           check_y < util.MAP_SIZE

#Mark the cells as occupied
def occupy(x: int, y: int, direction: str, ship : (str, int)) -> bool:
    try:
        assert check_position(x, y, direction, ship)
    except:
        return False

    step = 1

    if direction == 'south':
        arg = 1
    elif direction == 'east':
        arg = 0

    to_be = [(x, y)]

    if to_be[0] in util.OCCUPIED:
        return False

    for i in range(ship[1]):
        if arg == 1:
            tup = (x, y-(step*i))
        else:
            tup = (x+(step*i), y)

        if tup in util.OCCUPIED:
            return False

        to_be.append(tup)

    util.OCCUPIED += to_be

    return True

#Place a ship
def place_ship(ship : (str, int),  x: int, y: int, direction : str) -> bool:
    success = occupy(x, y, direction, ship)

    if success:
        util.TO_BE_PLACED.append("%s %d %d %s" % (ship[0], x, y, direction))
    else:
        return False

    return True

#Pick a valid position for a ship at random
def random_initial_ship():
    ship = choice(util.SHIPS)
    direction = choice(util.DIRECTIONS)
    util.SHIPS.pop(util.SHIPS.index(ship))

    placed = False

    while not placed:
        x = randint(0, util.MAP_SIZE - 1)
        y = randint(0, util.MAP_SIZE - 1)

        placed = place_ship(ship, x, y, direction)


#Count the number of free tiles around a ship
#Counting process stop when it found another ship or map out of range
def count_free_nearest_tiles(f_xy : [int, int], t_xy : [int, int]) -> int:
    count = 0
    while (f_xy != t_xy):
        if (f_xy[0], f_xy[1]) in util.OCCUPIED:
            count = 0
        else:
            count += 1

        if f_xy[0] == t_xy[0]:
            if f_xy[1] < t_xy[1]:
                f_xy[1] = f_xy[1] + 1
            else:
                f_xy[1] = f_xy[1] - 1

        else:
            if f_xy[0] < t_xy[0]:
                f_xy[0] = f_xy[0] + 1
            else:
                f_xy[0] = f_xy[0] - 1

    return count


#Count free surrounding tiles of a ship
#Call count_free_nearest_tiles on every cell for 4 directions
def count_free_surrounding_tiles(ship : (str, int), x : int, y : int, direction : str) -> int:
    cur_occupied = util.OCCUPIED[:]

    success = occupy(x, y, direction, ship)

    if not success:
        return -1

    to_be = util.OCCUPIED[len(cur_occupied)-1:]

    count = 0

    for tup in to_be:
        x, y = tup
        count += count_free_nearest_tiles([0, y], [x, y])
        count += count_free_nearest_tiles([util.MAP_SIZE- 1, y], [x, y])
        count += count_free_nearest_tiles([x, 0], [x, y])
        count += count_free_nearest_tiles([x, util.MAP_SIZE - 1], [x, y])


    util.OCCUPIED = cur_occupied[:]

    return count


#Generate a random position
def generate_random_positions() -> list:
    result = []

    for _ in range(70):
        ship = choice(util.SHIPS)
        x = randint(0, util.MAP_SIZE - 1)
        y = randint(0, util.MAP_SIZE - 1)

        direction = choice(util.DIRECTIONS)

        result.append((ship, x, y, direction))

    return result


#Place all 5 different ships with greedy method
#The position with most free surrounding tiles will be chosen at each stage
def place_everything():
    random_initial_ship()

    while util.SHIPS:
        candidates = generate_random_positions()
        fitness = []
        for c in candidates:
            fitness.append(count_free_surrounding_tiles(c[0], c[1], c[2], c[3]))

        best = max(fitness)
        pos = fitness.index(best)
        to_be = candidates[pos]
        #to_be = candidates[0]

        success = place_ship(to_be[0], to_be[1], to_be[2], to_be[3])
        if success:
            util.SHIPS.pop(util.SHIPS.index(to_be[0]))


    return util.TO_BE_PLACED


#Utility function to print the map
def print_map():
    f = open('map.txt', 'w')
    to_be = ''
    for y in range(util.MAP_SIZE):
        for x in range(util.MAP_SIZE):
            if (x, y) in util.OCCUPIED:
                to_be += '|X|'
            else:
                to_be += '|_|'

        to_be += '\n'
    f.write(to_be)
    f.close()
