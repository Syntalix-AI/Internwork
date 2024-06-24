#Libraries to be installed before execution: 
#!pip install opencv-python
#!pip install cmake
#!pip install dlib
#!pip install face_recognition
#!pip install deepface

#Importing libraries
import cv2
import face_recognition
from deepface import DeepFace
import os

Dataset_path='C:/Users/subha/Documents/GitHub/Internwork/Subhajoy_Mukherjee/Human Face Recognition System/ImageDataSetFor_2.0'

#Facial data extract
def Image_Extract(output_list_of_extract_faces):
  frame_images=[]
  a=dict()
  for i in range(len(output_list_of_extract_faces)):
    a=output_list_of_extract_faces[i]
    b=float(a.get('confidence'))
    if(b>0):
      frame_images.append(output_list_of_extract_faces[i].get('face'))
    else:
      print('No Faces detected!!!!')
  return frame_images

#Facial Loactaion Extract
'''def Image_Loc_Extract(output_list_of_extract_faces):
  for i in range(len(output_list_of_extract_faces)):
    face_loc=[]
    a=output_list_of_extract_faces[i]
    b=float(a.get('confidence'))
    c=dict(a.get('facial_area'))
    if(b>0.50):
      loc=[]
      loc.append(c.get('x'))
      loc.append(c.get('y'))
      loc.append(c.get('w'))
      loc.append(c.get('h'))
      face_loc.append(loc)
    else:
      print('No Faces detected!!!!')
  return face_loc'''

#This Function will update new faces in the Dataset whose path is specified in line no. 14
def update_image_dataset(ImageArray):
    Unique_ID=os.listdir(Dataset_path)
    filename=str(len(Unique_ID)-5)+".png"
    os.chdir(Dataset_path)
    flag=cv2.imwrite(filename,ImageArray)
    if(flag==0):
        print("ERROR : Problem in Image DataBase Updation")
    else:
        print("Image DataBase Succesfully Updated ")
        
        
#This part will take pictures from webcam in REALTIME
cap=cv2.VideoCapture(0)
cap.set(3,1080)
cap.set(4,720)
while (cap.isOpened()):
    Frame_Images=[]
    Face_Locations=[]#It will be a list of lists where each loaction will be saved as [x,y,w,h]
    ID_List=[]
    success,img=cap.read()
    #img=cv2.resize(img,(640,480))
    df1=DeepFace.extract_faces(img,detector_backend='opencv',enforce_detection=False)  #Here 
    Frame_Images=Image_Extract(df1)
    #Face_Locations=Image_Loc_Extract(df1)  : This fuction is giving sometimes ERROR so if it is used them it is asked to comment out below try-except bloc
    #Also comment out the whole function above named : "Image_Loc_Extract" & 73,74,81,82,83,84,103 line of code and comment in the 85 line of code. Also in the 75 line write the for-loop as : for imgs in Ftrame_Images  
    #i=0
    face_in_frame=face_recognition.face_locations(img)
    for imgs,face_loc in zip(Frame_Images,face_in_frame):
        df3=DeepFace.find(imgs,db_path=Dataset_path,enforce_detection=False,model_name='VGG-Face',threshold=0.90) 
        #Here in model_name=["Facenet512","Facenet","Dlib","VGG-Face","ArcFace","GhostFaceNet", "SFace","OpenFace", "DeepFace", "DeepID" ]
        #All the models are written in the decendeing order of their accuracy any and acsending order of their speed. 
        #According them 'VGG-Face' is suggested to use 
#        try:
        #left=Face_Locations[i][0]
        #right=Face_Locations[i][0]+Face_Locations[i][2]
        #top=Face_Locations[i][2]
        #bottom=Face_Locations[i][2]+Face_Locations[i][3]
        top,right,bottom,left=face_loc
        if (df3[0]['identity'].empty):
          try:
            region_of_interest=img[top-30:bottom+30,left-30:right+30]
          except:
            region_of_interest=img[top:bottom,left:right]
          update_image_dataset(region_of_interest)
          break
        else:  
            ID=df3[0]['identity'][0]
            ID=ID.split("\\")
            ID=ID[-1]
            ID=ID.split('.')
            ID=ID[0]
           
            cv2.rectangle(img,(left,top),(right,bottom),(0,255,0),2)
            cv2.rectangle(img,(left,bottom+35),(right,bottom),(0,255,0),cv2.FILLED)
            cv2.putText(img,f'ID : {ID}',(left,bottom+30),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2) 
            #i+=1
#        except:
#            break
    
    cv2.imshow('Human Face Recognition',img)
    cv2.waitKey(1) 
    if (cv2.waitKey(1) & 0xFF) == ord('q'):  # Press 'q' from keyboard and press ENTER to exit the loop
        break          
            
cap.release()
cv2.destroyAllWindows() 