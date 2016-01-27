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
    return  Game.dungeon[z][y][:x] + new_tile + Game.dungeon[z][y][x+1:]

def pri_input(txt=""):
    """print and wait for input"""
    print(txt)
    input("press enter")

def teleport(z):
    """teleport the player to a random floor in lvl z"""
    x = random.randint(1,len(Game.dungeon[z][1])-2)
    y = random.randint(1,len(Game.dungeon[z])-2)
    if Game.dungeon[z][y][x] != "." :
        x,y = teleport(z)
    return x,y,z

def fight(i1,i2):
    """fighting between two class instances i1 is attacking i2"""
    if i1.hp <1 or i2.hp <1:
        return
    print("{} fights {}".format(i1.name,i2.name))
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
            slot = random.choice(Game.slots)
            for item in Game.item_list:
                if item.__class__.__name__ == "Wearable":
                    if item.slot == slot and item.carried_by == Game.hero.number and item.worn:
                        #armorbonus = item.armorbonus
                        #armorvalue = item.armor
                        itemname = item.name
                        break
        damage = random.randint(1,i1.damage)
        if i1.__class__.__name__ == "Hero" and Game.instakill: 
            damage = 500
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
        #else:
           # i1.dx=0
           # i1.dy=0
           # i2.dx=0
           # i2.dy=0
    # --------------- i1 misses, i2 attacks instead------------
    elif i1_roll == i2_roll:
        print("its a draw - no damage taken")
       # i1.dx=0
       # i1.dy=0
       # i2.dx=0
       # i2.dy=0
    else:
        print("attack failed.. no damage")
       # i1.dx=0
       # i1.dy=0
       # i2.dx=0
       # i2.dy=0
            
            
class Dungeonobject():
    """positioning for items / monsters"""
    number = 1 #important to start with 1 because 0 == false
    
    def __init__(self,x,y,z, symbol):
        self.x=x
        self.y=y
        self.z=z
        self.dx=0
        self.dy=0
        self.symbol= symbol
        self.weight= 0
        self.number=Dungeonobject.number
        Dungeonobject.number += 1
        self.carried_by = 0
        if self.symbol in Game.zoo:
            self.name=Game.zoo[self.symbol][0] 
        elif self.symbol in Game.items:
            self.name=Game.items[self.symbol][0]
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

    def __init__(self, x,y,z, symbol, carried_by=False):
        Dungeonobject.__init__(self, x,y,z, symbol)
        self.carried_by= carried_by
    
    def init2(self):
        self.weight= Game.items[self.symbol][1]
        
        
class Pot(Item):
    """useable pots"""
    
    drop = {}
    price_sum = 0
    prices = []
    
        
        
    def init2(self):
        #print(Pot.drop, Pot.price_sum, Pot.prices)
        #pri_input()
        # what kind of pot did we find?
        r = random.randint(0,Pot.price_sum)  
        for d in Pot.prices:
            if d >= r:
                self.name = Pot.drop[d]
                break
        self.price = Game.pots[self.name][0]
        self.weight = Game.pots[self.name][1]
        if self.name == "Mysterypot":
            self.turns = random.randint(6, 10)
            self.e_str = random.randint(-5, 5)
            self.e_dex = random.randint(-5, 5)
            self.e_int = random.randint(-5, 5)
            self.e_hp = random.randint(-40, 40)
            
        else:
            self.turns = Game.pots[self.name][2]
            self.e_str = Game.pots[self.name][3]
            self.e_dex = Game.pots[self.name][4]
            self.e_int = Game.pots[self.name][5]
            self.e_hp = Game.pots[self.name][6]  
            
        
    
