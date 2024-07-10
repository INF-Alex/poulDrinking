import copy
import random

RED = 1
GREY = 2
YELLOW = 3
PURPLE = 4
PINK = 5
ORANGE = 6
LIGHT_GREEN = 7
DARK_GREEN = 8
LIGHT_BLUE = 9
DARK_BLUE = 10
LIGHT_BROWN = 11
DARK_BRONW = 12

Bottle_start = [[],
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
              [9,10,11,12]]

def cnt(Bottle, x):
    l = len(Bottle[x])
    assert l <= 4
    if l == 0:        return 0
    num_x = 1
    for i in range(l-1, 0, -1):
        if Bottle[x][i] == Bottle[x][i-1]:
            num_x += 1
    return num_x

assert cnt([[]],0) == 0
assert cnt([[1]],0) == 1
assert cnt([[1,1]],0) == 2

def valid(Bottle, x, y):
    num_x = cnt(Bottle, x)
    num_y = len(Bottle[y])

    if num_x == 0:
        return False, num_x, num_y 

    if num_y == 0:
        return num_x != len(Bottle[x]), num_x, num_y 
    
    return  Bottle[x][-1] == Bottle[y][-1], num_x, num_y 

def check(bottle):
    for item in bottle:
        if len(item) == 0:
            continue
        elif len(item) < 4:
            return False
        else:
            x = item[0]
            for y in item[1:]:
                if x != y:
                    return False
    return True

# x to y
def poul(B, x, y, num_x, num_y):
    Bottle = copy.deepcopy(B)
    if num_x > 4-num_y:
        num_x = 4-num_y
    Bottle[y] = Bottle[y] + [Bottle[x][-1]] * num_x
    Bottle[x] = Bottle[x][:len(Bottle[x])-num_x]

    return Bottle

def op(Bottle):
    global Situations
    if Bottle in Situations:
        return False
    Situations.append(Bottle)
    if check(Bottle):
        with open('v2.txt','a') as f:
            f.write(str(Bottle))
            f.write('\n')
        return True
    for i in range(14):
        for j in range(14):
            if i == j:
                continue
            flag, num_x, num_y = valid(Bottle, i, j)
            if flag:
                B = poul(Bottle, i, j, num_x, num_y)
                if op(B):
                    with open('v2.txt','a') as f:
                        f.write(str(Bottle))
                        f.write('\n')
                    return True
    return False

Situations = list()

with open('v2.txt','w') as f:
    f.write('')

if not op(Bottle_start):
    print(r"can't get!")