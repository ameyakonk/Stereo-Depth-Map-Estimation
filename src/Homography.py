import argparse
from operator import itemgetter
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math
import random


class PerspectiveTransform:

    def drawlines(self, img1, img2, lines, pts1, pts2):
    
        r, c = img1.shape
        img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
        img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
        
        for r, pt1, pt2 in zip(lines, pts1, pts2):
            
            # color = tuple(np.random.randint(0, 255,
            #                                 3).tolist())
            
            color = (255, 0, 0)
            x0, y0 = map(int, [0, -r[2] / r[1] ])
            x1, y1 = map(int, 
                        [c, -(r[2] + r[0] * c) / r[1] ])
            
            img1 = cv2.line(img1, 
                            (x0, y0), (x1, y1), color, 1)
            img1 = cv2.circle(img1,
                          (round(pt1[1]),round(pt1[0])) , 5, (0, 255, 0), -1)
            img2 = cv2.circle(img2,
                    (round(pt2[1]),round(pt2[0])) , 5, (0, 255, 0), -1)
            # img2 = cv2.circle(img2,             #                 tuple(pt2), 5, color, -1)
        return img1, img2

    def plt_epipolar_lines(self, F, ptsLeft, ptsRight, imgLeft, imgRight):

        print("Fundamental Matrix :")
        print(F)
        
        linesLeft = cv2.computeCorrespondEpilines(ptsRight.reshape(-1,1,2),2, F)
        
        linesLeft = linesLeft.reshape(-1, 3)
   
        img5, img6 = self.drawlines(imgLeft, imgRight, 
                            linesLeft, ptsLeft,
                            ptsRight)
        
        # Find epilines corresponding to 
        # points in left image (first image) and
        # drawing its lines on right image
        linesRight = cv2.computeCorrespondEpilines(ptsLeft.reshape(-1, 1, 2), 
                                                1, F)
        linesRight = linesRight.reshape(-1, 3)
        
        img3, img4 = self.drawlines(imgRight, imgLeft, 
                            linesRight, ptsRight,
                            ptsLeft)
        
        return img3, img5

    def transform_perspective(self, img1, img2, F, src_points, dst_points): 
        
        img6, img7 = self.plt_epipolar_lines(F, np.asarray(src_points), np.asarray(dst_points), img1, img2)
        plt.subplot(121), plt.imshow(img6)
        plt.subplot(122), plt.imshow(img7)
        plt.show()

        retBool ,rectmat1, rectmat2 = cv2.stereoRectifyUncalibrated(src_points.reshape(-1, 1, 2),dst_points.reshape(-1, 1, 2),F,(img1.shape[1],img1.shape[0]))
        
        # Apply Perspective Transform Algorithm
        img3 = cv2.warpPerspective(img1, rectmat1, (img1.shape[1], img1.shape[0]))
        img5 = cv2.warpPerspective(img2, rectmat2, (img1.shape[1], img1.shape[0]))
        
        F_new = np.linalg.inv(rectmat2).T.dot(F).dot(np.linalg.inv(rectmat1))   
        
        img3, img5 = self.plt_epipolar_lines(F_new, np.asarray(src_points), np.asarray(dst_points), img3, img5)
        
        plt.subplot(121), plt.imshow(img3)
        plt.subplot(122), plt.imshow(img5)
        plt.show()

        return img3, img5, F_new