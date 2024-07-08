import os
import numpy as np
import face_recognition
import cv2

Dataset_path = 'C:\\Users\\subha\\Documents\\GitHub\\Internwork\\Subhajoy_Mukherjee\\Human Face Recognition System\\ImageDataSet'
next_id = 1  # Initial unique ID counter

Images = []
Unique_ID = []
training_face_encoding = []

# Function to load images from the dataset
def loading_images(path):
    files = os.listdir(path)
    Image_List = []
    for i in files:
        currImage = cv2.imread(os.path.join(path, i))
        Image_List.append(currImage)
    return Image_List

# Function to load IDs from the dataset
def loading_IDs(path):
    files = os.listdir(path)
    ID_List = []
    for i in files:
        ID_List.append(os.path.splitext(i)[0])
    return ID_List

# Function to extract face encodings from images
def training_images(Images):
    ImageEncodeList = []
    for img in Images:
        face_locations = face_recognition.face_locations(img)
        if face_locations:
            face_encode = face_recognition.face_encodings(img, face_locations)[0]
            ImageEncodeList.append(face_encode)
        else:
            # Handle case where no faces are detected
            print("No face detected in an image.")
            # You might want to log this or handle it differently based on your application needs
    return ImageEncodeList


# Function to update the image dataset with a new image
def update_image_dataset(image_array):
    global next_id
    filename = f"{next_id}.png"
    os.chdir(Dataset_path)
    flag = cv2.imwrite(filename, image_array)
    if flag == 0:
        print("ERROR: Problem in Image Database Updation")
    else:
        print(f"Image {filename} added to dataset with ID {next_id}")
        next_id += 1
        Unique_ID.append(filename.split('.')[0])
        Images.append(image_array)
        training_face_encoding.append(face_recognition.face_encodings(image_array)[0])

# Initialize dataset and encodings
Images = loading_images(Dataset_path)
Unique_ID = loading_IDs(Dataset_path)
training_face_encoding = training_images(Images)

# Initialize webcam capture
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)

while cap.isOpened():
    success, img = cap.read()
    img = cv2.resize(img, (640, 480))

    face_locations = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        # Check if the detected face matches any of the known faces
        matches = face_recognition.compare_faces(training_face_encoding, face_encoding)
        face_distances = face_recognition.face_distance(training_face_encoding, face_encoding)
        match_index = np.argmin(face_distances)

        top, right, bottom, left = face_location

        if matches[match_index]:
            # Match found with an existing face
            ID = Unique_ID[match_index]
            cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.rectangle(img, (left, bottom + 35), (right, bottom), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, f'ID: {ID}', (left, bottom + 30), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
        else:
            # No match found, add new face to dataset
            region_of_interest = img[top-25:bottom+25, left-25:right+25]
            if region_of_interest is not None:
                update_image_dataset(region_of_interest)

    cv2.imshow('Human Face Recognition', img)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to exit the loop
        break

cap.release()
cv2.destroyAllWindows()