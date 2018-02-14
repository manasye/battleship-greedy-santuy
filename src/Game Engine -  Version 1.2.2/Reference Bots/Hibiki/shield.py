import util
from operator import itemgetter
from random import randint
import json


#Count the number of hit (player) cells around a certain coordinate
#return the score which is score / (shield size * 4)
def examine(x, y, p_map) :
    score = 0

    '''if (p_map.getSize() == 14):
        shield_size = 3
    elif (p_map.getSize() == 10):
        shield_size = 2
    else:
        shield_size = 1'''

    shield_size = 1

    i = 1

    while (x-i >= 0 and p_map.cellHitStat(x-i, y) and i <= shield_size):
        score += 1
        i += 1

    i = 1

    while (x+i < p_map.getSize() and p_map.cellHitStat(x+i, y) and i <= shield_size):
        score += 1
        i += 1

    j = 1
    while (y-j >= 0 and p_map.cellHitStat(x, y-j) and j <= shield_size):
        score += 1
        j += 1

    j = 1

    while (y+j < p_map.getSize() and p_map.cellHitStat(x, y+j) and j <= shield_size):
        score += 1
        j += 1
    
    
    return score / (shield_size * 4)

#Place shield on a cell with highest score from examine function
def shieldOn(p_map):
    max_score = -9999
    pos = (0,0)
    for x in range(util.MAP_SIZE):
        for y in range(util.MAP_SIZE):
            if (p_map.cellHitStat(x, y) or not p_map.cellOccStat(x,y)):
                continue
            score = examine(x, y, p_map)
            if score > max_score:
                max_score = score
                pos = (x, y)

    return (pos,max_score)

