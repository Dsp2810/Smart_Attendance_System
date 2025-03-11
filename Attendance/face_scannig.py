import cv2
import pickle
import face_recognition
from datetime import datetime
import csv
import os
from Barcode_Scanning import start_b_scanning  # Assuming this function returns barcode data
from Attendance_marking import create_attendance_csv  # Assuming this function marks attendance in CSV

def load_known_faces_from_csv(csv_file):
    """Loads known face encodings and roll numbers from a CSV file."""
    known_face_encodings = []
    known_face_ids = []
    
    # Read the CSV file
    with open(csv_file, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            student_id = row['id']
            photo_path = row['photo']
            
            # Load the student's image
            if os.path.exists(photo_path):
                student_image = face_recognition.load_image_file(photo_path)
                student_face_encoding = face_recognition.face_encodings(student_image)
                
                if student_face_encoding:
                    known_face_encodings.append(student_face_encoding[0])  # Get the first face encoding
                    known_face_ids.append(student_id)
                else:
                    print(f"Warning: No face found in image {photo_path}")
            else:
                print(f"Warning: Image file not found: {photo_path}")
    
    return {'encodings': known_face_encodings, 'roll_numbers': known_face_ids}

def verify_face(recognized_name, barcode_data, known_face_encodings, known_face_ids):
    """Verifies the face for a match after barcode scanning."""
    if recognized_name == barcode_data:
        create_attendance_csv(recognized_name)  # Mark attendance if names match
        print(f"Attendance Marked for {recognized_name}")
        return True
    else:
        print("Mismatch between barcode and face. Please try again.")
        return False

def start_face_recognition(barcode_data):
    """Starts face recognition after barcode scanning and marks attendance."""
    # Load known faces and their corresponding roll numbers
    known_faces = load_known_faces_from_csv(r"C:\Users\Dhava\Documents\GitHub\Smart_Attendance_System\Attendance\datasheet.csv")  # Use the CSV file instead of .pkl
    known_face_encodings = known_faces['encodings']
    known_face_ids = known_faces['roll_numbers']
    
    # Initialize the webcam for face scanning
    cap = cv2.VideoCapture(1)
    
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        exit()

    attempts = 0
    recognized_name = "Unknown"

    while attempts < 2:  # Perform face recognition twice for verification
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
                recognized_name = name
                attempts += 1

            # Draw a rectangle around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Display the result
        cv2.imshow("Face Recognition", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    if attempts == 2:  # After two attempts, verify face with barcode data
        return verify_face(recognized_name, barcode_data, known_face_encodings, known_face_ids)
    else:
        print("Face recognition failed twice. Please try again.")
        return False

def start_process():
    """Starts the barcode scanning and then initiates face recognition."""
    while True:  # Loop for continuously scanning barcodes and recognizing faces
        # Start barcode scanning and get the scanned barcode data
        barcode_data = start_b_scanning()  # Assuming this function returns the barcode data
        print(f"Barcode Scanned: {barcode_data}")
        
        # After barcode scan, initiate face recognition
        if start_face_recognition(barcode_data):
            print("Attendance process completed.")
        else:
            print("Attendance marking failed. Please try again.")

# Start the entire process
start_process()
