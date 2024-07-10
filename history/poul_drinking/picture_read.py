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


if __name__ == "__main__":
    p_read('./p1.jpg',7,7)