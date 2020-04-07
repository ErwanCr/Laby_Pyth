from enum import Enum
from collections import namedtuple
import re
from collections import namedtuple
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
# from PIL import Image 
import ipywidgets as widgets
import os
import math
from IPython.display import display
from ipywidgets import HBox, VBox
# import PIL
# import numpy as np
# import re
from IPython.display import Image
# from IPython.display import display
import random

position = namedtuple ("position",["i","j"])
PlayDirection = Enum('PlayDirection','Forward Backward None')
direction = { "0":[-1,0], # North  
               "1":[0,1], #East
               "2":[1,0],  #South
               "3":[0,-1]}  #Weast

class  Board: 
    def __init__(self,niveau):
        self.plateau=niveau
    
    def get(self,position):
        if (position.i<0 or position.j<0 or position.i >= len(self.plateau)or position.j>=len(self.plateau[0])):
            return Tiles.Outside
        else:
            return self.plateau[position.i][position.j] 
    
    def set(self,position,tuile):
        if (position.i<0 or position.j<0 or position.i >= len(self.plateau)or position.j>=len(self.plateau[0])):
             print('erreur !!')   
        self.plateau[position.i][position.j]=tuile       

def charger(nom_niveau):
    fichier = open(nom_niveau, 'r+')
    tab = []
    i=0
    j=0
    stockI=-1


    stockJ=-1
    dire=0
    for line in fichier:
        
        j=0
        bleau=[]
        if (len(line)>0 and (line[0] == "o" or line[0] =="." or line[0] =="x")):
            x = line.split()
            for nimportequoi in x: 
                if (nimportequoi=="←"):
                    stockI=i
                    stockJ=j
                    dire="3"
                    nimportequoi="."
                if (nimportequoi=="↓"):
                    stockI=i
                    stockJ=j
                    dire="2"
                    nimportequoi="."
                if (nimportequoi=="↑"): 
                    stockI=i
                    stockJ=j
                    dire="0"
                    nimportequoi="."
                if (nimportequoi =="→"):
                    stockI=i
                    stockJ=j
                    dire="1"
                    nimportequoi="."
                bleau.append(Tiles.char2Tile[nimportequoi])
                j+=1
            tab.append(bleau)
            i+=1
    return [tab,stockI,stockJ,dire]

class labyrinth:
    ## a rajouter from string // to string // html 
    
    def __init__(self,s):
        
        self._won = False
        self.carry = Tiles.Void
        self.temp = charger(s)
        self.direction = self.temp[3]
        self.board = Board(self.temp[0])
        self.randomize()
        self.position = position(self.temp[1],self.temp[2])
        self.message = ""
        
    def reset(self): 
        self._won = False
        self.carry = Tiles.Void
        self.direction = self.temp[3]
        self.board = Board(self.temp[0])
        self.randomize()
        self.position = position(self.temp[1],self.temp[2])
        self.message = ""

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
        return (len(self.board.plateau),len(self.board.plateau[0]))
    
    def devant(self):
        po = position(self.position.i+int(direction[self.direction][0]),self.position.j+int(direction[self.direction][1]));
        return po
    
    def gauche(self):
        self.direction = str((int(self.direction)-1)%4)
        self.message = ""
        return True
    
    def droite(self):
        self.direction = str((int(self.direction)+1)%4)
        self.message = ""
        return True
    
    def avance(self):
        tile=self.board.get(self.position)
        tile_devant=self.board.get(self.devant())
        if(tile==Tiles.Web or tile==Tiles.Exit or tile_devant==Tiles.Outside or tile_devant==Tiles.Exit
           or tile_devant==Tiles.Rock or tile_devant==Tiles.Wall):
            self.message = "je ne peux pas avancer."
            return False
        self.message = ""
        self.position = self.devant()
        return True
    
    def win(self):
        self._won=True
        message="J'ai gagné !"
    
    def won(self):
        return self._won
    
    def pose(self):
        if (self.carry==self.tile.Rock and (self.regarde()==self.tile.Void or self.regarde()==self.tile.Web 
                or self.regarde()==self.tile.SmallWeb or self.regarde()==self.tile.SmallRock  )):
            self.carry=self.tile.Void
            self.board.set(self.devant(),self.tile.Rock)
            message=""
            return True
        message="Je ne peux pas poser."
        return False
    
    def regarde(self):
        message=""
        return self.board.get(self.devant())
    
    def get(self,pos):
        if (pos[0] == self.position[0] and pos[1] ==self.position[1]):
            return self.dirToAnt()
        else:
            return self.board.get(pos)
    
    def ouvre(self):
        if self.regarde()!= Tiles.Exit :
            message = "Je ne peux pas ouvrir."
            return False
        if self.carry != Tiles.Void:
            message = "Je ne peux pas ouvrir en portant un objet."
            return False
        self.position = self.devant()
        self.win()
        return True
    
    def prend(self):
        if (self.carry==self.tile.Void and self.regarde()==self.tile.Rock):
            self.carry=self.tile.Rock
            self.board.set(self.devant(),self.tile.Void)
            message=""
            return True
        message = "Je ne peux pas prendre."
        return False
     
    def randomize(self):
        n_random_rocks=0
        n_random_webs=0
        for row in self.board.plateau:
            for c in row:
                if(c==Tiles.RandomRock):
                    n_random_rocks =n_random_rocks +1
                if(c==Tiles.RandomWeb):
                    n_random_webs =n_random_webs +1
        r_rock =math.floor( random.random()*25 % n_random_rocks) if n_random_rocks else 0
        r_web = math.floor( random.random()*25 % n_random_webs) if n_random_webs else 0
        n_random_rocks=0
        n_random_webs=0
        nRow=0
        
        for row in self.board.plateau:
            nC=0 
            for c in row:
                if (c == Tiles.RandomRock):
                    if (n_random_rocks == r_rock):
                         self.board.plateau[nRow][nC] = Tiles.SmallRock
                    else:
                        self.board.plateau[nRow][nC] = Tiles.Rock
                    n_random_rocks =n_random_rocks +1
                
                if (c == Tiles.RandomWeb):
                    if (n_random_webs == r_web):
                        self.board.plateau[nRow][nC] = Tiles.SmallWeb
                    else:
                        self.board.plateau[nRow][nC] = Tiles.Web
                    n_random_webs =n_random_webs +1
                nC=nC+1
               
            nRow=nRow+1  

