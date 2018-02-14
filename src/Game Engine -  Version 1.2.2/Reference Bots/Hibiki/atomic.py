import argparse
import json
import os
from random import choice

command_file = "command.txt"
place_file = "place.txt"
game_state_file = "state.json"
output_path = '.'
map_size = 0

class en_Matrix :
    #Class untuk Matriks Musuh
    M = [[]]
    def __init__(self,en_cells,size) :
        #inisialisasi Matriks Musuh dengan parameter OpponentCell dan MapDimension
        i = 0
        j = 0
        self.size = size
        for cell in en_cells :
            NewCell = en_Matrix.CellElmt(cell)
            if (j <  size):
                self.M[i].append(NewCell)
                j+=1
            else :
                self.M.append([NewCell])
                i+= 1
                j = 1
    def getSize(self) :
        #Mengembalikan Map Dimension
        return(self.size)
    def getCell(self,x,y) :
        #Mengembalikan Cell pada Baris X dan Kolom Y
        return(self.M[x][y])
    def getMap(self) :
        #Mengembalikan Matriks Cell
        return(self.M)
    def cellDmgdStat(self,x,y) :
        #Mengembalikan Status Damaged Cell di Koordinat x,y
        return(self.M[x][y].damaged)
    def cellMissStat(self,x,y) :
        #Mengembalikan Status Missed Cell di Koordinat x,y
        return(self.M[x][y].missed)
    def cellShieldHStat(self,x,y) :
        #Mengembalikan Status ShieldHit Cell di Koordinat x,y
        return(self.M[x][y].shieldHit)

    class CellElmt :
        def __init__(self, Cell) :
            self.damaged = Cell['Damaged']
            self.missed = Cell['Missed']
            self.shieldHit = Cell['ShieldHit']
        def damagedStat(self) :
            #Mengembalikan Status Damaged Cell
            return(self.damaged)
        def missedStat(self) :
            #Mengembalikan Status Missed Cell
            return(self.missed)
        def shieldHStat(self) :
            #Mengembalikan Status ShieldHit Cell
            return(self.shieldHit)

        def __repr__(self) :
            #Mengembalikan Status 1 0 dari Damaged, missed dan ShieldHit Cell
            if (self.damaged) :
                dmgd = 1
            else :
                dmgd = 0
            if (self.missed) :
                mss = 1
            else:
                mss = 0
            if (self.shieldHit):
                sh = 1
            else:
                sh = 0
            return('[{},{},{}]'.format(dmgd, mss, sh)) 
        
class p_Matrix :
    #Class Untuk Matriks Sendiri
    M = [[]]
    def __init__(self,player_cells,size) :
        #inisialisasi Matriks Sendiri dengan parameter PlayerCell dan MapDimension
        i = 0
        j = 0
        self.size = size
        for cell in player_cells :
            NewCell = p_Matrix.CellElmt(cell)
            if (j <  size):
                self.M[i].append(NewCell)
                j+=1
            else :
                self.M.append([NewCell])
                i+= 1
                j = 1
    def getSize(self) :
        #Mengembalikan MapDimension
        return(self.size)
    def getCell(self,x,y) :
        #Mengembalikan Cell di Baris x dan Kolom y
        return(self.M[x][y])
    def getMap(self) :
        #Mengembalikan Map Player
        return(self.M)
    def cellOccStat(self,x,y) :
        #Mengembalikan status Occupied Cell di baris x dan kolom y
        return(self.M[x][y].occupied)
    def cellHitStat(self,x,y) :
        #Mengembalikan status Hit Cell di baris x dan kolom y
        return(self.M[x][y].hit)
    def cellShieldHStat(self,x,y) :
        #Mengembalikan status ShieldHit Cell di baris x dan kolom y
        return(self.M[x][y].shieldHit)
    def cellShieldStat(self,x,y) :
        #Mengembalikan status Shield Cell di baris x dan kolom y
        return(self.M[x][y].shieldOn)

    class CellElmt :
        def __init__(self, Cell) :
            self.occupied = Cell['Occupied']
            self.hit = Cell['Hit']
            self.shieldHit = Cell['ShieldHit']
            self.shieldOn = Cell['Shielded']
        def occupiedStat(self) :
            #Mengembalikan status Occupied Cell
            return(self.occupied)
        def hitStat(self) :
            #Mengembalikan status Hit Cell
            return(self.hit)
        def shieldHStat(self) :
            #Mengembalikan status ShieldHit Cell
            return(self.shieldHit)
        def shieldStat(self) :
            #Mengembalikan status Shield Cell
            return(self.shieldOn)

        def __repr__(self) :
            if (self.occupied) :
                occ = 1
            else :
                occ = 0
            if (self.hit) :
                ht = 1
            else:
                ht = 0
            if (self.shieldHit):
                sh = 1
            else:
                sh = 0
            if (self.shieldOn):
                s = 1
            else :
                s = 0
            return('[{},{},{},{}]'.format(occ, ht, s,sh)) 


def StrPlace(Ship, x,y, direction) :
    #Mengembalikan String penempatan Ship di baris x dan kolom y dengan menghadap ke direction
    return('{} {} {} {}'.format(Ship,x,y,direction))


def PlaceShip(ShipList):
    #Menempatkan semua Ship yang berada pada ShipList
    with open(os.path.join(output_path, place_file), 'w') as fout:
        for ship in ShipList:
            fout.write(ship)
            fout.write('\n')
    return

def take_act(x, y, action):
    #Menuliskan Command yang akan dijalankan dengan action di cell x,y
    with open(os.path.join(output_path, command_file), 'w') as fout:
        fout.write('{},{},{}'.format(action, x, y))
        fout.write('\n')
    pass



#with open(os.path.join(output_path, game_state_file), 'r') as fin:
#    state = json.load(fin)
#EnState = en_Matrix(state['OpponentMap']['Cells'],state['MapDimension'])
#print(EnState.size)
#for i in range(0,EnState.size) :
#    print(i)
#    print(EnState.M[i])
#print()
#PState = p_Matrix(state['PlayerMap']['Cells'],state['MapDimension'])
#print(PState.size)
#for i in range(0,PState.size) :
#    print(i)
#    print(PState.M[i])
