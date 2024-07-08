import cv2
import face_recognition
import numpy as np
video_capture = cv2.VideoCapture(0)

known_faces = []
known_face_ids = []
next_person_id = 1

while True:
    ret, frame = video_capture.read()
    
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, known_face_locations = face_locations)
    
    for face in face_encodings:
        match = face_recognition.compare_faces(known_faces, face)
        
        if True in match:
            match_index = match.index(True)
            person_id = known_face_ids[match_index]
        else:
            person_id = next_person_id
            next_person_id += 1

            known_faces.append(face)
            known_face_ids.append(person_id)
        index = None
        for i, encoding in enumerate(face_encodings):
            if np.array_equal(face, encoding):
                index = i
                break
        top, right, bottom, left = face_locations[index]
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        cv2.putText(frame, f'Person {person_id}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
