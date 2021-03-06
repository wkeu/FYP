# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 16:56:30 2017

@author: temp2015
"""

"""
The difference between main and main2 is that we rotate the image to get two sets of point clouds
"""


import cv2
import numpy as np
from get_xyz import *
from calculate_rmsd import *
from rotate_map import *
import timeit


#TODO: remove the timer. 
#TODO: Aadd functionality to allow people to input their own video into the script. Easy enough to do
#       add a line where the person can put in their own directory. 



###############################################################################
# Obtain Rotations
###############################################################################
start = timeit.default_timer()


#Import Video
fname="test1_raw_initial_test.mp4"
fout="derotated_footage.avi"
cap = cv2.VideoCapture(fname) #Open Video File, from current directory
out_fps=30

#Obtain Rotation Matrices
#Using Train and Query image. Query behind train ie Query=frame_n-1,train=frame_n

#Initial setup for loop
ret, train = cap.read()
U_stream=list()

while(cap.isOpened()):
    
    query=train 
    ret, train = cap.read()
    
    if ret==0:
        break
    
    #Definitly not the most efficient implemenation
    #Calculating Certain Values Twice
    query_matched_pc, train_matched_pc =obtain_point_cloud(query,train)

    
    query_low_res = cv2.resize(query, (0,0), fx=0.125, fy=0.125) 
    train_low_res = cv2.resize(train, (0,0), fx=0.125, fy=0.125) 
    
    query_polar=rotate_map(query_low_res,y_axis_45())
    train_polar=rotate_map(train_low_res,y_axis_45())
    
    query_matched_pc_y_axis_45, train_matched_pc_y_axis_45 =obtain_point_cloud(query_polar,train_polar)
    
    #Rotate points back 45 degrees about y axis
    query_matched_pc_y_axis_45=point_cloud_multiplication(-y_axis_45(),query_matched_pc_y_axis_45)
    train_matched_pc_y_axis_45=point_cloud_multiplication(-y_axis_45(),train_matched_pc_y_axis_45)

    query_final_pc=np.concatenate((query_matched_pc,query_matched_pc_y_axis_45))
    train_final_pc=np.concatenate((train_matched_pc,train_matched_pc_y_axis_45))
    
    #rotational_matrix=kabsch(query_matched_pc, train_matched_pc)
    U=kabsch(train_matched_pc,query_matched_pc) #Assume for the moment that this matrix is correct. 
    
    U_stream.append(U)
    print("U obtained for frame"+str(len(U_stream)))
    
print("o.O.o\nRotational Matrix Stream Obtained")

###############################################################################
#Acumulate matrices
###############################################################################
n_frames=len(U_stream)

U_stream_acumilated=list()
U_stream_acumilated.append(U_stream[0])
U_acumilated=np.matrix(U_stream[0])

for n in range(1,n_frames):
    U_acumilated= U_acumilated*np.matrix(U_stream[n])
    U_stream_acumilated.append(U_acumilated)

print("o.O.o\nRotational Matrices Accumulated")

midway = timeit.default_timer()

###############################################################################
#Derotation of frames
###############################################################################

cap = cv2.VideoCapture(fname) #Open Video File, from current directory

#Open Output file
#Initial setup for loop, initial frame can be left as is
ret, frame_n = cap.read()

#*'XVID'
#*"MP4V"
fourcc = cv2.VideoWriter_fourcc(*'XVID')

out=cv2.VideoWriter(fout,fourcc,out_fps,(int(frame_n.shape[1]),int(frame_n.shape[0]))) #make sure the dimensions are the same size as input data 

#Write out initial unchanged frame
out.write(frame_n)
n=0

while(cap.isOpened()):
    
    ret, frame_n = cap.read()
    
    if ret==False:
        break
   
    frame_stabilized=rotate_map(frame_n,U_stream_acumilated[n])
    n+=1
    
    out.write(frame_stabilized)
    print("frame" +str(n)+"completed")
    
cap.release()
out.release()

stop = timeit.default_timer()
 

print("Half:"+str(midway - start))
print("Overall:"+str(stop - start))

print("o.O.o\nStabilised Video Outputed")



"""
Trobleshooting
theta_U=(np.pi/2)   #Set rotation angle

#Rotation matrices for each axis
U=np.matrix([ [np.cos(theta_U), -np.sin(theta_U), 0] , [np.sin(theta_U), np.cos(theta_U), 0] , [ 0, 0, 1] ])
"""