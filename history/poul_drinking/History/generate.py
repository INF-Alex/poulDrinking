import random
import json
import copy

BOTTLE_NUM = 14
Bottle_start = [[x,x,x,x] for x in range(1,BOTTLE_NUM-1)] + [[],[]]
# Bottle_start = [[1, 10, 1, 6], [9, 8, 4, 3], [9, 4, 12, 11], [10, 2, 4, 2], [11, 2, 7, 8], [12, 7, 9, 2], [5, 6, 4, 5], [8, 3, 6, 7], [12, 10, 12, 1], [5, 5, 3, 11], [1, 8, 10, 11], [3, 7, 6, 9], [], []]
LEVEL = 1
MUL = 1000

def cnt(Bottle, x):
    l = len(Bottle[x])
    assert l <= 4
    if l == 0:        return 0
    num_x = 1
    for i in range(l-1, 0, -1):
        if Bottle[x][i] == Bottle[x][i-1]:
            num_x += 1
    return num_x

def cnt(Bottle, x):
    l = len(Bottle[x])
    assert l <= 4
    if l == 0:        return 0
    num_x = 1
    for i in range(l-1, 0, -1):
        if Bottle[x][i] == Bottle[x][i-1]:
            num_x += 1
    return num_x

def r_pour(Bottle, x, y, num_x):
    if num_x != 1:
        num_x = random.randint(1, num_x-1)
    Bottle[y] += Bottle[x][-num_x:]
    Bottle[x] = Bottle[x][:len(Bottle[x])-num_x]
    return Bottle

# reversed path: x to y
def poul(Bottle, x, y):
    num_x = cnt(Bottle, x)
    num_y = cnt(Bottle, y)
    l_x = len(Bottle[x])
    l_y = len(Bottle[y])
    if num_x == 0 or l_y == 4:
        return Bottle
    if num_y == 0:
        if num_x == 1:
            return Bottle
        else:
            return r_pour(Bottle, x, y, num_x)
    if l_x == 4:
        if num_x == 1:
            return Bottle
        else:
            num_x = min(num_x, 4-l_y)
            return r_pour(Bottle, x, y, num_x)
    if Bottle[x][-1] == Bottle[y][-1]:
        return Bottle
    num_x = min(num_x, 4-l_y)
    return r_pour(Bottle, x, y, num_x)

def cnt_empty(Bottle):
    num = 0
    for i in Bottle:
        if len(i) == 0:
            num += 1
        if num == 2:
            return True
    return False

Bottle = Bottle_start
for _ in range(LEVEL*MUL):
    x = random.randint(0,BOTTLE_NUM-1)
    y = random.randint(0,BOTTLE_NUM-1)
    while x == y:
        y = random.randint(0,BOTTLE_NUM-1)
    Bottle = poul(Bottle, x, y)

# while True:
#     x = random.randint(0,13)
#     y = random.randint(0,13)
#     Bottle = poul(Bottle, x, y)

# num = [[0,0,0,0] for _ in range(12)]
# Bottle = [[0,0,0,0] for x in range(12)]
# for i in range(12):
#     for j in range(4):
#         while True:
#         x = random.randint(0,11)
#         y = random.randint(0,3)
#         Bottle

# Bottle = [[1, 10, 1, 6], [9, 8, 4, 3], [9, 4, 12, 11], [10, 2, 4, 2], [11, 2, 7, 8], [12, 7, 9, 2], [5, 6, 4, 5], [8, 3, 6, 7], [12, 10, 12, 1], [5, 5, 3, 11], [1, 8, 10, 11], [3, 7, 6, 9], [], []]
with open(r"generate.txt", "w") as f:
    f.write(str(Bottle))