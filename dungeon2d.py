"""
2D dungeon with python
by Andreas Schmuck 2015

dungeons must be in folder dungeons
dungeon file must be ".txt" file
file name should start with "dungeon"

"""

import random
import os
import csv


#dungeon = [dungeon1.split(),dungeon2.split(),dungeon3.split(),dungeon4.split()]
dungeon = [] 

legend = ""
commands = ""

for root, dirs, files in os.walk('dungeons'):
    for file in files:
        if file[0:7] == "dungeon" and file[-4:] == ".txt":
            mylevel = open(os.path.join("dungeons",file))
            lines =  mylevel.read().splitlines()
            dungeon.append(lines)
            mylevel.close() 
        elif file  == "legend.txt":
            legendfile = open(os.path.join("dungeons",file))
            legend = legendfile.read()
            legendfile.close()
        elif file == "commands.txt":
            commandsfile = open(os.path.join("dungeons",file))  
            commands = commandsfile.read()
            commandsfile.close()

def cls():
    """clear the screen for windows,mac,linus"""
    os.system('cls' if os.name=='nt' else 'clear')

def remove_tile(x,y,z,new_tile="."):
    """replace tiles / items with new tile"""
    return  dungeon[z][y][:x] + new_tile + dungeon[z][y][x+1:]

def pri_input(txt):
    """print and wait for input"""
    print(txt)
    input("press enter")

def teleport(z):
    """teleport the player to a random floor in lvl z"""
    x = random.randint(1,len(dungeon[z][1])-2)
    y = random.randint(1,len(dungeon[z])-2)
    if dungeon[z][y][x] != "." :
        x,y = teleport(z)
    return x,y,z
    
def fight(o1,o2):
    """fighting between monsters(hero)"""
    print("{} fights {}".format(zoo[o1][0],zoo[o2][0]))
    o1_roll = random.randint(1,zoo[o1][1]) # "[1] würfel"
    o2_roll = random.randint(1,zoo[o2][1])
    pri_input("{} rolls: {}, {} rolls: {} ".format(zoo[o1][0],
              o1_roll,zoo[o2][0],o2_roll))
    if o1_roll == o2_roll:
        return "reroll"
    elif o1_roll > o2_roll:
        return "first win"
    elif o1_roll < o2_roll:
        return "second win"




# hero start posi 1/1

hp=50
hpmax=100
mp=100
hunger=0
food=50
gold=0
key=0
x=1
y=1
dx=0
dy=0
z=0

#name,würfel,damage,attack
#zoo={"L":["lord",10,40,"magic sword"],
#     "S":["statue",6,20,"stone fist"],
#     "O":["ogre",8,30,"crush"],
#     "M":["mage",4,10,"frostbolt"],
#     "@":["hero",6,30,"sword"],
#     }
     
