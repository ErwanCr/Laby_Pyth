from enum import Enum
from collections import namedtuple

direction = { "0":[-1,0], # North  
               "1":[0,1], #East
               "2":[1,0],  #South
               "3":[0,-1]}  #Weast

Tile = namedtuple("Tile",["name","char"])

class Tiles:
        Ant_E=Tile(name="ant-e",char="→")
        Ant_N=Tile(name="ant-n",char="↑")
        Ant_S=Tile(name="ant-s",char="↓")
        Ant_W=Tile(name="ant-w",char="←")
        Exit=Tile(name="exit",char="x")
        SmallRock=Tile(name="nrock",char="ŕ")
        SmallWeb=Tile(name="nweb",char="ẃ")
        Rock=Tile(name="rock",char="r")
        Void=Tile(name="void",char=".")
        Wall=Tile(name="wall",char="o")
        Web=Tile(name="web",char="w")
        Outside=Tile(name="void",char=" ")
        RandomRock=Tile(name="void",char="R")
        RandomWeb=Tile(name="void",char="W")


        @staticmethod
        def char2Tile():
            for t in Tiles.__dict__.values():
                if isinstance(t, Tile):
                    print(t.name)
    
def gauche(x):
    return str((int(x)-1)%4)
    
def droite(x):
    return str((int(x)+1)%4)


position = namedtuple ("position",["i","j"])

def load (string):
    tab = []
    f = open(string)
    for line in f:
        if (line[0] == "o"):
            x = line.split()
            tab.append(x)
    return tab
class Labyrinth:
    def __init__(self,s):
        self.tile=Tiles
        self._won =False
        self.carry=self.tile.Void
        self.direction="0"
        self.board=load(s)
        self.position=position(5,5)
        self.message=""
    def size(self):
        return (len(self.board),len(self.board[0]))
    def devant(self):
        po= position(self.position.i+int(direction[self.direction][0]),self.position.j+int(direction[self.direction][1]))
        return po
    def gauche(self):
        self.direction= str((int(self.direction)-1)%4)
        self.message=""
        return True
    def droite(self):
        self.direction= str((int(self.direction)+1)%4)
        self.message=""
        return True
    def win(self):
        self._won=True
        self.message="J'ai gagné !"
    def won(self):
        return self._won


    def pose(self):
        if (self.carry==Tiles.Rock and (regarde()==Tiles.Void or regarde()==Tiles.Web or regarde()==Tiles.SmallWeb or regarde()==Tiles.SmallRock  )):
            self.carry=Tiles.Void
            self.board.set(devant(),Tiles.Rock)
            self.message=""
            return True
        self.message="Je ne peux pas poser."
        return False
    
    
    
    def regarde(self):
        self.message=""
        return self.board.get(devant())
    