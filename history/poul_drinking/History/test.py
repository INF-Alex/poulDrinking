import copy
import random

RED = 1
GREY = 2
YELLOW = 3
PURPLE = 4
PINK = 5
LIGHT_GREEN = 7
DARK_GREEN = 8
LIGHT_BLUE = 8
DARK_BLUE = 9
ORANGE = 10
LIGHT_BROWN = 11
DARK_BRONW = 12

Bottle_prime = [[x,x,x,x] for x in range(1,13)] + [[],[]]# 初始状态
Bottle_end = [[],
              [],
              [1,2,3,4],
              [1,2,3,4],
              [1,2,3,4],
              [1,2,3,4],
              [5,6,7,8],
              [5,6,7,8],
              [5,6,7,8],
              [5,6,7,8],
              [9,10,11,12],
              [9,10,11,12],
              [9,10,11,12],
              [9,10,11,12]]   # 终态

Mem = []

def poul(B, x, y):
    Bottle = copy.deepcopy(B)
    if ((len(Bottle[x]) == 1 or len(Bottle[x]) > 1 and Bottle[x][-1] == Bottle[x][-2])) and len(Bottle[y]) < 4:
        item = Bottle[x].pop()
        Bottle[y].append(item)
    return Bottle

def change(B,x,y):
    Bottle = copy.deepcopy(B)
    Bottle[x], Bottle[y] = Bottle[y], Bottle[x]
    return Bottle

def fv(Bottle):
    global Bottle_end
    num = 0
    for b in range(13):
        j = min(len(Bottle[b]), len(Bottle_end[b]))
        for i in range(j):
            if Bottle_end[b][i] == Bottle[b][i]:
                num += 1
    return num

def op(Bottle):
    if Bottle == Bottle_end:
        with open(r"test.txt",'a') as f:
            f.write('\n')
            f.write(Bottle)
        print('True')
        return True
    for i in range(13):
        for j in range(13):
            if i != j:
                if fv(poul(Bottle, i, j)) > fv(Bottle):
                # if poul(Bottle,i,j) not in Mem:
                    Mem.append(poul(Bottle,i,j))
                    # print('1a',i,j)
                    if op(poul(Bottle, i, j)):
                        with open(r"test.txt",'a') as f:
                            f.write('\n')
                            f.write(Bottle)
                        return True
                if fv(change(Bottle, i, j)) > fv(Bottle):
                # if change(Bottle,i,j) not in Mem:
                    Mem.append(change(Bottle,i,j))
                    # print('2b',i,j)
                    if op(change(Bottle, i, j)):
                        with open(r"C:\Users\86180\Desktop\test.txt",'a') as f:
                            f.write('\n')
                            f.write(Bottle)
                        return True

op(Bottle_prime)
