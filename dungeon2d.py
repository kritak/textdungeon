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
    """fighting between two class instances i1 is attacking i2"""
    if i1.hp <1 or i2.hp <1:
        return
    print("{} fights {}".format(i1.name,i2.name))
    #i1.hello(False)
    #i2.hello(False)
    #---------------- p_feint (int + dex)/100
    finte = random.random() # 0-1
    i1_roll = random.randint(1,i1.attack_roll)
    if finte < (i1.intelligence+i1.dexterity)/100:
        # attacker uses feint
        if finte > (i2.intelligence+i2.dexterity)/100:
            print("feint successful! (roll x3)")
            i1_roll *= 3
    #------------------defence roll-----------------------------
    i2_roll = random.randint(1,i2.attack_roll)       
    print("{} rolls: {}, {} rolls: {} ".format(i1.name,i1_roll,i2.name,i2_roll))
    #----- did i1hit i2 ? --------------
    # --------------------- i1 hit sucessfully -----------------------
    if i1_roll > i2_roll:
        d = random.random()#  0....1
        # --- is the defender the hero ----
        armorbonus = 0
        armorvalue = 0
        itemname = ""
        if i2.__class__.__name__ == "Hero":
            slot = random.choice(slots)
            for item in item_list:
                if item.__class__.__name__ == "Wearable":
                    if item.slot == slot and item.hero_backpack and item.worn:
                        armorbonus = item.armorbonus
                        armorvalue = item.armor
                        itemname = item.name
                        break
        damage = random.randint(1,i1.damage)
        if d < i1.strength/100:
            if d > i2.strength/100:
                print("critical damage! (x3)")
                damage *= 3
        # ------------- damage greater armor? ----------
        if damage > (armorvalue+armorbonus):
            print("damage is reduced by {} points of {} ".format(armorvalue+armorbonus,itemname))
            damage -= (armorvalue+armorbonus)
        else:
            # ----- armor soaks up damage completely -------
            print("the damage {} cannot penetrate the armor {} of {}".format(damage,armorvalue+armorbonus,itemname))
            damage = 0
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
    # --------------- i1 misses, i2 attacks instead------------
    elif i1_roll == i2_roll:
        print("its a draw - no damage taken")
        i1.dx=0
        i1.dy=0
        i2.dx=0
        i2.dy=0
    else:
        print("attack failed.. no damage")
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
    
    drop = {}
    price_sum = 0
    prices = []
    
    @staticmethod
    def destiny():
        r = random.randint(0,Item.price_sum)  
        for p in Item.prices:
            if p >= r:
                return Item.drop[p]
                #break

    def __init__(self, x,y,z, symbol, carried_by_player=False):
        Dungeonobject.__init__(self, x,y,z, symbol)
        self.hero_backpack= carried_by_player # carried by hero
    
    def init2(self):
        self.weight= items[self.symbol][1]
        
class Wearable(Item):
    """wearable items (head ..shoulders..hands...)"""
    
    drop = {}
    price_sum = 0
    prices = []
    
    def init2(self):
        # what kind of wearables did we find?
        r = random.randint(0,Wearable.price_sum)  
        self.equiped = False
        for d in Wearable.prices:
            if d >= r:
                self.name = Wearable.drop[d]
                break
        
        self.weight = wearables[self.name][8]
        self.price = wearables[self.name][1]
        self.entchantmentchance = wearables[self.name][2]
        self.quality = wearables[self.name][3]
        self.wear_tear_chance = wearables[self.name][4]
        self.prot_pierce = wearables[self.name][5]
        self.prot_slice = wearables[self.name][6]
        self.prot_crush = wearables[self.name][7]
        self.slot=wearables[self.name][0]
        
        ###------ boni-----
        self.strengthbonus = 0
        self.dexteritybonus = 0
        self.intelligencebonus = 0
        self.luckbonus = 0
        self.boni = 0
        if random.random() < self.entchantmentchance:            
            if random.random() < 0.1:
                self.strengthbonus = random.randint(-1,3)
            if random.random() < 0.1:
                self.dexteritybonus = random.randint(-1,3)
            if random.random() < 0.1:
                self.intelligencebonus = random.randint(-1,3)
            if random.random() < 0.1:
                self.luckbonus = random.randint(-1,3)
            boni = 0
            if self.strengthbonus != 0:
                boni += 1
            if self.dexteritybonus != 0:
                boni += 1
            if self.intelligencebonus != 0:
                boni += 1                
            if self.luckbonus != 0:
                boni += 1
            if boni > 0:
                self.name= "{} {}".format(entchantment[boni], self.name)
                self.boni = boni
               
        ### worn item is considered to be also in backpack
        self.worn= False
        
        
