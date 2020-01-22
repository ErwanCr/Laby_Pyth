from enum import Enum
from collections import namedtuple

direction = { "0":[-1,0], # North  
               "1":[0,1], #East
               "2":[1,0],  #South
               "3":[0,-1]}  #Weast

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
