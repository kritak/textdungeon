"""
2D dungeon with python
by Andreas Schmuck 2015"""

import random

legend="""
.    floor
#    wall
@    hero
f	 food
$	 coins
t	 trap
d 	 door
k 	 key
B	 boss
M	 mage"""

dungeon="""
###################################################
#.................................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
#.................................................#
###################################################"""

# hero start posi 1/1

hp=10
x=1
y=1
dx=0
dy=0

while hp >0:
	
	line_number = 0
	for line in dungeon.split():
		if line_number == y:
			print(line[:x]+"@"+line[x+1:])
		else:
			print(line)
		line_number += 1
	c = input("hp: {} command?".format(hp))
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
	tile = dungeon.split()[y+dy][x+dx]
	if tile == "#":
		print("you run into a wall, ouch!")
		hp -= 1
		dx=0
		dy=0
	# movement
	x += dx
	y += dy

print("game over")

