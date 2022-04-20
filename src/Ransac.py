import argparse
from dis import distb
from operator import itemgetter
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import random
from Normalise import Normalise

class RANSAC:
    def __init__(self) -> None:
        pass    
    
    def find_fundamental_matrix(self, src_points, dst_points):
        
        def reduce_f_mat_rank():
            u_f, s_f, vh_f = np.linalg.svd(F)
            s_f[-1] = 0
            F_new = np.matmul(u_f*s_f, vh_f)
            return F_new

        A_mat = []
        row = []

        for i in range(len(src_points)):
            row.append(src_points[i][0]*dst_points[i][0])     # x*x_dash
            row.append(src_points[i][0]*dst_points[i][1])     # x*y_dash
            row.append(src_points[i][0])                      # x
            row.append(src_points[i][1]*dst_points[i][0])     # y*x_dash
            row.append(src_points[i][1]*dst_points[i][1])     # y*y_dash
            row.append(src_points[i][1])                      # y
            row.append(dst_points[i][0])                      # x_dash
            row.append(dst_points[i][1])                      # y_dash
            row.append(1)                                     # 1
            rc = row.copy()
            A_mat.append(rc)
            row.clear()
        
        u, s, vh = np.linalg.svd(A_mat)
        x = vh[-1]
        
        F = np.reshape(x, [3,3])

        if np.linalg.matrix_rank(F) == 3:
            F = reduce_f_mat_rank()  

        return F

    def ransac(self, src_points, dst_points):

        max_Iterations = 1000
        ransac_minpoint = 8 
        ransac_threshold = 0.02 #5000

        random_list = list(zip(src_points, dst_points))
   
        src_inliers = []
        dst_inliers = []
        F_final = []

        for i in range(max_Iterations):
            random.shuffle(random_list)
            src_points, dst_points = zip(*random_list)

            src_points_norm, dst_points_norm, t_a, t_b = Normalise().normalise_points(src_points[0:8], dst_points[0:8])
            
            F_norm = RANSAC().find_fundamental_matrix(src_points_norm, dst_points_norm)
            F = (t_b.T.dot(F_norm)).dot(t_a)

            src_inliers_temp = []
            dst_inliers_temp = []

            for j in range(len(src_points)):
              
                a = np.array([src_points[j][0], dst_points[j][1], 1])  
                b = np.array([src_points[j][0], dst_points[j][1], 1])  
                if abs(b.dot(F).dot(a.T)) < ransac_threshold:
               
                    src_inliers_temp.append(src_points[j])
                    dst_inliers_temp.append(dst_points[j])

            if len(dst_inliers_temp) > ransac_minpoint:
                F_final = F
                
                src_inliers = src_inliers_temp
                dst_inliers = dst_inliers_temp
                
                ransac_minpoint = len(dst_inliers_temp) 
        
        return F_final, src_inliers, dst_inliers
