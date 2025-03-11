# main.py
from Barcode_Scanning import start_b_scanning
from face_scannig import start_face_recognition
import time

if __name__ == "__main__":
    print("Starting Barcode Scanning...")
    barcode_id = start_b_scanning()  # Get barcode data (student ID)

    if barcode_id:
        print(f"Barcode ID scanned: {barcode_id}")
        print("Starting Face Recognition...")
        start_face_recognition(barcode_id)  # Start face recognition with barcode data
