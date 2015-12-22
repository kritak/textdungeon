"""
2D dungeon with python
by Andreas Schmuck 2015
course project of http://spielend-programmieren.at

dungeons must be in folder dungeons
dungeon file must be ".txt" file
file name should start with "dungeon"

"""

import random
import os
import csv



def cls():
    """clear the screen for windows,mac,linus"""
    os.system('cls' if os.name=='nt' else 'clear')

def remove_tile(x,y,z,new_tile="."):
    """replace tiles / items with new tile"""
    return  dungeon[z][y][:x] + new_tile + dungeon[z][y][x+1:]

def pri_input(txt=""):
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

def fight(i1,i2):
    """fighting between two class instances"""
    if i1.hp <1 or i2.hp <1:
        return
    print("{} fights {}".format(i1.name,i2.name))
    i1_roll = random.randint(1,i1.attack_roll)
    i2_roll = random.randint(1,i2.attack_roll)       
    print("{} rolls: {}, {} rolls: {} ".format(i1.name,i1_roll,i2.name,i2_roll))
    if i1_roll == i2_roll:
        print("its a draw - no damage taken")
        i1.dx=0
        i1.dy=0
        i2.dx=0
        i2.dy=0
    elif i1_roll > i2_roll:
        damage = random.randint(1,i1.damage)
        i2.hp -= damage
        print("{} wins this round and makes {} damage".format(i1.name, damage))
        print("{} has {} hp left".format(i2.name,int(i2.hp)))
        if i2.hp < 1:
            print("{} lose, {} wins the fight".format(i2.name,i1.name))
        else:
            i1.dx=0
            i1.dy=0
            i2.dx=0
            i2.dy=0
    else:
        damage = random.randint(1,i2.damage)
        i1.hp -= damage
        print("{} wins this round and makes {} damage".format(i2.name, damage))
        print("{} has {} hp left".format(i1.name,int(i1.hp)))
        if i1.hp < 1:
            print("{} lose, {} wins the fight".format(i1.name,i2.name))
        else:
            i1.dx=0
            i1.dy=0
            i2.dx=0
            i2.dy=0
            
            
class Dungeonobject():
    """positioning for items / monsters"""
    number = 0
    
    def __init__(self,x,y,z, symbol):
        self.x=x
        self.y=y
        self.z=z
        self.symbol= symbol
        self.weight= 0
        self.number=Dungeonobject.number
        #self.hero_backpack = carried_by_player
        Dungeonobject.number += 1
        if self.symbol in zoo:
            self.name=zoo[self.symbol][0] 
        elif self.symbol in items:
            self.name=items[self.symbol][0]
        else:
            pri_input("symbol not found: {}".format(self.symbol))
            # error!!!
        self.init2()
    
    def init2(self):
        pass
    
            
class Item(Dungeonobject):
    """moveable items in dungeons"""

    def __init__(self, x,y,z, symbol, carried_by_player=False):
        Dungeonobject.__init__(self, x,y,z, symbol)
        self.hero_backpack= carried_by_player # carried by hero
    
    def init2(self):
        self.weight= items[self.symbol][1]
        


class Monster(Dungeonobject):
    """generic monster class"""
    
    # Monster soll init von Dungeonobject haben mit extras
    # def __init__(self, x,y,z, symbol):
    #     Dungeonobject.__init__(x,y,z,symbol)

    def init2(self):
        self.damage=zoo[self.symbol][2]
        self.attack_roll=zoo[self.symbol][1]
        self.attack1=zoo[self.symbol][3]       
        self.dx=0
        self.dy=0
        self.hp=zoo[self.symbol][4]
        self.init3()
        
    def init3(self):
        pass
    
        
    def move(self):
        pass
        
class Statue(Monster):
    pass

class Hero(Monster):
    
    def init3(self):
       pass
    
class Lord(Monster):
    def move(self):
        self.dx=random.randint(-1,1)
        self.dy=random.randint(-1,1)
        
class Ogre(Monster):
    def move(self):
        self.dx=random.randint(-1,1)
        self.dy=random.randint(-1,1)

class Mage(Monster):
    def move(self):
        self.dx=random.randint(-4,4)
        self.dy=random.randint(-4,4)
    
        #items
        # class item/monster > code dupliziert "eltern klasse > object"
        