class Wearable(Item):
    """wearable items (head ..shoulders..hands...)"""
    
    drop = {}
    price_sum = 0
    prices = []
    
    
    def __init__(self, x,y,z, symbol, carried_by=False, slot="?"):
        Dungeonobject.__init__(self, x,y,z, symbol)
       # self.hero_backpack= carried_by # carried by hero
        self.carried_by= carried_by
        self.slot = slot
    
    #def init2(self):
        # what kind of wearables did we find?
        while True:
             r = random.randint(0,Wearable.price_sum)  
             for d in Wearable.prices:
                 if d >= r:
                      self.name = Wearable.drop[d]
                      break
             # we have a random wearable
             # check for correct slot
             if self.slot == "?":
                 break # take this wearable
             if self.slot == Game.wearables[self.name][0]:
                 break # correct slot, continue
        
        self.equiped = False
        self.weight = Game.wearables[self.name][8]
        self.price = Game.wearables[self.name][1]
        self.entchantmentchance = Game.wearables[self.name][2]
        self.quality = Game.wearables[self.name][3]
        self.wear_tear_chance = Game.wearables[self.name][4]
        self.prot_pierce = Game.wearables[self.name][5]
        self.prot_slice = Game.wearables[self.name][6]
        self.prot_crush = Game.wearables[self.name][7]
        self.slot=Game.wearables[self.name][0]
        
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
                self.name= "{} {}".format(Game.entchantment[boni], self.name)
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
        self.weight = Game.meleeweapons[self.name][0]
        self.meleerange = Game.meleeweapons[self.name][1]
        self.pierce = Game.meleeweapons[self.name][2]
        self.slice = Game.meleeweapons[self.name][3]
        self.crush = Game.meleeweapons[self.name][4]
        self.blockchance = Game.meleeweapons[self.name][5]
        self.twohand = Game.meleeweapons[self.name][6]
        self.specialdamage = Game.meleeweapons[self.name][7]
        self.specialprocc = Game.meleeweapons[self.name][8]
        self.price = Game.meleeweapons[self.name][9]
        self.entchantmentchance = Game.meleeweapons[self.name][10]
        self.quality = Game.meleeweapons[self.name][11]
        self.wear_tear_chance = Game.meleeweapons[self.name][12]
        self.destroy_chance = Game.meleeweapons[self.name][13]
        self.min_str = Game.meleeweapons[self.name][14]
        self.min_dex = Game.meleeweapons[self.name][15]
        self.min_int = Game.meleeweapons[self.name][16]
        
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
                self.name= "{} {}".format(Game.entchantment[boni], self.name)
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
        """sucht monster aus"""
        r = random.randint(0,Monster.price_sum)  
        for m in Monster.prices:
            if m >= r:
                return Monster.drop[m]
                #break

    def init2(self):

        
        self.free_slots = 2
        self.sigma=Game.zoo[self.symbol][8]
        self.damage=Game.zoo[self.symbol][2]
        self.attack_roll=Game.zoo[self.symbol][1]
        self.attack1=Game.zoo[self.symbol][3]       
        self.dx=0
        self.dy=0
        self.jumprange = 1
        self.hp=random.gauss(Game.zoo[self.symbol][4], self.sigma)
        self.strength=random.gauss(Game.zoo[self.symbol][5], self.sigma)
        self.dexterity=random.gauss(Game.zoo[self.symbol][6], self.sigma)
        self.intelligence=random.gauss(Game.zoo[self.symbol][7], self.sigma)
        self.states ={"patrol": ["hunt","sleep","fight"],
                     "sleep": ["patrol"],
                     "hunt": ["fight","patrol"],
                     "fight": ["patrol","hunt","flee"],
                     "flee": ["patrol"]}
        self.state = "patrol"
        self.sniffrange = 3
        self.effects_str = []
        self.effects_dex = []
        self.effects_int = []
        self.effects_hp = []
        self.effects_str_bonus = 0
        self.effects_dex_bonus = 0
        self.effects_int_bonus = 0
        self.effects_hp_bonus = 0
        self.init3()
        
    def init3(self):
        pass
        
    def stat_effects_tick(self):
        """decrease the duration of stat effects"""
        
        self.effects_str = [[a-1,b] for [a,b] in self.effects_str if a > 0]
        self.effects_dex = [[a-1,b] for [a,b] in self.effects_dex if a > 0]
        self.effects_int = [[a-1,b] for [a,b] in self.effects_int if a > 0]
        self.effects_hp = [[a-1,b] for [a,b] in self.effects_hp if a > 0]
        self.effects_str_bonus = 0
        self.effects_dex_bonus = 0
        self.effects_int_bonus = 0
        self.effects_hp_bonus = 0

        """calculate maximal negative or positiv str effect for this turn"""
        if len(self.effects_str) > 0:
            maxvalues = [b for [a,b] in self.effects_str if b > 0]
            minvalues = [b for [a,b] in self.effects_str if b < 0]
            if len(maxvalues) > 0:
                maxeffect = max(maxvalues)
            else:
                maxeffect = 0
            if len(minvalues) > 0:
                mineffect = min(minvalues)
            else:
                mineffect = 0
            self.effects_str_bonus = maxeffect + mineffect
            
        #    self.effects_str_bonus = max([b for [a,b] in self.effects_str if b > 0]) - min([b for [a,b] in self.effects_str if b < 0])
        if len(self.effects_dex) > 0:
            maxvalues = [b for [a,b] in self.effects_dex if b > 0]
            minvalues = [b for [a,b] in self.effects_dex if b < 0]
            if len(maxvalues) > 0:
                maxeffect = max(maxvalues)
            else:
                maxeffect = 0
            if len(minvalues) > 0:
                mineffect = min(minvalues)
            else:
                mineffect = 0
            self.effects_dex_bonus = maxeffect + mineffect
             
        if len(self.effects_int) > 0:
            maxvalues = [b for [a,b] in self.effects_int if b > 0]
            minvalues = [b for [a,b] in self.effects_int if b < 0]
            if len(maxvalues) > 0:
                maxeffect = max(maxvalues)
            else:
                maxeffect = 0
            if len(minvalues) > 0:
                mineffect = min(minvalues)
            else:
                mineffect = 0
            self.effects_int_bonus = maxeffect + mineffect
            
            
        if len(self.effects_hp) > 0:
            maxvalues = [b for [a,b] in self.effects_hp if b > 0]
            minvalues = [b for [a,b] in self.effects_hp if b < 0]
            if len(maxvalues) > 0:
                maxeffect = max(maxvalues)
            else:
                maxeffect = 0
            if len(minvalues) > 0:
                mineffect = min(minvalues)
            else:
                mineffect = 0
            self.effects_hp_bonus = maxeffect + mineffect
            
            
        
    def drink(self,potion):
        """stats effects from potions"""
        #potion is the Pot class instance
        
        if potion.e_str != 0:
            if potion.turns == 0:
                # perma
                self.strength += potion.e_str
            else:
                #  temporary
                #[[4, 2], [13, 1], [2, -2], [0, -5]]
                #>>> [[a-1,b] for [a,b] in s2 if a>0]
                # duration, effect
                self.effects_str.append([potion.turns, potion.e_str])
        
        if potion.e_dex != 0:
            if potion.turns == 0:
                self.dexterity += potion.e_dex
            else:
                self.effects_dex.append([potion.turns, potion.e_dex])
                
        if potion.e_int != 0:
            if potion.turns == 0:
                self.intelligence += potion.e_int
            else:
                self.effects_int.append([potion.turns, potion.e_int])
        
        if potion.e_hp != 0:
            if potion.turns == 0:
                self.hp += potion.e_hp
            else:
                self.effects_hp.append([potion.turns, potion.e_hp])
                
        
    
    def equip(self):
        """gibt monster zufalls item"""
        if self.equip_chance > 0: #wenn größer 0 garantiere "Body" rüstung
            i = Game.item_list.append(Wearable(self.x,self.y,self.z,"w", carried_by = self.number, slot = "body"))
            # i.worn = True    
            for slot in Game.slots:
                if slot == "body":
                    continue
                if random.random() < self.equip_chance:
                    Game.item_list.append(Wearable(self.x,self.y,self.z,"w", carried_by = self.number, slot = slot))
            #weapon
            Game.item_list.append(Meleeweapon(self.x,self.y,self.z,"m", carried_by = self.number))
            #self.hello()
        
        
    def move(self,hero):
        # sniffing hero?
        if self.__class__.__name__ == "Hero":
            return
        self.dx = 0
        self.dy = 0
        if self.state == "hunt":
            self.state = "patrol"
        if self.state == "patrol" and hero.z == self.z:
            dist = ((self.x-hero.x)**2+(self.y-hero.y)**2)**0.5 #**2 quadrieren / **0.5 = wurzelziehen
            if dist <= self.sniffrange:
                self.state = "hunt"
        if self.state == "hunt":
            #clever movement
            if self.x < hero.x:
                self.dx = 1
            elif self.x > hero.x:
                self.dx = -1
            if self.y < hero.y:
                self.dy = 1
            elif self.y > hero.y:
                self.dy = -1
        elif self.state == "flee":
            if self.x < hero.x:
                self.dx = -1
            elif self.x > hero.x:
                self.dx = 1
            if self.y < hero.y:
                self.dy = -1
            elif self.y > hero.y:
                self.dy = 1
        elif self.state == "patrol":           
            self.dx=random.randint(-1,1)
            self.dy=random.randint(-1,1)
            ## jump?
            if self.jumprange > 1:
                self.dx *= random.randint(1, self.jumprange)
                self.dy *= random.randint(1, self.jumprange)
        
    def hello(self, wait = True):
        print("---------------------------")
        print("str: {:.1f} dex: {:.1f} int: {:.1f} hp: {:.1f} hallo ich bin ein(e) {}".format(
               self.strength, self.dexterity, self.intelligence, self.hp,self.__class__.__name__))
        print("my equipment:")
        for i in Game.item_list:
            if i.carried_by == self.number :
                print(i.name)
        if wait:
            pri_input()
        
        
      #  for x in range(10):
    #print(int(round(random.gauss(0, 1),0)))
        
