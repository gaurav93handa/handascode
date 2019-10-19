import cv2
import numpy as np
import glob
import os

#Parsing curves from the .skl file
basePath=r"D:\skelton-approach\Final_data\2.skel";

#Fetaching raw data from file
array_count=0;
points=[]
points_freq=[]
count_value=0;
for line in open(basePath,'r'):
    if line.find("CNN")!= -1:
        count=[int(s)for s in line.split() if s.isdigit()]
        count_value=count[0];
        points_freq.append(count_value);
        continue;
    if count_value!= 0:
        points.append(line);
        count_value= count_value -1;
point_freq=np.array(points_freq)
print(len(points_freq))
print(points_freq)
print(len(points))
print(points)


#Converting raw dat to numpy arrays
curveCount = len(points_freq)
pointscount = sum(points_freq)
point_list=[]
for i in range (0, pointscount):
    point_list.append(points[i].rstrip('\n').rstrip().split('\t'))
point_array=np.float32(point_list)
point_sorted=point_array[point_array[:,0].argsort()]
print(point_list)
print(point_array)

path=r'D:\skelton-approach\Final_data\2_ordered.obj'
file=open(path,'w+')
for j in range(0, len(point_array) - 1):
    file.write("v %f %f %f\n" % (float(point_array[j][0]), float(point_array[j][1]), float(point_array[j][2])))
file.close()