Tile= namedtuple("Tile",["name","char"])

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
        
       
        
        
Tiles.char2N=dict()
Tiles.char2Tile=dict()
for t in Tiles.__dict__.values():
    if isinstance(t, Tile):
        Tiles.char2N[t.char]=t.name
        Tiles.char2Tile[t.char]=t
                    

Tiles.char2T=dict()
p=re.compile('[A-Z]+(\w)*')
for t in Tiles.__dict__.keys() :
    z=p.match(t)
    if (z!=None):
        d=z.group()
        Tiles.char2T[getattr(Tiles,t).char]=d

class labyrinth_view:
    
    def __init__(self,labyrinth ):
        self.value=labyrinth
    def to_string(self):
        return value.to_string()
    def update(self):
        pass


class Player :
    def __init__(self, _view):
        self.view = _view
        self.original_value=view.value
        self.play_direction=forward
        self.play_fps=1
        self.timer =Timer ( partial(self.tick),self.play_fps)
        self.reset()
       
        def run(self):
            self.timer.run()
        
        def update(self):
            self.value = history[time]
            self.view.update()
        def get_value(self):
            
            return self.history[len(self.history)-1]
        
        def set_value(self,value):
            if (len(self.history) > 10000):
                raise RunTimeError("Votre programme a pris plus de 1000 étapes")
                #throw std::runtime_error("Votre programme a pris plus de 1000 étapes");#throw
            self.history.append(value);
            if ( not self.timer.running() and self.time == len(self.history) -2):
                self.time=self.tim+1
                self.update()
        def tick(self):
            if(self.play_direction == Forward ): # a check toute la fonction 
                self.step_forward()
            else:
                self.step_backward()
        
        def reset(self,value):      #verifier tous els attributs
                self.time=0
                self.history=[value]
                self.update()
        
        def begin(self):
            self.time=0
            self.update()
        
        def end(self):
            self.time= len(self.history)-1  
            self.update()
        def step_backward(self):
            if( self.time >0):
                self.time=self.time-1
                self.update()
        def step_forward(self):
            if( self.time <len(self.history)-1):  
                self.time=self.time+1
                self.update()        
        def backward (self):
            self.play_direction = Backward # a check
            self.timer.set_fps(self.play_fps)
        
        def play(self):
            self. play_direction = Forward # a check
            self.timer.set_fps(self.play_fps)
        
        def pause(self):
            self.play_direction=None
            self.timer.set_fps(0)
        
        def set_fps(self,fps):
            self.play_fps=fps
            if(self.play_direction != None):
                self.timer.set_fps(fps)
        
        def won(self):
            return self.history[len(self.history)-1].won()



class LabyBaseApp:
  
    def __init__(self,labyrinth):
        self.view=labyrinth
        self.player=Player(self.view)       
    
    def debut(self) :
        value = self.player.history[0]
        value.randomize()
        self.player.reset(value)
        return res

    def avance(self) :
        value = self.player.get_value()
        res = value.avance()
        self.player.set_value(value)
        return res
    
    def droite(self) :
        value = self.player.get_value()
        res = value.droite()
        self.player.set_value(value)
        return res
    
    def gauche(self) :
        value = self.player.get_value()
        res = value.gauche()
        self.player.set_value(value)
        return res
        
    def prend(self):
        value = self.player.get_value()
        res = value.prend()
        self.player.set_value(value)
        return res
    
    def pose(self) :
        value = self.player.get_value()
        res = value.pose()
        self.player.set_value(value)
        return res
    
    def sow(self) :
        value = self.player.get_value()
        res = value.sow()
        self.player.set_value(value)
        return res
    
    def regarde(self) :
        return self.player.get_value().regarde()
    
    def ouvre(self):
        value = self.player.get_value()
        res = value.ouvre()
        self.player.set_value(value)
        return res
    
    def won(self): 
        return self.player.won()
            
            
            
 ##########################################################""           

l = labyrinth("share/laby/levels/this-is-crazy.laby" )

def affichage_niveau_recursif(laby):
    carte = laby.board.plateau
    items=[]
    taille_ligne =0
    
    for j in range (0,len(carte)):
        taille_ligne = len(carte[0])
        for i in range (0,len(carte[0])):
            if(j==laby.position[0] and i==laby.position[1]):
                tuile= laby.dirToAnt()
            else:
                tuile = l.board.get(position(j,i))
            
            pof = tuile.name
            image = "include/laby/tiles_png/" + pof + ".png"
            file = open (image,'rb')
            image_lu = file.read()
            items.append(widgets.Image(value = image_lu, format='png', layout=widgets.Layout(display="flex",
            margin="1px", width="100%"
            )))
    display(widgets.GridBox(items,layout=widgets.Layout(grid_template_columns="repeat("+str(taille_ligne)+", 50px)")))

affichage_niveau_recursif(l)