import argparse
from operator import itemgetter
import cv2
import numpy as np
import matplotlib.pyplot as plt
from Normalise import Normalise
from Ransac import RANSAC
from Homography import PerspectiveTransform
from Disparity import Disparity
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('--option', '-o', default= 1)
args = parser.parse_args()

class Main:
    
    def check_F_validity(self, src_points_new, dst_points_new, F_temp, F):
        for i in range(len(src_points_new)):
            a = np.array([src_points_new[i][0], src_points_new[i][1], 1])  
            b = np.array([dst_points_new[i][0], dst_points_new[i][1], 1])  
            print("F_pred ",(b.dot(F)).dot(a.T))
            print("  F_cv2_pred",(b.dot(F_temp)).dot(a.T))    

    def find_matched_points(self, img1, img2):

        MIN_MATCHES = 50

        orb = cv2.ORB_create(nfeatures=500)
        kp1, des1 = orb.detectAndCompute(img1, None)
        kp2, des2 = orb.detectAndCompute(img2, None)

        index_params = dict(algorithm=6,
                            table_number=6,
                            key_size=12,
                            multi_probe_level=2)
        search_params = {}
        flann = cv2.FlannBasedMatcher(index_params, search_params)
        matches = flann.knnMatch(des1, des2, k=2)

        good_matches = []
        # ratio test as per Lowe's paper
        for i,(m,n) in enumerate(matches):
            if m.distance < 0.7*n.distance:
                good_matches.append(m)

        if len(good_matches) > MIN_MATCHES:
            src_points = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 2)
        
            dst_points = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 2)

            F, src_points, dst_points = RANSAC().ransac(src_points, dst_points)
 
            return F, src_points, dst_points
    
    def extract_camera_pose(self, F, intrinsic_mat):

       # intrinsic_mat=np.array([[1758.23, 0, 977.42], [0, 1758.23, 552.15], [0, 0, 1]])
       
        E = intrinsic_mat.T.dot(F).dot(intrinsic_mat)
        u, s, vh = np.linalg.svd(E)

        print ("Essential matrix:")
        print(E)
        
        w = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]])
        c1 = u[:,2]
        c2 = -u[:,2]
        c3 = u[:,2]
        c4 = -u[:,2]
        
        r1 = u.dot(w).dot(vh)
        r2 = u.dot(w).dot(vh)
        r3 = u.dot(w.T).dot(vh)
        r4 = u.dot(w.T).dot(vh)

        print ("T matrix:")
        print(c1)
        
        print ("R matrix:")
        print(r1)
        
    def main(self, img1, img2, intrinsic_mat, f, baseline):
        
        F, src_points, dst_points = self.find_matched_points(img1, img2)
        self.extract_camera_pose(F, intrinsic_mat)

        img1, img2, F = PerspectiveTransform().transform_perspective(img1, img2, F, np.asarray(src_points), np.asarray(dst_points))
        Disparity().find_disparity_(img1, img2, F, f, baseline)

if __name__ == "__main__":
    

    des = int(args.option)
    print(des)

    if des == 1:
        im1 = cv2.imread("curule/im0.png",cv2.IMREAD_GRAYSCALE)
        im2 = cv2.imread("curule/im1.png",cv2.IMREAD_GRAYSCALE)
        intrinsic_mat=np.array([[1758.23, 0, 977.42], [0, 1758.23, 552.15], [0, 0, 1]])
        f = 1758.23
        baseline=88.39
    
    elif des == 2:
        im1 = cv2.imread("octagon/im0.png",cv2.IMREAD_GRAYSCALE)
        im2 = cv2.imread("octagon/im1.png",cv2.IMREAD_GRAYSCALE)
        intrinsic_mat=np.array([[1742.11, 0, 804.90], [0, 1742.11, 541.22], [0, 0, 1]])
        f = 1742.11
        baseline=221.76

    elif des == 3:
        im1 = cv2.imread("pendulum/im0.png",cv2.IMREAD_GRAYSCALE)
        im2 = cv2.imread("pendulum/im1.png",cv2.IMREAD_GRAYSCALE)
        intrinsic_mat=np.array([[1729.05, 0, -364.24], [0, 1729.05, 552.22], [0, 0, 1]])
        f = 1729.05
        baseline=537.75
    
        
    Main().main(im1, im2,  intrinsic_mat, f, baseline)

