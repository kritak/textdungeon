import random

dungeon="..q..$..f..k..f..d..$..b..f..b.t.$..f..F...m..$..c..f..s..f..b..t..f..w..v..d..b..b..t..l"
hero="@"
x=0
hunger=0
food=5
gold=0
dx=0
hp=100
key=0
mp=100
healthpot=0

helptext="""
k = key 
d = door
b = boss
f = food
$ = gold
m = mage 
c = chest
s = stairs (next lvl)
t = trap
w = wolve
F = Fountain
l = lord
q = quest
v = vendor
p = pot
e = eat
tp = teleport"""

while hp>0:
		
	print(dungeon[:x]+hero+dungeon[x+1:])
	c=input("food: {} hunger: {} gold: {} hp: {} key:{} mp: {} healthpot: {} command?".format(food,hunger,gold,hp,key,mp,healthpot))
	dx=0     # delta x gewünschte richtung
	if c == "h" or c == "help":
		print(helptext)
	if c == "a":
		dx -= 1
	if c == "d":
		dx += 1
	if c == "e" or c == "eat":
		if food <= 0:
			print("you have no food!")
			input("press enter")
		else: 
			food -= 1
			hunger -= 5
	if c == "p" or c == "pot":
		if healthpot <= 0:
			print("you got no healthpot")
			input("press enter")
		else:
			hp += 25
	if c == "tp" or c == "teleport":
		if mp <= 0:
			print("you have not enough mp")
			input("press enter")
		else:
			dx += 2
			print("you used teleport")
			mp -= 25
	if c == ("a"):
		hunger+= 1
	if c == ("d"):
		hunger+= 1
	if x+dx < 0 or x+dx >= len(dungeon)or c == "quit":
		break
		print("game over")
	
	
	#monster / boss / traps
	
	target = dungeon[x+dx]
	if target == "b":
		print("bossfight")
		bossroll = random.randint(1,6)
		heroroll = random.randint(1,6)
		print("boss rolls {} hero rolls {}".format(bossroll,heroroll))
		if bossroll == heroroll:
			print("draw")
			dx=0
		elif bossroll > heroroll:
			print("boss win")
			hp -= 20
			dx=0
		else :
			print("hero wins")
			dungeon = dungeon[:x+dx]+"."+dungeon[x+dx+1:]
		input("press enter")
	x += dx

	target = dungeon[x+dx]
	if target == "m":
		print("magefight")
		mageroll = random.randint(1,6)
		heroroll = random.randint(1,6)
		print("mage rolls {} hero rolls {}".format(mageroll,heroroll))
		if mageroll == heroroll:
			print("draw")
			dx=0
		elif mageroll > heroroll:
			print("mage win")			
			hp -= 60
			dx=0
		else :
			print("hero wins")
			dungeon = dungeon[:x+dx]+"."+dungeon[x+dx+1:]
		input("press enter")
			
	target = dungeon[x+dx]
	if target == "d":
		print ("door locked")
		doorlocked = random.randint(1,6)
		heroroll = random.randint(1,6)
		print("door locked {} hero rolls {}".format(doorlocked, heroroll))
		if doorlocked == heroroll:
			print("arrows coming")
			hp -= 10
			dx=0
		elif doorlocked > heroroll:
			print("fireball incoming")
			hp -= 50
			dx=0
		else :
			print("hero opened the door and found a small healthpot")
			hp +=30
			dungeon = dungeon[:x+dx]+"."+dungeon[x+dx+1:]
		input("press enter")
	
	target = dungeon[x+dx]
	if target == "t":
		print("Its a trap")
		trap = random.randint (1,3)
		jump = random.randint (1,6)
		print("trap {} jump {}".format(trap,jump))
		if trap > jump:
			print("youre dead")
			hp -= 70
		else :
			print("Lucky! You survived")
	target = dungeon[x+dx]
	if target == "w":
		print("wolves incoming, hide")
		wolves = random.randint (1,6)
		hide = random.randint (1,6)
		print("wolves {} hide {}".format(wolves,hide))
		if wolves > hide:
			print("you lost your food")
			food -= 3
		else :
			print("you succesfully hided from the wolves")
	target = dungeon[x+dx]			
	if target == "l":
		print("you found the lord")
		lord = random.randint (1,6)
		hero = random.randint (1,6)
		print("lord {} hero {}".format(lord,hero))
		if lord > hero:
			print("you lost")
			hp -=50
		else :
			print("you defeated the lord and succesfully finished the quest")
	
	# hunger 
		
	if hunger > 40:
			hp = 0
			print("you died")
	elif hunger > 35:
			hp -= 10
			print("youre starving")
	elif hunger > 25:
			hp -= 5
			print("you really need something to eat!")
	elif hunger > 20:
		print("youre stomache growls! eat something")
	
		
		
			
		
		#ground / food / others
	
	ground = dungeon[x]   # wo bin ich
	if ground == "f":
		food += 1
		print("you found something to eat")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
	if ground == "$":
		gold += 1
		print("you found some goldcoins")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
	if ground == "k":
		key += 1
		print("you found a key")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
	if ground == "F":
		hp += 50
		print("you see a healing fountain and got hp")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
	if ground == "c":
		key -= 1
		gold += 4
		print("you opened the chest with the key")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
	if ground == "s":
		print("congratulation! you reached the next level")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
		break
	if ground == "q":
		print("greetings hero")
		print("you found a quest")
		print("defeat lord and save the townsmen")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
	if ground == "v":
		print("an old salesman")
		print("healthpot just 2 gold")
		dungeon = dungeon[:x]+"."+dungeon[x+1:]
			



