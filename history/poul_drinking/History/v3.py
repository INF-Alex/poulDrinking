import copy
import time
t_start = time.time()

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

BOTTLE_NUM = 14
  

# Bottle_start = [[],[],
#                 [PURPLE,DARK_BLUE,LIGHT_BLUE,GREY],
#                 [RED,DARK_GREEN,LIGHT_BROWN,ORANGE],
#                 [LIGHT_BROWN,ORANGE,YELLOW,LIGHT_BLUE],
#                 [PURPLE,YELLOW,LIGHT_BLUE,PURPLE],
#                 [DARK_GREEN,DARK_GREEN,PINK,RED],
#                 [RED,DARK_BRONW,DARK_BLUE,PINK],
#                 [PINK,GREY,PINK,DARK_BRONW],
#                 [GREY,DARK_BLUE,LIGHT_BLUE,LIGHT_GREEN],
#                 [LIGHT_GREEN,DARK_BLUE,YELLOW,LIGHT_GREEN],
#                 [RED,PURPLE,DARK_BRONW,LIGHT_BROWN],
#                 [LIGHT_GREEN,YELLOW,DARK_GREEN,ORANGE],
#                 [ORANGE,LIGHT_BROWN,DARK_BRONW,GREY]]



with open('generate.txt','r') as f:
    Bottle_start = eval(f.read())


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

def change(B, x, y):
    Bottle = copy.deepcopy(B)
    Bottle[x],Bottle[y] = Bottle[y], Bottle[x]
    return Bottle

def op(Bottle):
    global Situations
    global path
    if len(Situations) % 1000 == 0:
        print(len(Situations))
    if check(Bottle):
        return True
    for i in range(14):
        for j in range(14):
            if i == j:
                continue
            flag, num_x, num_y = valid(Bottle, i, j)
            if flag:
                B = poul(Bottle, i, j, num_x, num_y)
                if not B in Situations and op(B):
                    Situations.append(Bottle)
                    path.append(f"{i} → {j}")
                    return True
            B = change(Bottle, i, j)
            if not B in Situations and op(B):
                Situations.append(Bottle)
                path.append(f"{i} ⬅→ {j}")
                return True
    return False

Situations = list()
path = list()

if not op(Bottle_start):
    print(r"can't get!")

with open('v3.txt','w') as f:
    for i in path[::-1]:
        f.write(f"{i}")
        f.write('\n')

print('------v3------')
print('总步数：',len(path))
print(f'操作用时：{time.time() - t_start:.3f}',)
print('--------------')
