import numpy as np
import scipy.io as scio
import imageio
import car_window_v7
import time

# start = time.clock()
# image_path = r'C:\Users\ZY\Desktop\new_image_partition\869.png'
# rgb_image = imageio.imread(image_path)
# img_data = 'E://img_data.mat'
# #N是需要保存的矩阵，A为字典名，读取的方便，保存为新矩阵dataNew=img_data
# scio.savemat(img_data, {'rgb_image':rgb_image})

# print(np.shape(rgb_image))
# a = car_window_v7.initialize()
# end3 = time.clock()
# s = a.main(img_data) #这里运行时间长，time.clock()的差值为大概为10s
# print(end3-start)
# end4 = time.clock()
# print(s)
# print(end4-start) #输出s的值要5s
# a.terminate
