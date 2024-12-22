# from .Barcode_Scanning import start_b_scanning
import cv2
import pickle
import face_recognition
from datetime import datetime

def load_known_faces():
    with open("face_encodings.pkl", "rb") as file:
        data = pickle.load(file)
    return data

def start_face_recognition(barcode_data):
    # Load known faces and their corresponding roll numbers
    known_faces = load_known_faces()
    known_face_encodings = known_faces['encodings']
    known_face_ids = known_faces['roll_numbers']
    
    # Initialize the webcam
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        exit()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        rgb_small_frame = frame[:, :, ::-1]  # Convert the frame from BGR to RGB
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        # Check if any face is detected and match it with known faces
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

            name = "Unknown"  # Default name if no match
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_ids[first_match_index]
                print(f"Matched Face: {name}")
                
                # Compare with the barcode data
                if name == barcode_data:
                    mark_attendance(name)
                    print(f"Attendance Marked for {name}")
                else:
                    print("Face and Barcode do not match!")

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display the result
        cv2.imshow("Face Recognition", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

def mark_attendance(student_id):
    # Current date and time
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Check if attendance file exists, if not create it
    import os
    import csv
    if not os.path.exists('attendancelist.csv'):
        with open('attendancelist.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['id', 'time', 'session', 'status'])  # Writing headers

    # Append student attendance to the CSV file
    with open('attendancelist.csv', 'a', newline='') as file:
        writer = csv.writer(file)
        session = 'Morning'  # This could be dynamically set based on time of day
        status = 'Present'
        writer.writerow([student_id, current_time, session, status])

    print(f"Attendance for {student_id} marked as Present.")
