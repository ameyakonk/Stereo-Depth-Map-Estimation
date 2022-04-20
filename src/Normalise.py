import argparse
from operator import itemgetter
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import random

class Normalise:
        
    def normalise_points(self, src_points, dst_points):
        def segregate_x_y(points):
            x = []
            y = []
            for data in points:
                x.append(data[0])
                y.append(data[1])
            return x, y

        def centroid(x, y):
            return np.mean(x), np.mean(y)   

        def compute_S(x, y):
            mean = np.mean(np.add(np.square(x),np.square(y)))
            return math.pow(2/mean,0.5)

        def compute_t_mat(s, u, v):
            a = np.array([[s, 0, 0],
                        [0, s, 0],    
                        [0, 0, 1]])
            
            b = np.array([[1, 0, -u],
                        [0, 1, -v],    
                        [0, 0, 1]])
            return np.matmul(a, b)

        x, y = segregate_x_y(src_points)
        x_dash, y_dash = segregate_x_y(dst_points)

        x_c, y_c = centroid(x, y)
        x_dash_c, y_dash_c = centroid(x_dash, y_dash)
        
        x_tilda = x - x_c
        y_tilda = y - y_c

        x_dash_tilda = x_dash - x_dash_c
        y_dash_tilda = y_dash - y_dash_c
        
        s = compute_S(x_tilda, y_tilda)
        s_dash = compute_S(x_dash_tilda, y_dash_tilda)

        t_a = compute_t_mat(s, x_c, y_c)
        t_b = compute_t_mat(s_dash, x_dash_c, y_dash_c)
     
        one = np.ones((len(x)))
        src_new = np.matmul(t_a,np.vstack(([x], [y], [one])))
        dst_new = np.matmul(t_b,np.vstack(([x_dash], [y_dash], [one])))

        return src_new[0:2].T, dst_new[0:2].T, t_a, t_b

