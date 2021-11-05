from random import choice
import os

group  = {
    "A":['A'+str(i) for i in range(20)],
    "B":['B'+str(i) for i in range(20)],
    "C":['C'+str(i) for i in range(20)],
    "D":['D'+str(i) for i in range(20)],
    "E":['E'+str(i) for i in range(20)],
}

area = {
    "first":[],
    "second":[]
}

grouptags = [i for i in group.keys()]
areatags = [i for i in area.keys()]

def divide():
    info["count"] -= 1
    info["now"] += 1
    for i in grouptags:
        if(len(group[i]) == 0):
            grouptags.remove(i)
    for j in areatags:
        if(len(area[j])>=info["areamax"]):
            areatags.remove(j)
    area[choice(areatags)].append(group[choice(grouptags)].pop(0))

if __name__ == '__main__':

    info = {
        "count": 100,
        "now": 0,
        "max": 120,
        "areamax": 50,
    }

    while(info["count"]>=1 and info["now"]<info["max"]):
        divide()
    print(area)
    os.system('pause')