## read zoo from file
zoo = {}
with open(os.path.join("dungeons","zoo.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row["Symbol"], row["Name"], row["Roll"], row["Damage"], row["Attack"])
        zoo[row["Symbol"]] = [row["Name"], int(row["Roll"]), int(row["Damage"]), row["Attack"]]
print(zoo)
input("import of monster zoo successfull. press enter")

#"Symbol","Name","Roll","Damage","Attack"

while hp >0:
    
    cls()
    print("hp: {} mp: {} hunger: {} food: {} gold: {} key: {}".format(int(hp),mp,hunger,food,gold,key))
    line_number = 0
    for line in dungeon[z]:
        if line_number == y:
            print(line[:x]+"@"+line[x+1:])
        else:
            print(line)
        line_number += 1
    c = input("command?")
    dx= 0
    dy= 0
    if c == "quit":
        break
    if c == "help" or c == "?":
        pri_input(legend)
        pri_input(commands)
    if c == "a":
        dx -= 1
        hunger += 1
    if c == "d":
        dx += 1
        hunger += 1
    if c == "w":
        dy -= 1
        hunger += 1
    if c == "s":
        dy += 1
        hunger += 1
    
    tile = dungeon[z][y+dy][x+dx]
    if c == "e" or c == "eat":
        if food <= 0:
            print("you have no food!")
            input("press enter") 
        else: 
            food -= 1
            hunger -= 5
            hunger = max(0,hunger) 
              
    if c == "t" or c == "teleport":
        hunger += 20
        #x,y = teleport(random.randint(0,3))
        x,y,z = teleport(z)
        
    if (c == "esc" or c == "escape") and z >0:  
        hunger += 15
        hp = 1
        x,y,z = teleport(z-1)    
    
    if tile == "<":
        if c == "" or c == "<":
            if z == 0:
                pri_input("you leave the dungeon and return to town")
                break
            z -= 1         
    if tile == ">":
        if c == "" or c == ">":
            if z == len(dungeon)-1:
                pri_input("you already reached the deepest dungeon")
            else:
                z += 1    
    
    
    
    
    #  always
    hp += 0.1
    hp = min(hp,hpmax)
    if hunger > 40:
            hp = 0
            print("you died")
            input("press enter")
    elif hunger > 35:
            hp -= 10
            print("youre starving")
            input("press enter")
    elif hunger > 25:
            hp -= 5
            print("you really need something to eat!")
            input("press enter")
    elif hunger > 20:
        print("youre stomache growls! eat something")
        input("press enter")  
    
    
    
    # check movement
    if tile == "#":
        print("you run into a wall, ouch!")
        input("press enter")
        hp -= 1
        dx=0
        dy=0

    # monsters / traps
    
    if tile in zoo:
        #print("you fight a statue")
        #statue = random.randint(1,6)
        #hero   = random.randint(1,6)
        #pri_input("hero rolls: {} monster rolls: {} ".format(hero,statue))
        result = fight("@",tile)
        if result == "second win":
            pri_input("{} wins".format(zoo[tile][0]))
            hp -= random.randint(1,zoo[tile][2])
            dx=0
            dy=0
        elif result == "reroll":
            pri_input("equal match no damage")
            dx=0
            dy=0
        elif result == "first win":
            pri_input("hero wins")
            # replace statue with "."
            #dungeon[y+dy] = dungeon[y+dy][:x+dx] + "." + dungeon[y+dy][x+dx+1:]
            dungeon[z][y+dy] = remove_tile(x+dx,y+dy,z)

    if tile == "D":
        print("a big door find a way to open it")
        input("press enter")
        dx=0
        dy=0
    
    # movement
    x += dx
    y += dy
    # hero stays on special tile
    tile = dungeon[z][y][x]
    if tile == "$":
        print("you found gold!")
        input("press enter")
        gold += 1
        dungeon[z][y] = remove_tile(x,y,z) # replace gold with .
    if tile == "k":
        print("you found a key!")
        input("press enter")
        key += 1
        dungeon[z][y] = remove_tile(x,y,z)
    if tile == "c":
        print("you found a chest!")
        input("press enter")
        key -= 1
        gold += 10
        dungeon[z][y] = remove_tile(x,y,z)
    if tile == "f":
        print("you found food")
        input("press enter")
        food += 1
        dungeon[z][y] = remove_tile(x,y,z)
    if tile == "1":
        print("you found a lever which opened the big door")
        input("press enter")
        #dungeon[1] = dungeon [1][:4] + "." + dungeon[1][4+1:] #x + y coordinate zum entfernen!!!
        dungeon[z][1] = remove_tile(44,1,z) #entfernt türe bei x(4) y(1) siehe 1 zeile weiter oben
        dungeon[z][y] = remove_tile(x,y,z)
    if tile == "2":
        print("you found a lever which opened the big door in lvl one")
        input("press enter")
        dungeon[0][1] = remove_tile(42,1,0) #fragen wie!
        dungeon[z][y] = remove_tile(x,y,z)

        
        
print("game over")

