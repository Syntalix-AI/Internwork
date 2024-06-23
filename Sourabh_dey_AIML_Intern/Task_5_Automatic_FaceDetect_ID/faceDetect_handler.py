# importing the necessary libraries
import cv2
import time
import os
from deepface import DeepFace as dfc
import pandas as pd
import random
import shutil

# Initialize the webcam
vid = cv2.VideoCapture(0)

if not vid.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Load the pre-trained Haar cascade classifier for face detection
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Flag to indicate if the face is properly detected inside the rectangle
face_detected = False

# Time when the face was detected inside the rectangle
start_time = time.time()  # Initialize start_time outside the loop

while True:
    # Capture a single frame
    ret, frame = vid.read()

    if not ret:
        print("Error: Could not read frame.")
        break

    # Convert the frame to grayscale (Haar cascades work better on grayscale images)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    for (x, y, w, h) in faces:
        # Draw a rectangle around the detected face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        
        # Display a message
        cv2.putText(frame, "Face Detected", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

        # Set face_detected flag to True when face is detected inside the rectangle
        if not face_detected and x > 0 and y > 0:
            face_detected = True
            start_time = time.time()  # Record the time when face is detected

    # Display the countdown timer
    if face_detected:
        remaining_time = max(0, 4 - int(time.time() - start_time))
        cv2.putText(frame, f"Time remaining: {remaining_time}s", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "No face detected", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Display the resulting frame
    cv2.imshow("Webcam Feed", frame)

    # Check if 4 seconds have passed and the face is detected properly inside the rectangle
    if face_detected and time.time() - start_time >= 4:
        # Save only the face region as an image
        face_roi = frame[y:y+h, x:x+w]  # Crop the face region
        #cv2.imwrite("detected/detected_face.jpg", face_roi)  # Save only the face part by cropping
        cv2.imwrite("detected/detected_face.jpg", frame) # for saving the whole image
        print("\n\t\tImage Detected successfully.")
        time.sleep(2)
        print("\n\t\tImage scanning started\n")
        time.sleep(5)

        # Path to the reference image for comparison
        reference_img_path = 'detected/detected_face.jpg'

        # Folder containing images to be verified
        folder_path = 'db/'

        # List of file extensions to check
        extensions = ('.jpg', '.jpeg', '.png')

        # Counter to track the number of verified images
        count = 0
        paths = []  # Initialize an empty list to store image paths

        # Loop through the folder to verify each image
        for fname in os.listdir(folder_path):
            if fname.lower().endswith(extensions):
                img_path = os.path.join(folder_path, fname)
                if os.path.isfile(img_path):
                    resp = dfc.verify(img1_path=reference_img_path, img2_path=img_path, enforce_detection=False)
                    if resp['verified']:
                        count += 1
                        paths.append(img_path)

        if count > 0:
            # Extract filenames from the image paths in ids list
            image_names = [os.path.basename(img_path) for img_path in paths]
            
            # Extract IDs from image names
            image_ids = [name.split(".")[0] for name in image_names]

            # Create a Pandas DataFrame with locations and IDs
            data = {'ID': image_ids,'Location': paths}
            df = pd.DataFrame(data)
            
            # Print the DataFrame
            cv2.putText(frame, "Face is present in Database", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            print("\n\t\tFace is present in Database with locations and IDs:\n")
            print(df)
            time.sleep(3)
            break
        if count == 0:
            # Generate a random 4-digit ID
            new_id = str(random.randint(1000, 9999))

            # Construct the new image filename with the random ID
            new_img_filename = new_id + '.jpg'

            # Copy the face region to the database folder with the new filename
            new_img_path = os.path.join(folder_path, new_img_filename)
            cv2.imwrite(new_img_path, face_roi)  # Save only the face part with the new ID
            print("\n\t\tFace is not present in Database\n")
            print(f"\t\tAssigned unique ID {new_id} and saved to database")
            print("\n\t\tUpdated Database Successfully\n")
            #print(df)

            # Show message on OpenCV window
            cv2.putText(frame, "Assigned unique ID and saved to database", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            time.sleep(3)
            break

    # Check if no face is detected and close the window after 5 seconds
    if not face_detected and time.time() - start_time > 5:
        print("No face detected. Closing window.")
        break

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object
vid.release()
cv2.destroyAllWindows()
