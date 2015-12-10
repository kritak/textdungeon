"""
2D dungeon with python
by Andreas Schmuck 2015"""

import random
import os


def cls():
    """clear the screen for windows,mac,linus"""
    os.system('cls' if os.name=='nt' else 'clear')

def remove_tile(x,y,z,new_tile="."):
    """replace tiles / items with new tile"""
    return  dungeon[z][y][:x] + new_tile + dungeon[z][y][x+1:]




legend="""
.    floor
#    wall
@    hero
f    food
$    coins
t    trap
d    door
k    key
B    boss
M    mage
S    statue
<    stair-up
>    stair-down"""

dungeon1="""
###################################################
#..<........................................D.....#
#......#.....................#..............#.....#
#......#.....................#..............#.....#
#.1....#.....................#..............#<....#
####d###.....................#..............#######
#....#..........##############....................#
#....#..........#.................................#
#....#..........#.................................#
#####################.....................#########
#...................#.....................#.......#
#...................#.....................#...#...#
#...................#.....................#..##...#
#...................#.....................#.#.#...#
#...................#.....................#...#...#
#...................#.....................#...#...#
#...................#.....................#.......#
###################################################"""

dungeon2="""
###################################################
#......#............................#.O.#######...#
#......#............................#.#<##..M...#.#
#......#............................#.####.######.#
#......#............................#......##>....#
####d###............................###############
#....#..............................#>.....L#######
#....#..............................###############
#....d............................................#
######..................................###########
#.......................................#.........#
#.......................................#.#####...#
#.......................................#.#...#...#
#.......................................#....#....#
#.......................................#...#.....#
#.......................................#.#####...#
#.......................................#.........#
###################################################"""

dungeon3="""
###################################################
#......#.................................##########
#......#..............................#>.##########
#......#..............................#############
#......#............................###############
####d###............................#<SSS........>#
#....#..............................###############
#....#............................................#
#....d............................................#
######..................................###########
#.......................................#.........#
#.......................................#.#####...#
#.......................................#.....#...#
#.......................................#.#####...#
#.......................................#.....#...#
#.......................................#.#####...#
#.......................................#.........#
###################################################"""

dungeon4="""
###################################################
#......#..........................................#
#......#..........................................#
#......#..........................................#
#......#..........................................#
####d###.........................................<#
#....#............................................#
#....#............................................#
#....d............................................#
######............................................#
#.......................................###########
#.......................................#.........#
#.......................................#.#..#....#
#.......................................#.#####...#
#.......................................#....#....#
#.......................................#....#....#
#.......................................#.........#
###################################################"""



dungeon = [dungeon1.split(),dungeon2.split(),dungeon3.split(),dungeon4.split()]


# hero start posi 1/1

hp=100
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


while hp >0:
    
    cls()
    print("hp: {} mp: {} hunger: {} food: {} gold: {} key: {}".format(hp,mp,hunger,food,gold,key))
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
    if tile == "S":
        print("you fight a statue")
        statue = random.randint(1,6)
        hero   = random.randint(1,6)
        if statue > hero:
            print("statue wins")
            input("press enter")
            hp -= 20
            dx=0
            dy=0
        elif statue == hero:
            print("reroll")
            input("press enter")
            dx=0
            dy=0
        else:
            print("hero wins")
            input("press enter")
            # replace statue with "."
            #dungeon[y+dy] = dungeon[y+dy][:x+dx] + "." + dungeon[y+dy][x+dx+1:]
            dungeon[z][y+dy] = remove_tile(x+dx,y+dy,z)
    if tile == "M":
        print("you fight a mage")
        mage = random.randint(1,6)
        hero   = random.randint(1,6)
        if mage > hero:
            print("mage wins")
            input("press enter")
            hp -= 20
            dx=0
            dy=0
        elif mage == hero:
            print("reroll")
            input("press enter")
            dx=0
            dy=0
        else:
            print("hero wins")
            input("press enter")
            dungeon[z][y+dy] = remove_tile(x+dx,y+dy,z)           
    if tile == "L":
        print("you fight a lord")
        lord = random.randint(1,6)
        hero   = random.randint(1,6)
        if lord > hero:
            print("lord wins")
            input("press enter")
            hp -= 40
            dx=0
            dy=0
        elif lord == hero:
            print("reroll")
            input("press enter")
            dx=0
            dy=0
        else:
            print("hero wins")
            input("press enter")
            dungeon[z][y+dy] = remove_tile(x+dx,y+dy,z)          
    if tile == "O":
        print("you fight an ogre")
        ogre = random.randint(1,6)
        hero   = random.randint(1,6)
        if ogre > hero:
            print("ogre wins")
            input("press enter")
            hp -= 10
            dx=0
            dy=0
        elif ogre == hero:
            print("reroll")
            input("press enter")
            dx=0
            dy=0
        else:
            print("hero wins")
            input("press enter")
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
        print("you found a lever which opened the big door")
        input("press enter")
        dungeon[z][2] = remove_tile(44,1,0) #fragen wie!
        dungeon[z][y] = remove_tile(x,y,z)
    if tile == "<":
        if c == "" or c == "<":
            z += 1
    if tile == ">":
        if c == "" or c == ">":
            z -= 1
        
        
print("game over")