dungeon = [] 
monster_list = []
item_list = []

legend = ""
commands = ""


## read zoo from file
zoo = {}
print("welcome in the dungeon you will find this monsters in this game\n")
with open(os.path.join("dungeons","zoo.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row["Symbol"], row["Name"], row["Roll"], row["Damage"], row["Attack"], row["hp"])
        zoo[row["Symbol"]] = [row["Name"], int(row["Roll"]), int(row["Damage"]), row["Attack"], int(row["hp"])]
input("\npress enter")

items = {}
with open(os.path.join("dungeons","items.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        print(row["Symbol"], row["Name"])
        items[row["Symbol"]] = [row["Name"], float(row["Weight"])]
input("\npress enter")
        

## read dungeon from file / legend / help / commands
for root, dirs, files in os.walk('dungeons'):
    lz = 0
    filelist = []
    for file in files:
        filelist.append(file)
    filelist.sort()
    for file in filelist:
        print("processing:", file)
        if file[0:7] == "dungeon" and file[-4:] == ".txt":
            mylevel = open(os.path.join("dungeons",file))
            lines =  mylevel.read().splitlines()
            ly = 0
            for line in lines:
                lx = 0
                for char in line:
                    if char in items:
                        #-------------  items   -----------
                        item_list.append(Item(lx,ly,lz,char))
                        line = line[:lx]+"."+line[lx+1:]
                    if char in zoo:                   
                        # ----------  monster   ------------                      
                        if char == "@":
                            hero= Hero(lx,ly,lz,char)
                            monster_list.append(hero)
                        elif char == "S":
                            monster_list.append(Statue(lx,ly,lz,char))
                        elif char == "L":
                            monster_list.append(Lord(lx,ly,lz,char))
                        elif char == "O":
                            monster_list.append(Ogre(lx,ly,lz,char))
                        elif char == "M":
                            monster_list.append(Mage(lx,ly,lz,char))
                        #monster_list.append(Monster(lx,ly,lz,char))
                        line = line[:lx]+"."+line[lx+1:]
                    lx += 1
                lines[ly] = line
                ly+=1
            lz += 1            
            #print(lines)
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

pri_input(commands)



hero.hp=500
hero.hpmax=1000
hero.mp=100
hero.hunger=0
#hero.food=50
hero.healthpot=0

hero.dx=0
hero.dy=0
# add 50 food
for x in range(50):
    item_list.append(Item(0,0,0,"f",carried_by_player=True)) 
    
while hero.hp >0:
    
    #     --------------paint the dungeon------------------
    
    cls()
    print("food: {} gold: {} key: {} healthpot: {} inv: {}".format(
          len([i for i in item_list if i.hero_backpack and i.name == "food"]),
          len([i for i in item_list if i.hero_backpack and i.name == "gold"]),
          len([i for i in item_list if i.hero_backpack and i.name == "key"]),
          len([i for i in item_list if i.hero_backpack and i.name == "healthpot"]),
          len([i for i in item_list if i.hero_backpack])))
    line_number = 0
    for line in dungeon[hero.z]:
        pline = line[:]
        myline = ""
        
        
        #       ------ items/monster ------
 
       
        for x in range(len(pline)):
            stash = []
            monster = False
            mychar = pline[x]
            for mymonster in monster_list:
                if mymonster.z == hero.z and mymonster.y == line_number and mymonster.x == x:
                    monster = True
                    mychar=mymonster.symbol 
            if not monster:        
                for item in item_list:
                    if not item.hero_backpack and item.z == hero.z and item.y == line_number and item.x == x:
                        stash.append(item)
                if len(stash) == 1:
                    mychar=stash[0].symbol
                elif len(stash) > 1:
                    mychar = "?"
            myline += mychar   
        print(myline)
        line_number += 1
    # hero stays on special tile?
    tile = dungeon[hero.z][hero.y][hero.x]
    #   items // if item.x == hero.x....
    ####  hero found items?####
    stash = []
    for item in item_list:
        if hero.z == item.z and not item.hero_backpack:
            if hero.y == item.y:
                if hero.x == item.x:
                    stash.append(item)
                    
    if len(stash) > 0:
        print("you found {} item{}:".format(len(stash),"" if len(stash) == 1 else "s"))
        for i in stash:
            print(i.name)
        print("press enter to pick up all items")
        
    if tile == "1":
        print("you found a lever which opened the big door")
        #dungeon[1] = dungeon [1][:4] + "." + dungeon[1][4+1:] #x + y coordinate zum entfernen!!!
        dungeon[hero.z][1] = remove_tile(44,1,hero.z) #entfernt türe bei x(4) y(1) siehe 1 zeile weiter oben
        dungeon[hero.z][hero.y] = remove_tile(hero.x,hero.y,hero.z)
    elif tile == "2":
        print("you found a lever which opened the big door in lvl one")
        dungeon[0][1] = remove_tile(42,1,0)
        dungeon[hero.z][hero.y] = remove_tile(hero.x,hero.y,hero.z)
    elif tile =="<":
        print("you found a stair up (press Enter to climb up)")
    elif tile ==">":
        print("you found a stair down (press Enter to climb down)")
        
    # -----------food clock -------------------
    hero.hp += 0.1
    hero.hp = min(hero.hp,hero.hpmax)
    if hero.hunger > 40:
            hero.hp = 0
            print("you died")
            break
    elif hero.hunger > 35:
            hero.hp -= 10
            print("youre starving")
    elif hero.hunger > 25:
            hero.hp -= 5
            print("you really need something to eat!")
    elif hero.hunger > 20:
        print("youre stomache growls! eat something")  
    
    # ---------- ask for new command ----------
    c = input("hp: {} mp: {} hunger: {} \ncommand?".format(int(hero.hp),hero.mp,hero.hunger))
    
    #-------------items-------------
    if len(stash) > 0:
        if c == "":
            for i in stash:
                i.hero_backpack = True
            continue
    
    
    hero.dx= 0
    hero.dy= 0
    # -------- movement -----------
    if tile == "<":
        if c == "" or c == "<":
            if hero.z == 0:
                pri_input("you leave the dungeon and return to town")
                break
            hero.z -= 1  # climb up
            hero.hunger += 2
    elif tile == ">":
        if c == "" or c == ">":
            if hero.z == len(dungeon)-1:
                pri_input("you already reached the deepest dungeon")
            else:
                hero.z += 1    # climb down
                hero.hunger += 2
    if c == "a":   
        hero.dx -= 1                # left
    elif c == "d":
        hero.dx += 1                # right
    elif c == "w":
        hero.dy -= 1                # up
    elif c == "s":
        hero.dy += 1                # down
    if hero.dx != 0 or hero.dy != 0:
        hero.hunger+=0.5
    #---------------- other commands (non- movement) -------------
    if c == "quit" or c == "exit":
        break
        
        
        
    # ------------------inventory----------------------
    
    
    elif c == "i" or c == "inventory":
        rucksack = {}
        for item in item_list:
            if item.hero_backpack:
                if item.name in rucksack:
                    rucksack[item.name][0] += 1
                    rucksack[item.name][1] += item.weight
                else:
                    rucksack[item.name] = [1,item.weight]
               # print(item.name,item.weight)
        #-----output inventory------
        print("player inventory:")
        print("name     amount   weight:")
        for i in rucksack:
            print(" {}    {}    {}".format(i,rucksack[i][0],rucksack[i][1]))        
        pri_input()
        
    elif c == "x" or c == "drop":
        rucksack = {}
        for item in item_list:
            if item.hero_backpack:
                if item.name in rucksack:
                    rucksack[item.name][0] += 1
                    rucksack[item.name][1] += item.weight
                else:
                    rucksack[item.name] = [1,item.weight]
        print("player inventory:")
        print("name     amount   weight:")
        for i in rucksack:
            print(" {}    {}    {}".format(i,rucksack[i][0],rucksack[i][1]))
        what=input("what do you want to drop?")
        if what in rucksack:
            amount = input("how much do you want to drop?")
            try:
                amount = int(amount)
            except:
                print("wrong amount!")
                continue
            for a in range(amount):
                for item in item_list:
                    if item.name == what and item.hero_backpack:
                        item.hero_backpack = False 
                        item.x,item.y,item.z = hero.x,hero.y,hero.z
                        print("dropped 1 {}".format(item.name))
                        break
            pri_input()
                        
                    
                
    elif c == "help" or c == "?":
        pri_input(legend)
        pri_input(commands)

    elif c == "e" or c == "eat":
        
        #if hero.food <= 0:
        if  len([i for i in item_list if i.hero_backpack and i.name == "food"]) <= 0:
            
            pri_input("you have no food!")
        else: 
            #hero.food -= 1
            n=-1
            for i in item_list:
                if i.hero_backpack and i.name == "food":
                    n= i.number
                    break
            item_list = [i for i in item_list if i.number != n]
            hero.hunger -= 5
            hero.hunger = max(0,hero.hunger) 
    elif c == "p" or c == "healthpot":
        if hero.healthpot <=0:
            pri_input("you have no healthpot")
        else:
            hero.healtpot -=1
            hero.hp += 10
    elif c == "t" or c == "teleport":
        hero.hunger += 20
        hero.x,hero.y,hero.z = teleport(hero.z)
        
    elif (c == "esc" or c == "escape") and hero.z >0:  
        hero.hunger += 15
        hero.hp = 1
        hero.x,hero.y,hero.z = teleport(hero.z-1)    

    # -------- check if movement is possible -------------
    tile = dungeon[hero.z][hero.y+hero.dy][hero.x+hero.dx]
    if tile == "#":   # hero runs into wall
        pri_input("you run into a wall, ouch!")
        hero.hp -= 1
        hero.dx=0
        hero.dy=0
    if tile == "D":   # hero runs into door
        pri_input("a big door find a way to open it")
        hero.dx=0
        hero.dy=0
    if tile == "d":
        pri_input("a small door find a key to open it")
        hero.dx=0
        hero.dy=0

        
    
    
    
    
    # ----------- monster movement-----------------
    
    occupied = []
    for mymonster in monster_list:
        if mymonster.z == hero.z:
            occupied.append((mymonster.x,mymonster.y))
    
    for mymonster in monster_list:
        if mymonster.number == hero.number:
            continue
        if mymonster.z == hero.z:
            mymonster.move()# makes new dx/dy for monster
            # mage shall not jump out of dungeon
            width = len(dungeon[hero.z][0])
            height = len(dungeon[hero.z])
            if mymonster.x+mymonster.dx < 0 or mymonster.x+mymonster.dx >= width:
                mymonster.dx = 0
            if mymonster.y+mymonster.dy < 0 or mymonster.y+mymonster.dy >= height:
                mymonster.dy = 0    
                
            tile = dungeon[mymonster.z][mymonster.y+mymonster.dy][mymonster.x+mymonster.dx]
            if tile == "#" or tile == "D":
                mymonster.dx=0
                mymonster.dy=0
            elif mymonster.x+mymonster.dx == hero.x:
                if mymonster.y+mymonster.dy == hero.y:
                    fight(mymonster,hero)
                    input("press enter to continue")
            else:
                if (mymonster.x+mymonster.dx,mymonster.y+mymonster.dy) in occupied:
                    mymonster.dx = 0 
                    mymonster.dy = 0
                else:
                    # clear old position
                    occupied.remove((mymonster.x,mymonster.y))
                    mymonster.x += mymonster.dx
                    mymonster.y += mymonster.dy
                    occupied.append((mymonster.x,mymonster.y))
                
    # ----------- monster  battle -----------------
    
    for mymonster in monster_list:
        if mymonster.number == hero.number:
            # hero himself
            continue # proceed to next monster in monster_list
        if mymonster.z == hero.z:
            if mymonster.y == hero.y+hero.dy:
                if mymonster.x == hero.x+hero.dx:
                    fight(hero,mymonster) #fight
                    if mymonster.hp <1:
                        # monster down , drop?
                        if random.random() <0.25:
                            item_list.append(Item(mymonster.x,mymonster.y,mymonster.z,random.choice(("$","f","p","k"))))
                            print("the monster dropped something!")
                    input("press enter to continue")
                    
    #  remove monster from monsterlist
    monster_list = [m for m in monster_list if m.hp > 0]
     

    
    # movement
    hero.x += hero.dx
    hero.y += hero.dy


        
        
print("game over")

