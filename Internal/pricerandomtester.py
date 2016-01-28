"""testing random frequency of items based on price for item.
   a cheap item is more common, a expensive item is very rare"""

import random

d = {"healing":50, 
     "berserk":60,
     "clever":100,
     "swiftness":100,
     "might":100,
     "awesomeness":500,
     }
     
# reverse d

dr = [[1/b,a] for [a,b] in d.items()] # list of [price, drinkname]
dr.sort()                           # sort this list by price
pricelist1 = [a for [a,b] in dr]    # list of price only
drinklist = [b for [a,b] in dr]     # list of drinkname only
pricelist2 = []                     # list of added up prices
kprice = 0
for p in pricelist1:
    kprice += p
    pricelist2.append(kprice)
    

print(pricelist1, pricelist2)

result = {}

for x in range(10000):
    
    
    y = random.random()*(pricelist2[-1]) # 1 to maxprice
    for p in pricelist2:
        if y < p:
            drinkname = drinklist[pricelist2.index(p)]
            if drinkname in result:
                result[drinkname] += 1
            else:
                result[drinkname] = 1
            break
print(result)
