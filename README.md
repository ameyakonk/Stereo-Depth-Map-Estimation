# Stereo-Depth-Map-Estimation

## Overview
The repository contains the following contents.

Following processes are performed on three sets of images namely Curule, Octagon and Pendulum.

1. Camera caliberation, Fundamental matrix using RANSAC, Essential Matrix, Camera Rotation and Camera Matrix estimation estimation.
2. Image rectification using Fundamental matrix and Plotting Epipolar lines.
3. Disparity Image estimation 
4. Depth image estimation. 

## Personnel
### Ameya Konkar 

UID:118191058

Master's Student at University of Maryland, College Park

## Dependencies 

1.  Python 3.7.x
2.  Matplotlib
3.  Numpy
4.  tqdm
 
### Building the Program and Tests

```
sudo apt-get install git
git clone --recursive https://github.com/ameyakonk/Stereo-Depth-Map-Estimation.git
cd <path to repository>
conda activate <name of env>
```

To Run the code:
```
cd src/
chmod +x calibration2.py
```

For Curule Dataset.
``` 
python calibration2.py -o 1
```

For Octagon Dataset.
``` 
python calibration2.py -o 2
```

For Pendulum Dataset.
``` 
python calibration2.py -o 3
```
## Results
The depth estimation was performed on the three classes Curule, Pendulum and Octagon
Folowing are the results for the Curule class

Markup : - Curule
          
### Original images

<p float="left">
  <img src="https://user-images.githubusercontent.com/78075049/222946262-9f915a81-ab35-4050-ac24-81ddb534d099.png" width="400" height="280">
  <img src="https://user-images.githubusercontent.com/78075049/222946487-448c8c62-17a3-490d-91a3-0a80c20fcb82.png" width="400" height="280">
</p>

### Rectified images
<img src="https://user-images.githubusercontent.com/78075049/222946895-543fcd6d-668f-4f82-9f86-901cc5adea08.png" width="800" height="560">

### Disparity map 
<img src="https://user-images.githubusercontent.com/78075049/222946850-6c3eedea-7384-4636-af68-821f8622d991.png" width="800" height="580">

### Depth map
<img src="https://user-images.githubusercontent.com/78075049/222946829-b2923646-8d3b-4aeb-9414-5c55c7181838.png" width="800" height="580">

