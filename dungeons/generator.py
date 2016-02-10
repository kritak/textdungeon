"""tool to generate random levels"""


import random
import os


LOOTCHANCE = 0.05
MONSTERCHANCE = 0.05

def cls():
    """clear the screen for windows,mac,linus"""
    os.system('cls' if os.name=='nt' else 'clear')

class Game():
    prefix = "gen"
    number = 0
    suffix = ".txt"
    maxwidth = 50
    minwidth = 50
    maxheight = 18
    minheight = 18
    stairs = 3
    rooms_per_level = 10
    #             "c": "chest",
    #             "+" : "shop",
    #             "s" : "scroll",
    chars = {"#": "wall", 
             "." : "floor",
             "$" : "gold",
             "d" : "door",
             "k" : "key",
             "f" : "food",
             "D" : "big door",
             "1" : "lever",
             "<" : "stair up", 
             ">" : "stair down",
             "r" : "random loot",
             "R" : "random enemy"}
             
             



class Rect():
    """dungeon creator// a rectangle on the map used to charecterize a room"""
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.x2 = x + w
        self.y2 = y + h
        self.mx = random.randint(self.x, self.x2)
        self.my = random.randint(self.y, self.y2)
        
        







def main():
    #level name / linien generierung
    level = []
    rooms = []
    corridors = []
    mittelpunkte = []
    width = random.randint(Game.minwidth,Game.maxwidth)
    height = random.randint(Game.minheight,Game.maxheight)
    
    # full of stone walls
    for y in range(height):
        line = "#"*width
        level.append(line)
    
    
    for roomnumber in range(Game.rooms_per_level):
        
        # make room ------------------
        x= random.randint(1,width-2)
        y= random.randint(1,height-2)
        
        w = random.randint(0,min(width//2, width-2-x))
        h = random.randint(0,min(height//2, height-2-y))
        myroom = Rect(x,y,w, h)
        
        
        
        # ----------room made -----------------       
        rooms.append(myroom)
        
        
    # grabe verbindungsgang
    
    for r in rooms:
        mittelpunkte.append([r.mx, r.my])
    for roomnr in range(Game.rooms_per_level):
        start = mittelpunkte[roomnr]
        ziele = list(range(Game.rooms_per_level))
        ziele.remove(roomnr)
        zielnr = random.choice(ziele)
        ziel = mittelpunkte[zielnr]
        
        # gang graben zwischen start und ziel 
        
        # wer ist höher ? (niedrigeres y )
        if start[1] <= ziel[1]:
            # runtergraben von start nach ziel
            # wer ist links (niedrigeres x)
            if start[0] <= ziel[0]:
                # start nach ziel
                # nach rechts graben
                c1 = Rect(start[0], start[1], ziel[0]-start[0],0)
                corridors.append(c1)
                # nach unten graben
                c2 = Rect(c1.x2, c1.y2, 0, ziel[1]-start[1])
                corridors.append(c2)  
            else:
                # nach links graben
                c1 = Rect(ziel[0], start[1],start[0]-ziel[0],0)
                corridors.append(c1)
                #nach unten graben
                c2 = Rect(ziel[0], start[1], 0, ziel[1]-start[1])
                corridors.append(c2)

        else:
            # runtergraben von ziel nach start
            # wer ist links (niedrigeres x)
            if start[0] <= ziel[0]:
                #nach links graben
                c1 = Rect(start[0], ziel[1], ziel[0]-start[0],0)
                corridors.append(c1)
                #nach unten graben
                c2 = Rect(start[0],ziel[1], 0, start[1]-ziel[1])
                corridors.append(c2)
                #print("now")
                
            else:  
                # nach rechts graben
                c1 = Rect(ziel[0], ziel[1], start[0]-ziel[0],0)
                corridors.append(c1)
                # nach unten graben
                c2 = Rect(c1.x2, c1.y2, 0, start[1]-ziel[1])
                corridors.append(c2)
        
        
    
    # paint level
    for myroom in rooms:
        for y in range(height):
            for x in range(width):
                if y >= myroom.y and y <= myroom.y2:
                    if x >= myroom.x and x <= myroom.x2:
                        tile = "."
                        # ---------- fill room with loot ----------
                        if random.random() < LOOTCHANCE:
                            tile = "r"
                        # -------- fill room with monsters ---------
                        if random.random() < MONSTERCHANCE:
                            tile = "R"
                        level[y] = level[y][:x] + tile + level[y][x+1:]
    
    for myroom in corridors:
        for y in range(height):
            for x in range(width):
                if y >= myroom.y and y <= myroom.y2:
                    if x >= myroom.x and x <= myroom.x2:
                        level[y] = level[y][:x] + "." + level[y][x+1:]
    
    
    
    
    
    ## write to file
    Game.number += 1
    numstr = str(Game.number)
    if Game.number < 10:
        numstr = "00"+numstr
    elif Game.number < 100:
        numstr = "0" + numstr
        
    
    filename = Game.prefix + numstr + Game.suffix
    myfile = open(filename,"w")
    for line in level:
        myfile.write(line+"\n")
    myfile.close()
    
    # show
    cls()
    for line in level:
        print(line)
    print(Game.number)
    input()
    






if __name__=="__main__":
    for a in range(40):
        main()