class Statue(Monster):
    def move(self,hero):
        self.dx = 0
        self.dy = 0
    
    def init3(self):
        self.equip_chance=Game.zoo[self.symbol][10]        

class Hero(Monster):
    
    def move(self,hero):
        pass
        
    def init3(self):
        self.history = []
        self.trophy = {}
        self.equip_chance=Game.zoo[self.symbol][10]
        self.equip()
        self.hp=500
        self.hpmax=1000
        self.mp=100
        self.hunger=0
        self.healthpot=0

        
class Lord(Monster):
    
    def init3(self):
        self.equip_chance=Game.zoo[self.symbol][10]
        self.equip()
            
class Ogre(Monster):
    
    def init3(self):
        self.equip_chance=Game.zoo[self.symbol][10]
        self.equip()
        
class Mage(Monster):
        
    def init3(self):
        self.equip_chance=Game.zoo[self.symbol][10]
        self.equip()
        self.jumprange = 4
        
class Ysera(Monster):
    def move(self,hero):
        self.dx = 0
        self.dy = 0
    
    def init3(self):
        self.equip_chance=Game.zoo[self.symbol][10]
        
class Bonewarrior(Monster):
    
    def init3(self):
        self.equip_chance=Game.zoo[self.symbol][10]
        self.equip()
        
        
