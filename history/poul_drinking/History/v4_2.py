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




def Input(BOTTLE_NUM):
    Bottle = [[],[]]
    for x in range(BOTTLE_NUM-2):
        Bottle.append([0,0,0,0])
    for i in range(1,BOTTLE_NUM-1):
        s = input()         # 输入以1为基数
        x = int(s[0]) + 1   # 偏移两个
        y = int(s[2]) - 1
        while Bottle[x][y] != 0:
            s = input()         
            x = int(s[0]) + 1   
            y = int(s[2]) - 1
        Bottle[x][y] = i
    return Bottle

with open('generate.txt','r') as f:
    Bottle_start = eval(f.read())

# Bottle_start = [[], [], [4, 10, 9, 2], [1, 8, 11, 6], [11, 6, 3, 9], [4, 3, 9, 4], [8, 8, 5, 1], [1, 12, 10, 5], [5, 2, 5, 12], [2, 10, 9, 7], [7, 10, 3, 7], [1, 4, 12, 11], [7, 3, 8, 6], [6, 11, 12, 2]]

# Bottle_start = Input(BOTTLE_NUM)

Bottle_start = [[1, 10, 1, 6], [9, 8, 4, 3], [9, 4, 12, 11], [10, 2, 4, 2], [11, 2, 7, 8], [12, 7, 9, 2], [5, 6, 4, 5], [8, 3, 6, 7], [12, 10, 12, 1], [5, 5, 3, 11], [1, 8, 10, 11], [3, 7, 6, 9], [], []]

# Bottle_start = [[],[],
#                 [YELLOW,ORANGE,YELLOW,YELLOW],
#                 [LIGHT_BROWN,LIGHT_BROWN,ORANGE,ORANGE],
#                 [PURPLE,DARK_BLUE,ORANGE,LIGHT_GREEN],
#                 [YELLOW,LIGHT_BROWN,DARK_GREEN,LIGHT_GREEN],
#                 [PURPLE,RED,LIGHT_BROWN,LIGHT_BLUE],
#                 [DARK_GREEN,DARK_BLUE,DARK_BLUE,DARK_BLUE],
#                 [LIGHT_GREEN,RED,RED,LIGHT_BLUE],
#                 [LIGHT_BLUE,DARK_GREEN,PURPLE,DARK_GREEN],
#                 [LIGHT_BLUE,PURPLE,RED,LIGHT_GREEN]]

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
    l_y = len(Bottle[y])

    if num_x == 0:
        return False, num_x, l_y 
    if l_y == 0:
        return num_x != len(Bottle[x]), num_x, l_y 
    
    return  Bottle[x][-1] == Bottle[y][-1], num_x, l_y 

def check(bottle):
    # return bottle == [[1, 10, 1, 6], [9, 8, 4, 3], [9, 4, 12, 11], [10, 2, 4, 2], [11, 2, 7, 8], [12, 7, 9, 2], [5, 6, 4, 5], [8, 3, 6, 7], [12, 10, 12, 1], [5, 5, 3, 11], [1, 8, 10, 11], [3, 7, 6, 9], [], []]
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

def f_value(bottle):
    bottle = bottle[0]
    v = 0
    for item in bottle:
        if len(item) == 0:
            v += 1
        elif len(item) < 4:
            t = 0.5
            x = item[0]
            for y in item[1:]:
                if x != y:
                    t = 0
                    break
            v += t
        else:
            t = 1
            x = item[0]
            for y in item[1:]:
                if x != y:
                    t = 0
                    break
            v += t
    return v

# x to y
def poul(B, x, y, num_x, l_y):
    Bottle = copy.deepcopy(B)
    if num_x > 4-l_y:
        num_x = 4-l_y
    Bottle[y] = Bottle[y] + [Bottle[x][-1]] * num_x
    Bottle[x] = Bottle[x][:len(Bottle[x])-num_x]

    return Bottle

def op(Bottle):
    global Situations
    if Bottle in Situations:
        return False
    Situations.append(Bottle)
    if len(Situations) % 10000 == 0:
        print(len(Situations))
    if check(Bottle):
        return True
    all_B = list()
    for i in range(BOTTLE_NUM):
        for j in range(BOTTLE_NUM):
            if i == j:
                continue
            flag, num_x, l_y = valid(Bottle, i, j)
            if flag:
                B = poul(Bottle, i, j, num_x, l_y)
                all_B.append([B,i,j])
    all_B = sorted(all_B, key=f_value, reverse=True)
    for B,i,j in all_B:
        if op(B):
            global path
            path.append(f"{i} → {j}")
            return True
    return False

Situations = list()
path = list()

if not op(Bottle_start):
    print(r"can't get!")

with open('v4_2.txt','w') as f:
    for i in path[::-1]:
        f.write(f"{i}\n")


print('------v4.2------')
print('总步数：',len(path))
print(f'操作用时：{time.time() - t_start:.3f}',)
print('----------------')