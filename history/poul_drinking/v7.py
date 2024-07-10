import copy
import time
import sys
from picture_read import p_read
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
    if not op(Bottle_start):
        PRE = False
        # print("pre-false\n")
        Bottle_start = p_read(p_dir,X,Y)
        if not op(Bottle_start):
            # print(r"can't get!")
            exit()

    with open('./result.txt','w') as f:
        if PRE:
            for i in pre_path:
                f.write(f"{i}\n")
        for i in path[::-1]:
            f.write(f"{i}\n")

    print('--------------')
    print('总步数：',len(path))
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