class Goblin(Monster):
    
    def init3(self):
        self.equip_chance=Game.zoo[self.symbol][10]
        self.equip()
        self.jumprange = 2
            
        #items
        # class item/monster > code dupliziert "eltern klasse > object"
        
class Rect():
    """dungeon creator// a rectangle on the map used to charecterize a room"""
    def __init__(self, x, y, w, h):
        self.x1 = x
        self.y1 = y
        self.x2 = x + w
        self.y2 = y + h
        
    
class Game():
    
    spoils_of_war_chance= 0.15
    instakill = False  # set true for cheatmode!
    
    dungeon = [] 
    monster_list = []
    item_list = []
    #hero = None
    legend = ""
    commands = ""

    entchantment = {1:"magic",2:"rare",3:"epic",4:"legendary",5:"unique"}
    slots = ("head","neck","body","hand","legs","feet")
    zoo = {}
    wearables = {}
    meleeweapons = {}
    items = {}
    pots = {}
    
def main():
    
    

    ## --------------read monster zoo values from file -------------------------------
    with open(os.path.join("dungeons","zoo.csv")) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Game.zoo[row["Symbol"]] = [row["Name"],
                                  int(row["Roll"]),
                                  int(row["Damage"]),
                                  row["Attack"],
                                  int(row["hp"]),
                                  int(row["Strength"]),
                                  int(row["Dexterity"]),
                                  int(row["Intelligence"]),
                                  int(row["Sigma"]),
                                  int(row["Price"]),
                                  float(row["Equip_Chance"])
                                  ]
                                  
    max_price=0    # ----find highest price (wearables dropchance)
    for z in Game.zoo:
        if z == "@" or z == "R":
            continue
        price = Game.zoo[z][9]
        if price > max_price:
            max_price = price
    price_sum=0    # --- calculate relative wearables dropchance
    for z in Game.zoo:
        if z == "@" or z == "R":
            continue
        price = max_price*1.2-Game.zoo[z][9]
        price_sum += price
        Monster.drop[price_sum] = z
        Monster.prices.append(price_sum)
    Monster.price_sum = price_sum
    Monster.prices.sort()
                                  
                                  
    ## ------------------------read wearable values from file-------------------------------
    with open(os.path.join("dungeons","wearables.csv")) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Game.wearables[row["Name"]] = [row["Slot"],
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
    for w in Game.wearables:
        price = Game.wearables[w][1]
        if price > max_price:
            max_price = price
    price_sum=0    # --- calculate relative wearables dropchance
    for w in Game.wearables:
        price = max_price*1.2-Game.wearables[w][1]
        price_sum += price
        Wearable.drop[price_sum] = w
        Wearable.prices.append(price_sum)
    Wearable.price_sum = price_sum
    Wearable.prices.sort()



    ## --------------read meleeweapon values from file -------------------------------
    with open(os.path.join("dungeons","meleeweapon.csv")) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Game.meleeweapons[row["Name"]] = [
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
    for mw in Game.meleeweapons:
        price = Game.meleeweapons[mw][9]
        if price > max_price:
            max_price = price
    price_sum=0    # --- calculate relative meleedropchance
    for mw in Game.meleeweapons:
        price = max_price*1.2-Game.meleeweapons[mw][9]
        price_sum += price
        Meleeweapon.drop[price_sum] = mw
        Meleeweapon.prices.append(price_sum)
    Meleeweapon.price_sum = price_sum
    Meleeweapon.prices.sort()    
    
    
    ## --------------read potions from file -------------------------------
    with open(os.path.join("dungeons","pots.csv")) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            Game.pots[row["Name"]] = [
                                  int(row["Price"]),
                                  float(row["Weight"]),
                                  int(row["Turns"]),
                                  int(row["E_str"]),
                                  int(row["E_dex"]),
                                  int(row["E_int"]),
                                  int(row["E_hp"])
                                    ]
    max_price=0    # ----find highest price (pot droppchance)
    for p in Game.pots:
        price = Game.pots[p][0]
        if price > max_price:
            max_price = price
    price_sum=0    # --- calculate relative potdropchance
    for p in Game.pots:
        price = max_price*1.2-Game.pots[p][0]
        price_sum += price
        Pot.drop[price_sum] = p
        Pot.prices.append(price_sum)
    Pot.price_sum = price_sum
    Pot.prices.sort()    




    
    with open(os.path.join("dungeons","items.csv")) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            #print(row["Symbol"], row["Name"])
            Game.items[row["Symbol"]] = [row["Name"], float(row["Weight"]), int(row["Price"])]
            
    max_price=0    # ----find highest price (random item dropchance)
    for i in Game.items:
        price = Game.items[i][2]
        if price > max_price:
            max_price = price
    price_sum=0    # --- calculate relative random item dropchance
    for i in Game.items:
        price = max_price*1.2-Game.items[i][2]
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
                        if char in Game.items:
                            #-------------  items   -----------
                            if char == "w":
                                Game.item_list.append(Wearable(lx,ly,lz,char))
                            elif char == "m":
                                Game.item_list.append(Meleeweapon(lx,ly,lz,char))
                            elif char == "p":
                                Game.item_list.append(Pot(lx,ly,lz,char))
                            else:
                                Game.item_list.append(Item(lx,ly,lz,char))
                            line = line[:lx]+"."+line[lx+1:]
                        if char in Game.zoo:                   
                            # ----------  monster   ------------                      
                            if char == "@":
                                Game.hero= Hero(lx,ly,lz,char)
                                Game.monster_list.append(Game.hero)
                            elif char == "S":
                                Game.monster_list.append(Statue(lx,ly,lz,char))
                            elif char == "L":
                                Game.monster_list.append(Lord(lx,ly,lz,char))
                            elif char == "O":
                                Game.monster_list.append(Ogre(lx,ly,lz,char))
                            elif char == "M":
                                Game.monster_list.append(Mage(lx,ly,lz,char))
                            elif char == "Y":
                                Game.monster_list.append(Ysera(lx,ly,lz,char))
                            elif char == "B":
                                Game.monster_list.append(Bonewarrior(lx,ly,lz,char))
                            elif char == "G":
                                Game.monster_list.append(Goblin(lx,ly,lz,char))
                            line = line[:lx]+"."+line[lx+1:]
                        lx += 1
                    lines[ly] = line
                    ly+=1
                lz += 1            
                #print(lines)
                Game.dungeon.append(lines)
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




    # add 50 food
    for x in range(50):
        Game.item_list.append(Item(0,0,0,"f",carried_by=Game.hero.number)) 
    turns = 0
    victory = False
    while Game.hero.hp >0 and not victory:
        turns += 1
        
        #     --------------paint the dungeon------------------
        
        cls()
        print("food: {} gold: {} key: {} healthpot: {} inv: {}".format(
              len([i for i in Game.item_list if i.carried_by == Game.hero.number and i.name == "food"]),
              len([i for i in Game.item_list if i.carried_by == Game.hero.number and i.name == "gold"]),
              len([i for i in Game.item_list if i.carried_by == Game.hero.number and i.name == "key"]),
              len([i for i in Game.item_list if i.carried_by == Game.hero.number and i.__class__.__name__ == "Pot"]),
              len([i for i in Game.item_list if i.carried_by == Game.hero.number])))
        line_number = 0
        for line in Game.dungeon[Game.hero.z]:
            pline = line[:]
            myline = ""
            
            
            #       ------ items/monster ------
     
           
            for x in range(len(pline)):
                stash = []
                monster = False
                mychar = pline[x]
                for mymonster in Game.monster_list:
                    if mymonster.z == Game.hero.z and mymonster.y == line_number and mymonster.x == x:
                        monster = True
                        mychar=mymonster.symbol 
                if not monster:        
                    for item in Game.item_list:
                        if not item.carried_by and item.z == Game.hero.z and item.y == line_number and item.x == x:
                            stash.append(item)
                    if len(stash) == 1:
                        mychar=stash[0].symbol
                    elif len(stash) > 1:
                        mychar = "?"
                myline += mychar   
            print(myline)
            line_number += 1
        # hero stays on special tile?
        tile = Game.dungeon[Game.hero.z][Game.hero.y][Game.hero.x]
        #   items // if item.x == hero.x....
        ####  hero found items?####
        stash = []
        for item in Game.item_list:
            if Game.hero.z == item.z and not item.carried_by:
                if Game.hero.y == item.y:
                    if Game.hero.x == item.x:
                        stash.append(item)
                        
        if len(stash) > 0:
            print("you found {} item{}:".format(len(stash),"" if len(stash) == 1 else "s"))
            for i in stash:
                print(i.name)
            print("press enter to pick up all items")
            
        if tile == "1":
            print("you found a lever which opened the big door")
            #dungeon[1] = dungeon [1][:4] + "." + dungeon[1][4+1:] #x + y coordinate zum entfernen!!!
            Game.dungeon[Game.hero.z][1] = remove_tile(44,1,Game.hero.z) #entfernt türe bei x(4) y(1) siehe 1 zeile weiter oben
            Game.dungeon[Game.hero.z][Game.hero.y] = remove_tile(Game.hero.x,Game.hero.y,Game.hero.z)
        elif tile == "2":
            print("you found a lever which opened the big door in lvl one")
            Game.dungeon[0][1] = remove_tile(42,1,0)
            Game.dungeon[Game.hero.z][Game.hero.y] = remove_tile(Game.hero.x,Game.hero.y,Game.hero.z)
        elif tile =="<":
            print("you found a stair up (press Enter to climb up)")
        elif tile ==">":
            print("you found a stair down (press Enter to climb down)")
            
        # -----------food clock -------------------
        Game.hero.hp += 0.1
        Game.hero.hp = min(Game.hero.hp,Game.hero.hpmax)
        if Game.hero.hunger > 40:
                Game.hero.hp = 0
                print("you died")
                break
        elif Game.hero.hunger > 35:
                Game.hero.hp -= 10
                print("youre starving")
        elif Game.hero.hunger > 25:
                Game.hero.hp -= 5
                print("you really need something to eat!")
        elif Game.hero.hunger > 20:
            print("youre stomache growls! eat something")  
        
        # ---------- ask for new command ----------
        c = input("hp: {} ({}) mp: {} hunger: {} \nstr: {:.0f} ({}) dex: {:.0f} ({}) int: {:.0f} ({}) \ntype help or enter command:".format(
                  int(Game.hero.hp), Game.hero.effects_hp_bonus,Game.hero.mp,Game.hero.hunger,
                  Game.hero.strength, Game.hero.effects_str_bonus,
                  Game.hero.dexterity,Game.hero.effects_dex_bonus,
                  Game.hero.intelligence, Game.hero.effects_int_bonus))
        
        #-------------items-------------
        #dropped items are not instantly picked up again, only if you hit enter
        if len(stash) > 0:
            if c == "":
                for i in stash:
                    i.carried_by = Game.hero.number
                continue
        
        
        Game.hero.dx= 0
        Game.hero.dy= 0
        # -------- movement -----------
        if tile == "<":
            if c == "" or c == "<":
                if Game.hero.z == 0:
                    pri_input("you leave the dungeon and return to town")
                    break
                Game.hero.z -= 1  # climb up
                Game.hero.hunger += 2
        elif tile == ">":
            if c == "" or c == ">":
                if Game.hero.z == len(Game.dungeon)-1:
                    pri_input("you already reached the deepest dungeon")
                else:
                    Game.hero.z += 1    # climb down
                    Game.hero.hunger += 2
        if c == "a":   
            Game.hero.dx = -1                # left
        elif c == "d":
            Game.hero.dx = 1                # right
        elif c == "w":
            Game.hero.dy = -1                # up
        elif c == "s":
            Game.hero.dy = 1                # down
        if Game.hero.dx != 0 or Game.hero.dy != 0:
            Game.hero.hunger+=0.5
        #---------------- other commands (non- movement) -------------
        if c == "quit" or c == "exit":
            break
            
            
            
        # ------------------inventory----------------------
        
        
        elif c == "i" or c == "inventory":
            cls()
            rucksack = {}
            for item in Game.item_list:
                if item.carried_by == Game.hero.number:
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
                for item in Game.item_list:
                    if item.symbol == "w" and item.carried_by == Game.hero.number:
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
                    for item in Game.item_list:
                        if item.__class__.__name__ == "Wearable":
                            if item.number == w and item.carried_by == Game.hero.number:
                                if item.worn:
                                    item.worn = False
                                else:
                                    item.worn = True
                                    slot = item.slot
                    if slot:   #remove wearable
                        for item in Game.item_list:
                            if item.__class__.__name__ == "Wearable":
                                if item.number != w and item.carried_by == Game.hero.number and item.slot == slot:
                                    item.worn = False
                    print("you have changed your equipment!")
                ### weaponscreen####
            m = 1
            while m != 0:
                    
                print("-----------------------------\ndetailed list of meleeweapon\n-----------------------------")
                for item in Game.item_list:
                    if item.symbol == "m" and item.carried_by == Game.hero.number:
                        print(" {} ra: {} q: {:3.1f}% ({}) ({}) {} {} {}".format(
                              item.number,item.meleerange, item.quality*100, "equiped" if item.equiped else "pack","2h" if item.twohand else "1h",item.name, 
                              "" if item.boni == 0 else "\n                    boni: att {} def {} str {} dex {} int {}".format(
                              item.attackbonus,item.defensebonus,item.strengthbonus,item.dexteritybonus,item.intelligencebonus),
                              "" if Game.hero.strength >= item.min_str and Game.hero.dexterity >= item.min_dex and Game.hero.intelligence >= item.min_int else
                              "\n                    malus: (hero not qualified) min_str {} str {} min_dex {} dex {} min_int {} int {}".format(
                               item.min_str, Game.hero.strength,item.min_dex,Game.hero.dexterity,item.min_int,Game.hero.intelligence)))
                m = input("enter number of item to wield/unwield or press enter to continue")
                cls()
                try:
                    m = int(m)
                except:
                    m = 0
                if m > 0:
                    for item in Game.item_list:
                        if item.__class__.__name__ == "Meleeweapon":
                            if item.number == m and item.carried_by == Game.hero.number:
                                if item.equiped:
                                    item.equiped = False
                                    if item.twohand:
                                        Game.hero.free_slots += 2
                                    else:
                                        Game.hero.free_slots += 1                            
                                else:
                                    if Game.hero.free_slots < 1:
                                        print("you have no free weaponslot left! please unequip weapon(s) first")
                                    elif Game.hero.free_slots < 2 and item.twohand:
                                        print("remove both weapon(s) first to equip a 2h weapon")
                                    else:
                                        item.equiped = True 
                                        if item.twohand:
                                            Game.hero.free_slots -= 2
                                        else:
                                            Game.hero.free_slots -= 1    
                                            
            ### potionscreen####
            p = 1
            while p != 0:
                    
                print("-----------------------------\ndetailed list of potions\n-----------------------------")
                for item in Game.item_list:
                    if item.symbol == "p" and item.carried_by == Game.hero.number:
                        print(" {} {}".format(item.number,item.name))
                p = input("enter number of potion to drink or press enter to continue")
                cls()
                try:
                    p = int(p)
                except:
                    p = 0
                if p > 0:
                    for item in Game.item_list:
                        if item.__class__.__name__ == "Pot":
                            if item.number == p and item.carried_by == Game.hero.number:
                                print("you feel the power of the potion")
                                Game.hero.drink(item)
                                Game.item_list = [i for i in Game.item_list if i.number != p] #remove item from item_list
                                
            
        elif c == "x" or c == "drop":
            rucksack = {}
            for item in Game.item_list:
                if item.carried_by == Game.hero.number:
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
                    for item in Game.item_list:
                        if item.name == what and item.carried_by == Game.hero.number:
                            item.carried_by = False 
                            item.x,item.y,item.z = Game.hero.x,Game.hero.y,Game.hero.z
                            print("dropped 1 {}".format(item.name))
                            break
                pri_input()
                            
                        
                    
        elif c == "help" or c == "?":
            pri_input(legend)
            pri_input(commands)

        elif c == "e" or c == "eat":
            
            #if hero.food <= 0:
            if  len([i for i in Game.item_list if i.carried_by == Game.hero.number and i.name == "food"]) <= 0:
                
                pri_input("you have no food!")
            else: 
                #hero.food -= 1
                n=-1
                for i in Game.item_list:
                    if i.carried_by == Game.hero.number and i.name == "food":
                        n= i.number
                        break
                Game.item_list = [i for i in Game.item_list if i.number != n] #remove item from item_list
                Game.hero.hunger -= 5
                Game.hero.hunger = max(0,Game.hero.hunger) 
                
        elif c == "t" or c == "teleport":
            Game.hero.hunger += 20
            Game.hero.x,Game.hero.y,Game.hero.z = teleport(Game.hero.z)
            
        elif (c == "esc" or c == "escape") and Game.hero.z >0:  
            Game.hero.hunger += 15
            Game.hero.hp = 1
            Game.hero.x,Game.hero.y,Game.hero.z = teleport(Game.hero.z-1)   
            
        elif c == "c" or c == "check" or c == "sniff":
            # check stats of monsters nearby
            for dy in [-1,0,1]:
                for dx in [-1,0,1]:
                    for mymonster in Game.monster_list:
                        if mymonster.z == Game.hero.z and mymonster.x == Game.hero.x+dx and mymonster.y == Game.hero.y+dy:
                            mymonster.hello(wait = False)
            pri_input()
            
        #--------- potion effects ---------------------------
        for mymonster in Game.monster_list:
            mymonster.stat_effects_tick()
        # kill monsters without hitpoints
        #  remove monster from monsterlist
        if Game.hero.hp + Game.hero.effects_hp_bonus < 0:
            print("you die due to negative hitpoints")
            pri_input()
        Game.monster_list = [m for m in Game.monster_list if (m.hp + m.effects_hp_bonus) > 0]
                
                

        # -------- check if movement is possible -------------
        tile = Game.dungeon[Game.hero.z][Game.hero.y+Game.hero.dy][Game.hero.x+Game.hero.dx]
        if tile == "#":   # hero runs into wall
            pri_input("you run into a wall, ouch!")
            Game.hero.hp -= 1
            Game.hero.dx=0
            Game.hero.dy=0
        if tile == "D":   # hero runs into door
            pri_input("a big door find a way to open it")
            Game.hero.dx=0
            Game.hero.dy=0
        if tile == "d":
            #        hero has at least 1 key?
            if len([i for i in Game.item_list if i.carried_by == Game.hero.number and i.name == "key"]) > 0:
                n=-1
                for i in Game.item_list:
                    if i.carried_by == Game.hero.number and i.name == "key":
                        n= i.number
                        break
                Game.item_list = [i for i in Game.item_list if i.number != n]
                Game.dungeon[Game.hero.z][Game.hero.y+Game.hero.dy] = remove_tile(Game.hero.x+Game.hero.dx,Game.hero.y+Game.hero.dy,Game.hero.z)
            else:
                pri_input("a small door find a key to open it")
                Game.hero.dx=0
                Game.hero.dy=0

            
        
        
        
        
        # ----------- monster movement-----------------
        
        occupied = []
        for mymonster in Game.monster_list:
            if mymonster.z == Game.hero.z:
                occupied.append((mymonster.x,mymonster.y))
        
        for mymonster in Game.monster_list:
            if mymonster.number == Game.hero.number:
                continue
            if mymonster.z == Game.hero.z:
                mymonster.move(Game.hero)  # makes new dx/dy for monster, monsters are hunting player
                # mage shall not jump out of dungeon
                width = len(Game.dungeon[Game.hero.z][0])
                height = len(Game.dungeon[Game.hero.z])
                if mymonster.x+mymonster.dx < 0 or mymonster.x+mymonster.dx >= width:
                    mymonster.dx = 0
                if mymonster.y+mymonster.dy < 0 or mymonster.y+mymonster.dy >= height:
                    mymonster.dy = 0    
                # where does the monster want to go to?    
                tile = Game.dungeon[mymonster.z][mymonster.y+mymonster.dy][mymonster.x+mymonster.dx]
                # doors and walls are forbidden
                if tile == "#" or tile == "D" or tile == "d": 
                    mymonster.dx=0
                    mymonster.dy=0
                elif mymonster.x+mymonster.dx == Game.hero.x:
                    if mymonster.y+mymonster.dy == Game.hero.y:
                        fight(mymonster,Game.hero)
                        fight(Game.hero,mymonster)
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
        
        for mymonster in Game.monster_list:
            if mymonster.number == Game.hero.number:
                # hero himself
                continue # proceed to next monster in monster_list
            if mymonster.z == Game.hero.z:
                if mymonster.y == Game.hero.y+Game.hero.dy:
                    if mymonster.x == Game.hero.x+Game.hero.dx:
                        Game.hero.dx = 0
                        Game.hero.dy = 0
                        fight(Game.hero,mymonster) #fight
                        fight(mymonster,Game.hero)
                        if mymonster.hp <1:
                            # monster down , drop?
                            # special drop
                            if mymonster.__class__.__name__ == "Ysera":
                                #remove door when dragon slain @level 5
                                Game.dungeon[4][9] = remove_tile(40,9,4)
                            if mymonster.__class__.__name__ == "Lord":
                                print("you have slain the dark lord and completed the quest")
                                victory = True                          
                            droppings = False
                            if random.random() <0.25:
                                Game.item_list.append(Item(mymonster.x,mymonster.y,mymonster.z,random.choice(("$","f","p","k"))))
                                print("the monster dropped something!")
                                droppings = True
                            for i in Game.item_list:
                                if i.carried_by == mymonster.number:
                                    if random.random() < Game.spoils_of_war_chance:
                                        droppings = True
                                        print("spoils of war: ", i.name)
                                        i.carried_by = False
                                        i.x = mymonster.x
                                        i.y = mymonster.y
                                        i.z = mymonster.z
                            if droppings:
                                pri_input()
                            Game.hero.history.append("turn {}: slain a {}".format(turns,mymonster.__class__.__name__))
                            m = mymonster.__class__.__name__
                            if m in Game.hero.trophy:
                                Game.hero.trophy[m] += 1
                            else:
                                Game.hero.trophy[m] = 1
                        
                        input("press enter to continue")
                        
        #  remove monster from monsterlist
        Game.monster_list = [m for m in Game.monster_list if m.hp > 0]
         

        
        # movement
        Game.hero.x += Game.hero.dx
        Game.hero.y += Game.hero.dy


            
            
    print("game over")

    print("history of hero:")
    input("press enter to continue")
    for m in Game.hero.trophy:
        print(m,Game.hero.trophy[m])
    for line in Game.hero.history:
        print(line)


if __name__ == "__main__":
    main()
