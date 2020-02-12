direction = { "0":[-1,0], # North  
               "1":[0,1], #East
               "2":[1,0],  #South
               "3":[0,-1]}  #Weast

 maDirection="0"             
 maDirection=gauche(maDirection)
 maDirection[0]
 direction[maDirection]
 direction[maDirection][0]


 def gauche(x):
    return str((int(x)-1)%4)
    
def droite(x):
    return str((int(x)+1)%4)

position = namedtuple ("position",["i","j"])
p=position(1,2)
p.i
p.j


class Labyrinth:
    def __init__(self,s):
        self._won =False
        self.carry=0
        self.direction="0"
        self.board=load(s)

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
        self._won =False
        self.carry=0
        self.direction="0"
        self.board=load(s)
        self.position=position(0,0)
        
    def size(self):
        return (len(self.board),len(self.board[0]))
    def devant(self):
        po= position(self.position.i+direction[0],self.position.j+direction[1]);
        return po
    def gauche(self):
        self.direction= str((int(self.direction)-1)%4)
    
    def droite(self):
        self.direction= str((int(self.direction)+1)%4)
   