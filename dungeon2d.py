"""
2D dungeon with python
by Andreas Schmuck 2015"""

import random

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
S    statue"""

dungeon="""
###################################################
#.....S...........................................#
#.................................................#
#.....S...$.......................................#
#.................................................#
#.......$.........................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
###################################################"""
dungeon = dungeon.split()


# hero start posi 1/1

hp=10
x=1
y=1
dx=0
dy=0
gold=0

while hp >0:
    
    line_number = 0
    for line in dungeon:
        if line_number == y:
            print(line[:x]+"@"+line[x+1:])
        else:
            print(line)
        line_number += 1
    c = input("hp: {} gold: {} command?".format(hp,gold))
    dx= 0
    dy= 0
    if c == "quit":
        break
    if c == "a":
        dx -= 1
    if c == "d":
        dx += 1
    if c == "w":
        dy -= 1
    if c == "s":
        dy += 1
    tile = dungeon[y+dy][x+dx]
    # check movement
    if tile == "#":
        print("you run into a wall, ouch!")
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
            hp -= 2
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
            dungeon[y+dy] = dungeon[y+dy][:x+dx] + "." + dungeon[y+dy][x+dx+1:]
    # movement
    x += dx
    y += dy
    # hero stays on special tile
    tile = dungeon[y][x]
    if tile == "$":
        print("you found gold!")
        input("press enter")
        gold += 1
        dungeon[y] = dungeon[y][:x] + "." + dungeon[y][x+1:] # replace gold with .
print("game over")

