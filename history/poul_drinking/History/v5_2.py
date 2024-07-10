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

# with open('generate.txt','r') as f:
#     Bottle_start = eval(f.read())

Bottle_start = [[],[],
                [RED,DARK_BRONW,DARK_BLUE,LIGHT_GREEN],
                [LIGHT_BROWN,DARK_BRONW,LIGHT_BLUE,YELLOW],
                [YELLOW,GREY,PURPLE,RED],
                [GREY,ORANGE,PURPLE,LIGHT_BROWN],
                [DARK_GREEN,PURPLE,DARK_GREEN,LIGHT_GREEN],
                [RED,LIGHT_BROWN,DARK_BLUE,LIGHT_BLUE],
                [DARK_GREEN,LIGHT_BROWN,GREY,DARK_BRONW],
                [ORANGE,ORANGE,YELLOW,PINK],
                [DARK_BLUE,DARK_BLUE,ORANGE,LIGHT_BLUE],
                [PINK,PINK,PINK,DARK_GREEN],
                [DARK_BRONW,YELLOW,LIGHT_GREEN,LIGHT_GREEN],
                [GREY,LIGHT_BLUE,RED,PURPLE]]

Bottle_start = [[],[],[1, 12, 10, 7], [11, 12, 9, 3], [3, 2, 4, 1], [2, 6, 4, 11], [8, 4, 8, 7], [1, 11, 10, 9], [8, 11, 2, 12], [6, 6, 3, 5], [10, 10, 6, 9], [5, 5, 5, 8], [12, 3,7,7], [2, 9, 1, 4]]

Bottle_start = [[],[],
                [DARK_GREEN,DARK_GREEN,LIGHT_BROWN,DARK_BRONW],
                [DARK_GREEN,PURPLE,ORANGE,LIGHT_GREEN],
                [DARK_GREEN,RED,DARK_BLUE,PURPLE],
                [LIGHT_BROWN,YELLOW,GREY,PINK],
                [ORANGE,PINK,YELLOW,LIGHT_BROWN],
                [LIGHT_GREEN,LIGHT_GREEN,LIGHT_BLUE,DARK_BRONW],
                [GREY,DARK_BRONW,LIGHT_BROWN,YELLOW],
                [YELLOW,ORANGE,RED,DARK_BLUE],
                [ORANGE,PINK,GREY,DARK_BLUE],
                [RED,GREY,PURPLE,LIGHT_BLUE],
                [LIGHT_BLUE,DARK_BLUE,PINK,DARK_BRONW],
                [LIGHT_GREEN,PURPLE,RED,LIGHT_BLUE]]

# Bottle_start = [[12,12,12], [9,9,9], [8, 8, 11], [8, 4, 6, 7], [8, 1, 10, 4], [11, 3, 2, 5], [6, 5, 3, 11], [7, 7], [2, 12, 11, 3], [3, 6, 1, 10], [6, 5, 2, 10], [1, 2, 4], [9, 10, 5], [7, 4, 1]]



def cnt(Bottle, x):
    l = len(Bottle[x])
    assert l <= 4
    if l == 0:        return 0
    num_x = 1
    for i in range(l-1, 0, -1):
        if Bottle[x][i] == Bottle[x][i-1]:
            num_x += 1
        else:
            break
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
    if check(Bottle):
        return True
    for i in range(BOTTLE_NUM):
        for j in range(BOTTLE_NUM):
            if i == j:
                continue
            flag, num_x, l_y = valid(Bottle, i, j)
            if flag:
                B = poul(Bottle, i, j, num_x, l_y)
                if op(B):
                    global path
                    path.append(f"{i+1} → {j+1}")
                    return True
    return False

Situations = list()
path = list()


assert(Bottle_start[0] == [])
assert(Bottle_start[1] == [])
pre_path = list()
for turn in range(2):
    m = 0
    mc = RED
    for c in range(1,BOTTLE_NUM-1):
        t = 0
        for x in range(2,BOTTLE_NUM):
            if Bottle_start[x][-1] == c:
                t += cnt(Bottle_start,x)
        assert t <= 4
        if t > m:
            m = t
            mc = c
    for i in range(2,BOTTLE_NUM):
        if Bottle_start[i][-1] == mc:
            n = cnt(Bottle_start, i)
            for _ in range(n):
                Bottle_start[i].pop()
    Bottle_start[turn] = [mc for _ in range(m)]
if not op(Bottle_start):
    print(r"can't get!")

with open('v5.txt','w') as f:
    for i in path[::-1]:
        f.write(f"{i}\n")


print('------v5_2----')
print('总步数：',len(path))
print(f'操作用时：{time.time() - t_start:.3f}',)
print('--------------')