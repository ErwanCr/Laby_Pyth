from widget
 import *


##declare ton appli 

app = laby_SVG_view_player_app("share/laby/levels/this-is-crazy.laby") #ici

def debut():
    app.debut()
    
def avance():
    app.avance()
    
def droite():
    app.droite()
    
def gauche():
    app.gauche()
    
def pose():
    app.pose()
    
def prend():
    app.prend()
    
def ouvre():
    app.ouvre()

def regarde():
    app.regarde()
    
def win():
    app.win()
    
def LABY(s): 
    app = laby_level(s)


def LABY_BAR(s) :
    app = laby_bar(s)
