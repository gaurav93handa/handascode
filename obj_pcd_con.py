import numpy as np

path=r'C:\Users\abc\Desktop\PCLProject\testing\final_initial_alignment\2018-10-12\vicon_wrist_shot_one_foot\IA\frame3\pruned_cloud.obj'

#getting new path
path=path.replace('\\','/')
base_path=path.rsplit('/',1)
name=base_path[1].split('.')
print(name)
new_path=base_path[0]+'/'+name[0]+'.pcd'


#convert obj->pcd
file=open(path,'r')
list_norm=[]
list_xyz=[]
for i in file:
    if not(i.find('vn')):
        string=i.strip("vn").strip('\n').replace(" ",",").strip("").split(",")
        del string[0]
        list_norm.append(string)
    else:
        string = i.strip("v").strip('\n').replace(" ",",").strip("").split(",")
        del string[0]
        list_xyz.append(string)
file.close()
list_xyz=np.float32(list_xyz)
list_norm=np.float32(list_norm)

file_new=open(new_path,'w+')
if len(list_norm)==0:
    file_new.write("# .PCD v0.7 - Point Cloud Data file format\n\
VERSION 0.7\n\
FIELDS x y z\n\
SIZE 4 4 4\n\
TYPE F F F\n\
COUNT 1 1 1\n\
WIDTH %s\n\
HEIGHT 1\n\
VIEWPOINT 0 0 0 1 0 0 0\n\
POINTS %s\n\
DATA ascii\n\
    "%(str(len(list_xyz)),str(len(list_xyz))))
    for i in range(0,len(list_xyz)):
        file_new.write("%f %f %f\n"%(list_xyz[i][0],list_xyz[i][1],list_xyz[i][2]))
    file_new.close()
else:
    file_new.write("# .PCD v0.7 - Point Cloud Data file format\n\
VERSION 0.7\n\
FIELDS x y z\n\
SIZE 4 4 4\n\
TYPE F F F\n\
COUNT 1 1 1\n\
WIDTH %s\n\
HEIGHT 1\n\
VIEWPOINT 0 0 0 1 0 0 0\n\
POINTS %s\n\
DATA ascii\n\
" % (str(len(list_xyz)), str(len(list_xyz))))
    for i in range(0, len(list_xyz)):
        file_new.write("%f %f %f %f %f %f\n" % (list_xyz[i][0], list_xyz[i][1], list_xyz[i][2],list_norm[i][0], list_norm[i][1], list_norm[i][2]))
    file_new.close()
