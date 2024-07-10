import copy
import time
import sys
# from picture_read import p_read

from PIL import Image 
import numpy as np
from math import floor
from collections import Counter


def p_read(p_dir="./p1.jpg",x=7,y=7):
    # ROW = 2
    COLS = [x, y]
    BOTTLE_COLOR = np.array([199,197,202])
    image = Image.open(p_dir) # 用PIL中的Image.open打开图像
    image_arr = np.array(image) # 转化成numpy数组
    HEIGHT, WIDTH = image_arr.shape[:2]

    mul = HEIGHT/2556
    eps = 20
    def color_cmp(c1,c2,eps=20):
        for x in range(3):
            if eps < abs(c1[x] - c2[x]) < 256-eps:
                return False
        return True
    BOTTLE = list()
    COLORS = list()
    OFFSET = [25,0]
    pr = [[1100,1000,900,800], [1730,1630,1530,1430]]
    pr = [list(map(lambda x:floor((x+OFFSET[0])*mul),pr[0])) , list(map(lambda x:floor((x+OFFSET[0])*mul),pr[1]))]
    # print(pr)
    SS = 0


    for ci,COL in enumerate(COLS):
        MARGIN = 0
        for c in range(WIDTH):
            if color_cmp(image_arr[pr[ci][0]][c], BOTTLE_COLOR):
                MARGIN = c+1
                break
        

        unit_width = (WIDTH-MARGIN) // COL
        MARGIN += unit_width // 2
        for r in pr[ci]:
            for j in range(COL):
                c = image_arr[r][MARGIN+j*unit_width+floor(OFFSET[1]*mul)]
                SS += 1
                # print(SS,r,MARGIN+j*unit_width+floor(OFFSET[1]*mul))
                for i,t in enumerate(COLORS):
                    if color_cmp(c,t):
                        BOTTLE.append(i+1)
                        break
                else:
                    COLORS.append(c)
                    BOTTLE.append(len(COLORS))
        MARGIN -= unit_width // 2
    # from collections import Counter
    # print(Counter(BOTTLE))
    if len(COLORS) != sum(COLS) - 1:
        return False

    # print(BOTTLE)
    import copy
    b = copy.deepcopy(BOTTLE)
    BOTTLE = []
    b2 = [[] for _ in range(COLS[0])]
    j = 0
    for i in b[:4*(COLS[0])]:
        b2[j].append(i)
        j = (j+1)%(COLS[0])
    BOTTLE += b2

    b2 = [[] for _ in range(COLS[1])]
    j = 0
    for i in b[4*(COLS[0]):]:
        b2[j].append(i)
        j = (j+1)%(COLS[1])
    BOTTLE += b2

    BOTTLE[0], BOTTLE[1] = [], []
    check = np.array(BOTTLE[2:])
    check = list(check.flat)
    check = Counter(check)
    if len(check) != sum(COLS) - 2:
        return False
    for i in check:
        if check[i] != 4:
            return False
    # print(BOTTLE)
    return BOTTLE


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
LIMIT = 1000

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
    global Situations, LIMIT
    if len(Situations) == LIMIT:
        return False
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

def opt(path):
    num1, num2 = list(), list()
    for p in path:
        x = p.split()
        num1.append(int(x[0]))
        num2.append(int(x[-1]))
    for i,n in enumerate(num1):
        m = num2[i]
        if n in num2[i+1:]:
            j = num2[i+1:].index(n)+i+1
            if m != num1[j]:
                continue
            if n in num1[i+1:j] or m in num1[i+1:j] or n in num2[i+1:j] or m in num2[i+1:j]:
                continue
            path = path[:i]+path[i+1:]
            return opt(path)
    return path


Situations = list()
path = list()


def main(p_dir='./p1.jpg',X=7,Y=7):
    Bottle_start = False
    for X in [7,6,5]:
        for Y in range(7,X-1,-1):
            Bottle_start = p_read(p_dir,X,Y)
            if Bottle_start:
                break
        if Bottle_start:
            break
    if not Bottle_start:
        for X in range(9,2,-1):
            for Y in (9,2,-1):
                Bottle_start = p_read(p_dir,X,Y)
                if Bottle_start:
                    break
            if Bottle_start:
                break

    global BOTTLE_NUM
    BOTTLE_NUM = X+Y
    assert(Bottle_start[0] == [])
    assert(Bottle_start[1] == [])
    assert len(Bottle_start) == BOTTLE_NUM
    
    # print(Bottle_start)
    # exit()

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
                pre_path.append(f"{i+1} → {turn+1}")
        Bottle_start[turn] = [mc for _ in range(m)]

    # Bottle_start = p_read(p_dir,X,Y)
    # print(Bottle_start)

    PRE = True
    global LIMIT
    while True:
        if not op(Bottle_start):
            PRE = False
            # print("pre-false\n")
            Bottle_start = p_read(p_dir,X,Y)
            if not op(Bottle_start):
                # print(r"can't get!")
                # exit()
                LIMIT += 1000
            else:
                break
        else:
            break
    
    Path = opt(path[::-1])
    # Path = path[::-1]
    with open('./result.txt','w') as f:
        if PRE:
            for i in pre_path:
                f.write(f"{i}\n")
        for i in Path:
            f.write(f"{i}\n")

    print('--------------')
    print('总步数(不包含预处理）：',len(Path))
    print('优化步数：',len(path)-len(Path))
    print(f'操作用时：{time.time() - t_start:.3f}',)
    print('--------------')

if __name__ == "__main__":
    if len(sys.argv) > 1:
        p_dir = sys.argv[1]
        X = int(sys.argv[2])
        Y = int(sys.argv[3])
        BOTTLE_NUM = X+Y
        main(p_dir,X,Y)
    else:
        main()