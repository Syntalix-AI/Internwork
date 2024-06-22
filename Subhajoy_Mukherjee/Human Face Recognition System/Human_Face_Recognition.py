#Libraries to be Installed Before running the Code:
#pip install --upgrade pip
#pip install --upgrade pip setuptools
#pip install cmake
#pip install dlib
#pip install face-recognition
#pip install opencv-python

import os
import numpy as np
import face_recognition
import time

import cv2

Images=[]
Unique_ID=[]
training_face_encoding=[]
#This is the existing image dataset Path Link
Dataset_path='C:/Users/subha/Documents/GitHub/Internwork/Subhajoy_Mukherjee/Human Face Recognition System/ImageDataSet'

#This function will load images frrom the existing dataset into a variable by cv2
def loading_images(path):
    files=os.listdir(path)
    Image_List=[]
    for i in files:
        currImage=cv2.imread(f'{path}/{i}')
        
        Image_List.append(currImage)
        return Image_List
        

#This function will load IDs frrom the existing dataset into a variable by cv2
def loading_IDs(path):
    files=os.listdir(path)
    ID_List=[]
    for i in files:
        ID_List.append(os.path.splitext(i)[0])
        return ID_List
#This will extract features from each images in the dataset and stored the features in a variable  
#This fuction parameter is pixels values of in numpy array/List of numpy arrays containing pixel values of images 
#This will return List of faceencoding of images
def training_images(Images):     #This will extract features from the Images datasets
        ImageEncodeList=[]
        for i in Images:
            face_encode=face_recognition.face_encodings(i)[0]    #face_encoding function returns a set of 128 computer-generated measurements from a image from its features. 
            ImageEncodeList.append(face_encode)
        return ImageEncodeList

def update_image_dataset(ImageArray):
    filename=str(len(Unique_ID)+1)+".png"
    os.chdir(Dataset_path)
    flag=cv2.imwrite(filename,ImageArray)
    if(flag==0):
        print("ERROR : Problem in Image DataBase Updation")
    else:
        print("Image DataBase Succesfully Updated ")

    



#This  part will take picture from webcam in REALTIME

Images=loading_images(Dataset_path)
Unique_ID=loading_IDs(Dataset_path)

training_face_encoding=training_images(Images)

cap=cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
while (cap.isOpened()):
    success,img=cap.read()  #cap.read() function returns the bool value of is the video read or not and the numpy array of the readed video pixels in a tuple form
    img=cv2.resize(img,(640,480))  #Resize the video frame to increase the Resolution
    face_in_frame=face_recognition.face_locations(img)
    #print(face_in_frame)
    #print(type(face_in_frame))
    encode_face_in_frame=face_recognition.face_encodings(img,face_in_frame)
    for i,faceloc in zip(encode_face_in_frame,face_in_frame):
        match=face_recognition.compare_faces(training_face_encoding,i)
        face_distance=face_recognition.face_distance(training_face_encoding,i)
        match_index=np.argmin(face_distance)
        top,right,bottom,left=faceloc
        if match[match_index]:
            ID=Unique_ID[match_index]
#cv2.rectangle function parameters are: 
#Image(pixel values in numpy array),top-left co-ordinate ,bottom-right co-ordinate of rectangle, color of rectangle(Red,Green, Blue values), Thickness of the rectangle line
            cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),2)
            cv2.rectangle(img,(left,bottom+35),(right,bottom),(0,255,0),cv2.FILLED)  #This function is to make filled place at the botto of the rectangle
            cv2.putText(img,f'ID : {ID}',(left,bottom+30),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
        else:
            region_of_interest=img[top-25:bottom+25,left-25:right+25]
            update_image_dataset(region_of_interest)
            Images=loading_images(Dataset_path)
            Unique_ID=loading_IDs(Dataset_path)
            training_face_encoding=training_images(Images)
            
     
    
    cv2.imshow('Human Face Recognition',img)
    
    cv2.waitKey(1)            
            
            
        
    
    
    
    


#Face Recognition Library loads images in the form of BGR 