class Meleeweapon(Item):
    """wearable meleeweapon"""
    
    drop = {}
    price_sum = 0
    prices = []

###"Weight",Meleerange,"Pierce","Slice","Crush",
###"Blockchance","Twohand","Specialdamage","Specialprocc",
###"Price","Dropchance","Drop"
    
    def init2(self):
        # what kind of weapon did we find?
        r = random.randint(0,Meleeweapon.price_sum)  
        self.equiped = False
        for d in Meleeweapon.prices:
            if d >= r:
                self.name = Meleeweapon.drop[d]
                break
        self.weight = meleeweapon[self.name][0]
        self.meleerange = meleeweapon[self.name][1]
        self.pierce = meleeweapon[self.name][2]
        self.slice = meleeweapon[self.name][3]
        self.crush = meleeweapon[self.name][4]
        self.blockchance = meleeweapon[self.name][5]
        self.twohand = meleeweapon[self.name][6]
        self.specialdamage = meleeweapon[self.name][7]
        self.specialprocc = meleeweapon[self.name][8]
        self.price = meleeweapon[self.name][9]
        self.entchantmentchance = meleeweapon[self.name][10]
        self.quality = meleeweapon[self.name][11]
        self.wear_tear_chance = meleeweapon[self.name][12]
        self.destroy_chance = meleeweapon[self.name][13]
        self.min_str = meleeweapon[self.name][14]
        self.min_dex = meleeweapon[self.name][15]
        self.min_int = meleeweapon[self.name][16]
        
        # ---------- boni---------------
        self.strengthbonus = 0
        self.dexteritybonus = 0
        self.intelligencebonus = 0
        self.attackbonus = 0
        self.defensebonus = 0
        self.boni = 0
        if random.random() < self.entchantmentchance:   
            if random.random() < 0.1:         
                self.strengthbonus = random.randint(-1,3)
            if random.random() < 0.1:
                self.dexteritybonus = random.randint(-1,3)
            if random.random() < 0.1:
                self.intelligencebonus = random.randint(-1,3)
            if random.random() < 0.2:
                self.attackbonus = random.randint(-1,4)
            if random.random() < 0.2:
                self.defensebonus = random.randint(-1,4)
            boni = 0
            if self.strengthbonus != 0:
                boni += 1
            if self.dexteritybonus != 0:
                boni += 1
            if self.intelligencebonus != 0:
                boni += 1 
            if self.attackbonus != 0:
                boni += 1
            if self.defensebonus != 0:
                boni += 1
            if boni > 0:
                self.name= "{} {}".format(entchantment[boni], self.name)
                self.boni = boni
        #print("i am a ", self.name)
        #input()        
        
class Monster(Dungeonobject):
    """generic monster class"""
    
    drop = {}
    price_sum = 0
    prices = []
    
    # Monster soll init von Dungeonobject haben mit extras
    # def __init__(self, x,y,z, symbol):
    #     Dungeonobject.__init__(x,y,z,symbol)

    @staticmethod
    def destiny():
        r = random.randint(0,Monster.price_sum)  
        for m in Monster.prices:
            if m >= r:
                return Monster.drop[m]
                #break

    def init2(self):

        
        self.free_slots = 2
        self.sigma=zoo[self.symbol][8]
        self.damage=zoo[self.symbol][2]
        self.attack_roll=zoo[self.symbol][1]
        self.attack1=zoo[self.symbol][3]       
        self.dx=0
        self.dy=0
        self.hp=random.gauss(zoo[self.symbol][4], self.sigma)
        self.strength=random.gauss(zoo[self.symbol][5], self.sigma)
        self.dexterity=random.gauss(zoo[self.symbol][6], self.sigma)
        self.intelligence=random.gauss(zoo[self.symbol][7], self.sigma)
        self.init3()
        
    def init3(self):
        pass
    
        
    def move(self):
        self.dx=random.randint(-1,1)
        self.dy=random.randint(-1,1)
        
    def hello(self, wait = True):
        print("---------------------------")
        print("str: {:.1f} dex: {:.1f} int: {:.1f} hp: {:.1f} hallo ich bin ein(e) {}".format(
               self.strength, self.dexterity, self.intelligence, self.hp,self.__class__.__name__))
        if wait:
            pri_input()
        
        
      #  for x in range(10):
	#print(int(round(random.gauss(0, 1),0)))
        
