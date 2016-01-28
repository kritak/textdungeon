
import random



def fight(i1,i2):
    """fighting between two class instances i1 is attacking i2"""
    if i1.hp <1 or i2.hp <1:
        return
    print("{} fights {}".format(i1.name,i2.name))
    i1weapons = []
    i1armor = []
    i2weapons = []
    i2armor = []
    #i1weapon equipped?
    for item in Game.item_list:
        if item.carried_by == i1.number:
            if item.__class__.__name__ == "Meleeweapon":
                if item.equiped:
                    i1weapons.append(item)
            if item.__class__.__name__ == "Wearable":
                if item.worn:
                    i1armor.append(item)
        if item.carried_by == i2.number:
            if item.__class__.__name__ == "Meleeweapon":
                if item.equiped:
                    i2weapons.append(item)
            if item.__class__.__name__ == "Wearable":
                if item.worn:
                    i2armor.append(item)
    #weaponrange
    i1weaponrange = 0
    i2weaponrange = 0
    
    for w in i1weapons:
        if w.meleerange > i1weaponrange:
            i1weaponrange = w.meleerange
    for w in i2weapons:
        if w.meleerange > i2weaponrange:
            i2weaponrange = w.meleerange
            
            
    #all resistence set to 0
    #random.choose slot to hit
    #iterate over armor (defender)
    #check if hit slot has armor(resistence)
    

        
                     
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
    #------------------parry chance for defender-----------------
    if i2weaponrange > i1weaponrange:
        if random.random()<Game.parrychance:
            print("defending {} succesfully parried with his longer weapon".format(i2.name))
            return
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
