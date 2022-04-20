import argparse
from operator import itemgetter
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from tqdm import tqdm

class Disparity:

    def find_disparity_(self, img1, img2, F, f, baseline):
        disp_img = np.zeros((img1.shape[0], int(img1.shape[1]),1), dtype=np.uint8)
    
        block_size = 5
        
        for i in tqdm(range(block_size, img1.shape[0], block_size)):
            x = np.repeat(np.arange(start=i-block_size, stop=i+block_size), 2*block_size)

            for j in range(block_size, int(img1.shape[1]), block_size):

                y = np.tile(np.arange(start=j-block_size, stop=j + block_size), 2*block_size)
                block_left = img1[x,y]
                
                min_ = 1000000000
                index = j
                for k in range(max(block_size, j - 100), j, block_size):
                    z = np.tile(np.arange(start=k-block_size, stop=k + block_size), 2*block_size)
                   
                    block_right = img2[x, z]
                    difference = np.sum(np.square(np.subtract(block_left, block_right)))
                    if(difference < min_):
                        index = k
                        min_ = difference

                disp_img[x, y] = int(abs(index - j))
                # print(abs(index - j))

        min_ = np.min(disp_img)
        max_ = np.max(disp_img)
        print(min_)
        print(max_)

        disp_img_final = np.zeros((img1.shape[0], int(img1.shape[1])))
        depth_img_final = np.zeros((img1.shape[0], int(img1.shape[1])))

        # f = 1758.23
        # baseline=88.39
        slope = (255 - 0) / (max_ - min_)
        disp_img_final = np.multiply(disp_img, slope)
        depth_img_final = np.multiply(1/disp_img + 1e-10, baseline*f)

        plt.imshow(disp_img_final, cmap="gray")
        plt.show()
      
        plt.imshow(depth_img_final, cmap="gray")
        plt.show()
      
