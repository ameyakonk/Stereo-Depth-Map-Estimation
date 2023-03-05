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
### Original images

![image](https://user-images.githubusercontent.com/78075049/222946221-aa6260d9-bdd5-4db1-bace-dbbed800cdd7.png)
