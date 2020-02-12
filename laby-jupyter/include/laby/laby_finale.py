from collections import namedtuple
from PIL import Image 
import ipywidgets as widgets
import os
from IPython.display import display
from ipywidgets import HBox, VBox
from IPython.display import Image
from IPython.display import display
from enum import Enum
import re
     
entries = os.listdir('tiles_png/')
path = "tiles_png"
path_mur = "tiles\wall.svg"
Tile = namedtuple("Tile",["name","char"])


position = namedtuple ("position",["i","j"])

direction = { "0":[-1,0], # North  
               "1":[0,1], #East
               "2":[1,0],  #South
               "3":[0,-1]}  #Weast



# tuple+enum
#########################################################################################################################
# class tiles avec toutes les tiles et 2 dico pour retrouver  


class Tiles():
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
        
        def __init__(self):
            self.char2N=dict()
            self.char2T=dict()
            self.char2Name()
            self.char2Tile()
        
        #@staticmethod
        def char2Name(self):
            for t in Tiles.__dict__.values():
                if isinstance(t, Tile):
                    self.char2N[t.char]=t.name
        def char2Tile(self):
            p=re.compile('[A-Z]+(\w)*')
            for t in Tiles.__dict__.keys() :
                z=p.match(t)
                if (z!=None):
                    d=z.group()
                    self.char2T[getattr(Tiles,t).char]=d

til = Tiles()
til.char2Tile()
t = til.char2T
til.char2T

path_level = "../../share/laby/levels/"
path_level




#########################################################################################################################


#Load a degager quand board fait 

def load (string):
    tab = []
    f = open(string)
    for line in f:
        if (line[0] == "o"):
            x = line.split()
            tab.append(x)
    return tab




# class Labyrinth qui prend en argument le fichier a ouvrir 

class Labyrinth:
    def __init__(self,s):
        self.tile=Tiles
        self._won =False
        self.carry=self.tile.Void
        self.direction="0"
        self.board=load(s)
        self.position=position(5,5)
        self.message=""
        
       
    def dirToAnt(self):
        if self.direction =="0":
            return Tiles.Ant_N
        elif self.direction =="1":
            return Tiles.Ant_E
        elif self.direction =="2":
            return Tiles.Ant_S
        elif self.direction =="3":
            return Tiles.Ant_W     
        
    def size(self):
        return (len(self.board),len(self.board[0]))
    def devant(self):
        po= position(self.position.i+int(direction[self.direction][0]),self.position.j+int(direction[self.direction][1]));
        return po
    def gauche(self):
        self.direction= str((int(self.direction)-1)%4)
        self.message=""
        return True;
    def droite(self):
        self.direction= str((int(self.direction)+1)%4)
        self.message=""
        return True;
    def win(self):
        self._won=True
        message="J'ai gagné !"
    def won(self):
        return self._won
    def pose(self):
        if (self.carry==t.Rock and (regarde()==t.Void or regarde()==t.Web or regarde()==t.SmallWeb or regarde()==t.SmallRock  )):
            self.carry=t.Void
            board.set(devant(),t.Rock)
            message=""
            return True
        message="Je ne peux pas poser."
        return False
    def regarde(self):
        message=""
        return self.board.get(devant())
    def get(self,pos):
        if (pos.i==self.position.i and pos.j==self.position.j):
            return self.dirToAnt()
        else:
            return self.board.get(pos)
    def ouvre(self):
        if self.regarde()!=tile.Exit :
            message = "Je ne peux pas ouvrir."
            return False
        if carry != tile.Void:
            message = "Je ne peux pas ouvrir en portant un objet."
            return False
        self.position=self.devant()
        self.win()
        return True
    def prend(self):
        if self.carry==self.tile.Void and self.regarde()==self.tile.Rock:
            self.carry=self.tile.Rock
            self.board.set(self.devant(),self.tile.Void)
            message=""
            return True
        message = "Je ne peux pas prendre."
        return False
    
            



#########################################################################################################################


#fct charger prend le niveau et creer un tableau 2D avec les char des tiles
def charger(nom_niveau):
    fichier = open(nom_niveau, 'r+')
    tab = []
    for line in fichier:
        if (len(line)>0 and (line[0] == "o" or line[0] =="." or line[0] =="x")):
            x = line.split()
            tab.append(x)
    return tab

#charger(path_level + "0.laby")


#affiche le niveau prend le nom du fichier a ouvrir 

def affichage_niveau(nom_niveau):
    charger_niveau = remplir_plateau(nom_niveau)
    items=[]
    taille_ligne =0
    for line in charger_niveau:
        taille_ligne = len(line)
        for caractere in line:
           # print(til.char2T[caractere])
            pof=getattr(Tiles,caractere).name
            image = ""
            image = "tiles_png/" + pof + ".png"
#             print(image)
            file = open (image,'rb')
            image_lu = file.read()
            items.append(widgets.Image(value = image_lu, format='png', layout=widgets.Layout(display="flex",
            margin="1px", width="100%"
            )))
    display(widgets.GridBox(items,layout=widgets.Layout(grid_template_columns="repeat("+str(taille_ligne)+", 50px)")))

# affichage_niveau(path_level + "0.laby")



# prend le nom du fichier et remplit un tableau 2D de tiles 
def remplir_plateau(nom_niveau):
    fichier = open(nom_niveau, 'r+')
    tab = []
    for line in fichier:
        if (len(line)>0 and (line[0] == "o" or line[0] =="." or line[0] =="x")):
            x = line.split()
            tab_line = []
            for i in x:
                bloc = til.char2T[i]
                tab_line.append(bloc)
            tab.append(tab_line)
    return tab

#remplir_plateau(path_level + "0.laby")
        
