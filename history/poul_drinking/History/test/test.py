from PIL import Image 
import numpy as np
 
image = Image.open("./test.jpg") # 用PIL中的Image.open打开图像
image_arr = np.array(image) # 转化成numpy数组
print(image_arr[0][0])
print(image_arr[100][0])
print(image_arr[0][100])