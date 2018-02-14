import util
from operator import itemgetter
from random import randint
import json

#Count the number of damaged (enemy) tiles around a certain coordinate
#return the score which is 1000 * N where N = number of damaged tiles
#if score is less than 1000 (no damaged tiles around) count the number of
#free tiles (haven't been damaged/missed)
def examine(x: int, y: int, en_map) -> int:
	i = 1
	score = 0

	while (x+i < util.MAP_SIZE and en_map.cellDmgdStat(x+i, y)\
		and (x+i, y) not in util.SUNK_CELLS):
		score += 1000
		i += 1

	i = 1
	while (x-i >= 0 and en_map.cellDmgdStat(x-i, y)\
		and (x-i, y) not in util.SUNK_CELLS):
		score += 1000
		i += 1

	j = 1

	while (y + j < util.MAP_SIZE and en_map.cellDmgdStat(x, y+j)\
		and (x, y+j) not in util.SUNK_CELLS):
		score += 1000
		j += 1

	j = 1

	while (y-j >= 0 and en_map.cellDmgdStat(x, y-j) \
		and (x, y-j) not in util.SUNK_CELLS):
		score += 1000
		j += 1

	if score == 0:
		return free_space(x, y, en_map)
	
	return score

#Count the number of free tiles around a certain coordinate
def free_space(x: int, y: int, en_map) -> int:
	i = 1
	score = 0

	while (x+i < util.MAP_SIZE and i < 5 and \
		(not en_map.cellDmgdStat(x+i, y) and not (en_map.cellMissStat(x+i, y)))\
		and (x+i, y) not in util.SUNK_CELLS):
		score += 1
		i += 1

	i = 1
	while (x-i >= 0 and i < 5 and \
		(not en_map.cellDmgdStat(x-i, y) and not (en_map.cellMissStat(x-i, y))) \
		and (x-i, y) not in util.SUNK_CELLS):
		score += 1
		i += 1

	j = 1
	while (y+j < util.MAP_SIZE and j < 5 and \
		(not en_map.cellDmgdStat(x, y+j) and not (en_map.cellMissStat(x, y+j)))\
		and (x, y+j) not in util.SUNK_CELLS):
		score += 1
		j += 1

	j = 1

	while (y-j >= 0 and j < 5 and \
		(not en_map.cellDmgdStat(x, y-j) and not (en_map.cellMissStat(x, y-j)))\
		and (x, y-j) not in util.SUNK_CELLS):
		score += 1
		j += 1	

	return score

#Select a weapon from available weapon list
#Choose the biggest weapon available
def pick_special(x : int, y : int, score : int):
	miss_weapon = []
	hit_weapon = []

	for ship in util.state['PlayerMap']['Owner']['Ships']:
		if ship['Destroyed']:
			continue
		for weapon in ship['Weapons']:
			if weapon['EnergyRequired'] <= util.state['PlayerMap']['Owner']['Energy']:
				if weapon['WeaponType'] == 'SingleShot':
					if weapon not in miss_weapon:
						miss_weapon.append(weapon)
						hit_weapon.append(weapon)
				elif weapon['WeaponType'] == 'SeekerMissile':
					miss_weapon.append(weapon)
				else:
					hit_weapon.append(weapon)

	if score < 1000:
		weapon = max(miss_weapon, key=itemgetter('EnergyRequired'))
	else:
		weapon = max(hit_weapon, key=itemgetter('EnergyRequired'))

	return weapon
	
#Examine all the tiles in map which have never been hit
#Pick a tile with maximum score and attack it
def single_attack(en_map):
	max_score = -9999         
	pos = (0,0)
	for x in range(util.MAP_SIZE):
		for y in range(util.MAP_SIZE):
			if en_map.cellDmgdStat(x, y) or en_map.cellMissStat(x, y):
				continue
			score = examine(x, y, en_map)

			if score > max_score:
				max_score = score
				pos = (x, y)

	return pos , pick_special(*pos, max_score)