class Statue(Monster):
    def move(self):
        self.dx = 0
        self.dy = 0
        

class Hero(Monster):
    
    def move(self):
        pass
        
    def init3(self):
        self.history = []
        self.trophy = {}

class Lord(Monster):
    pass
    
class Ogre(Monster):
    pass

class Mage(Monster):
    
    def move(self):
        self.dx=random.randint(-4,4)
        self.dy=random.randint(-4,4)
        
class Ysera(Monster):
    def move(self):
        self.dx = 0
        self.dy = 0
    
        #items
        # class item/monster > code dupliziert "eltern klasse > object"
        
class Rect():
    """dungeon creator// a rectangle on the map used to charecterize a room"""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        
    


dungeon = [] 
monster_list = []
item_list = []

legend = ""
commands = ""

entchantment = {1:"magic",2:"rare",3:"epic",4:"legendary",5:"unique"}
slots = ("head","neck","body","hand","legs","feet")
zoo = {}
wearables = {}
meleeweapon = {}

## --------------read monster zoo values from file -------------------------------
with open(os.path.join("dungeons","zoo.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        zoo[row["Symbol"]] = [row["Name"],
                              int(row["Roll"]),
                              int(row["Damage"]),
                              row["Attack"],
                              int(row["hp"]),
                              int(row["Strength"]),
                              int(row["Dexterity"]),
                              int(row["Intelligence"]),
                              int(row["Sigma"]),
                              int(row["Price"])
                              ]
                              
max_price=0    # ----find highest price (wearables dropchance)
for z in zoo:
    if z == "@" or z == "R":
        continue
    price = zoo[z][9]
    if price > max_price:
        max_price = price
price_sum=0    # --- calculate relative wearables dropchance
for z in zoo:
    if z == "@" or z == "R":
        continue
    price = max_price*1.2-zoo[z][9]
    price_sum += price
    Monster.drop[price_sum] = z
    Monster.prices.append(price_sum)
Monster.price_sum = price_sum
Monster.prices.sort()
                              
                              
## ------------------------read wearable values from file-------------------------------
with open(os.path.join("dungeons","wearables.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        wearables[row["Name"]] = [row["Slot"],
                              int(row["Price"]),
                              float(row["Entchantmentchance"]),
                              float(row["Quality"]),
                              float(row["Wear_Tear_Chance"]),
                              int(row["Prot_Pierce"]),
                              int(row["Prot_Slice"]),
                              int(row["Prot_Crush"]),
                              float(row["Weight"])
                              ]

max_price=0    # ----find highest price (wearables dropchance)
for w in wearables:
    price = wearables[w][1]
    if price > max_price:
        max_price = price
price_sum=0    # --- calculate relative wearables dropchance
for w in wearables:
    price = max_price*1.2-wearables[w][1]
    price_sum += price
    Wearable.drop[price_sum] = w
    Wearable.prices.append(price_sum)
Wearable.price_sum = price_sum
Wearable.prices.sort()



## --------------read meleeweapon values from file -------------------------------
with open(os.path.join("dungeons","meleeweapon.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        meleeweapon[row["Name"]] = [
                              float(row["Weight"]),
                              float(row["Meleerange"]),
                              int(row["Pierce"]),
                              int(row["Slice"]),
                              int(row["Crush"]),
                              float(row["Blockchance"]),
                              int(row["Twohand"]),
                              row["Specialdamage"],
                              float(row["Specialprocc"]),
                              int(row["Price"]),
                              float(row["Entchantmentchance"]),
                              float(row["Quality"]),
                              float(row["Wear_Tear_Chance"]),
                              float(row["Destroy_Chance"]),
                              int(row["min_str"]),
                              int(row["min_dex"]),
                              int(row["min_int"])
                                ]
max_price=0    # ----find highest price (meleedropchance)
for mw in meleeweapon:
    price = meleeweapon[mw][9]
    if price > max_price:
        max_price = price
price_sum=0    # --- calculate relative meleedropchance
for mw in meleeweapon:
    price = max_price*1.2-meleeweapon[mw][9]
    price_sum += price
    Meleeweapon.drop[price_sum] = mw
    Meleeweapon.prices.append(price_sum)
Meleeweapon.price_sum = price_sum
Meleeweapon.prices.sort()    




items = {}
with open(os.path.join("dungeons","items.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        #print(row["Symbol"], row["Name"])
        items[row["Symbol"]] = [row["Name"], float(row["Weight"]), int(row["Price"])]
        
max_price=0    # ----find highest price (random item dropchance)
for i in items:
    price = items[i][2]
    if price > max_price:
        max_price = price
price_sum=0    # --- calculate relative random item dropchance
for i in items:
    price = max_price*1.2-items[i][2]
    price_sum += price
    Item.drop[price_sum] = i
    Item.prices.append(price_sum)
Item.price_sum = price_sum
Item.prices.sort()

        

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
                    if char == "r":
                            #random item
                            char = Item.destiny()
                    if char == "R":
                            char = Monster.destiny()
                    if char in items:
                        #-------------  items   -----------
                        if char == "w":
                            item_list.append(Wearable(lx,ly,lz,char))
                        elif char == "m":
                            item_list.append(Meleeweapon(lx,ly,lz,char))
                        else:
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
                        elif char == "Y":
                            monster_list.append(Ysera(lx,ly,lz,char))
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
turns = 0
victory = False
while hero.hp >0 and not victory:
    turns += 1
    
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
    c = input("hp: {} mp: {} hunger: {} \ntype help or enter command:".format(int(hero.hp),hero.mp,hero.hunger))
    
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
        cls()
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
        print("amount weight   name:")
        for i in rucksack:
            print(" {:3.0f}   {:5.1f}     {}".format(rucksack[i][0],rucksack[i][1],i))  
        w = 1
        while w != 0:
            
            print("-----------------------------\ndetailed list of wearables\n-----------------------------")
            for item in item_list:
                if item.symbol == "w" and item.hero_backpack:
                    print(" {} {} q: {:3.1f}% ({}) {} {}".format(
                          item.number,item.slot, item.quality*100,"worn" if item.worn else "pack",item.name, 
                          "" if item.boni == 0 else "\n                    boni: str {} dex {} int {} luck {}".format(
                          item.strengthbonus,item.dexteritybonus,item.intelligencebonus,item.luckbonus)))
            w = input("enter number of item to wear/remove or press enter to continue")
            cls()
            try:
                w = int(w)
            except:
                w = 0
            if w > 0:
                slot = False
                for item in item_list:
                    if item.__class__.__name__ == "Wearable":
                        if item.number == w and item.hero_backpack:
                            if item.worn:
                                item.worn = False
                            else:
                                item.worn = True
                                slot = item.slot
                if slot:   #remove wearable
                    for item in item_list:
                        if item.__class__.__name__ == "Wearable":
                            if item.number != w and item.hero_backpack and item.slot == slot:
                                item.worn = False
                print("you have changed your equipment!")
            ### weaponscreen####
        m = 1
        while m != 0:
                
            print("-----------------------------\ndetailed list of meleeweapon\n-----------------------------")
            for item in item_list:
                if item.symbol == "m" and item.hero_backpack:
                    print(" {} ra: {} q: {:3.1f}% ({}) ({}) {} {} {}".format(
                          item.number,item.meleerange, item.quality*100, "equiped" if item.equiped else "pack","2h" if item.twohand else "1h",item.name, 
                          "" if item.boni == 0 else "\n                    boni: att {} def {} str {} dex {} int {}".format(
                          item.attackbonus,item.defensebonus,item.strengthbonus,item.dexteritybonus,item.intelligencebonus),
                          "" if hero.strength >= item.min_str and hero.dexterity >= item.min_dex and hero.intelligence >= item.min_int else
                          "\n                    malus: (hero not qualified) min_str {} str {} min_dex {} dex {} min_int {} int {}".format(
                           item.min_str, hero.strength,item.min_dex,hero.dexterity,item.min_int,hero.intelligence)))
            m = input("enter number of item to wield/unwield or press enter to continue")
            cls()
            try:
                m = int(m)
            except:
                m = 0
            if m > 0:
                for item in item_list:
                    if item.__class__.__name__ == "Meleeweapon":
                        if item.number == m and item.hero_backpack:
                            if item.equiped:
                                item.equiped = False
                                if item.twohand:
                                    hero.free_slots += 2
                                else:
                                    hero.free_slots += 1                            
                            else:
                                if hero.free_slots < 1:
                                    print("you have no free weaponslot left! please unequip weapon(s) first")
                                elif hero.free_slots < 2 and item.twohand:
                                    print("remove both weapon(s) first to equip a 2h weapon")
                                else:
                                    item.equiped = True 
                                    if item.twohand:
                                        hero.free_slots -= 2
                                    else:
                                        hero.free_slots -= 1    
                
                    
        
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
       # if hero.healthpot <=0:
        if  len([i for i in item_list if i.hero_backpack and i.name == "healthpot"]) <= 0:
            pri_input("you have no healthpot")
        else:
           # hero.healtpot -=1
            n=-1
            for i in item_list:
                if i.hero_backpack and i.name == "healthpot":
                    n= i.number
                    break
            item_list = [i for i in item_list if i.number != n]          
            hero.hp += random.randint(5,10)
    elif c == "t" or c == "teleport":
        hero.hunger += 20
        hero.x,hero.y,hero.z = teleport(hero.z)
        
    elif (c == "esc" or c == "escape") and hero.z >0:  
        hero.hunger += 15
        hero.hp = 1
        hero.x,hero.y,hero.z = teleport(hero.z-1)   
        
    elif c == "c" or c == "check" or c == "sniff":
        # check stats of monsters nearby
        for dy in [-1,0,1]:
            for dx in [-1,0,1]:
                for mymonster in monster_list:
                    if mymonster.z == hero.z and mymonster.x == hero.x+dx and mymonster.y == hero.y+dy:
                        mymonster.hello(wait = False)
        pri_input()

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
        #        hero has at least 1 key?
        if len([i for i in item_list if i.hero_backpack and i.name == "key"]) > 0:
            n=-1
            for i in item_list:
                if i.hero_backpack and i.name == "key":
                    n= i.number
                    break
            item_list = [i for i in item_list if i.number != n]
            dungeon[hero.z][hero.y+hero.dy] = remove_tile(hero.x+hero.dx,hero.y+hero.dy,hero.z)
        else:
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
                    fight(hero,mymonster)
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
                    fight(mymonster,hero)
                    if mymonster.hp <1:
                        # monster down , drop?
                        # special drop
                        if mymonster.__class__.__name__ == "Ysera":
                            #remove door when dragon slain @level 5
                            dungeon[4][9] = remove_tile(40,9,4)
                        if mymonster.__class__.__name__ == "Lord":
                            print("you have slain the dark lord and completed the quest")
                            victory = True                            
                        if random.random() <0.25:
                            item_list.append(Item(mymonster.x,mymonster.y,mymonster.z,random.choice(("$","f","p","k","w"))))
                            print("the monster dropped something!")
                        hero.history.append("turn {}: slain a {}".format(turns,mymonster.__class__.__name__))
                        m = mymonster.__class__.__name__
                        if m in hero.trophy:
                            hero.trophy[m] += 1
                        else:
                            hero.trophy[m] = 1
                    input("press enter to continue")
                    
    #  remove monster from monsterlist
    monster_list = [m for m in monster_list if m.hp > 0]
     

    
    # movement
    hero.x += hero.dx
    hero.y += hero.dy

#### for x in range(20):
####print("str",random.gauss(10, 2),"int",random.gauss(5, 1))

        
        
print("game over")

print("history of hero:")
input("press enter to continue")
for m in hero.trophy:
    print(m,hero.trophy[m])
for line in hero.history:
    print(line)
