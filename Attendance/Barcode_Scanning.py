import cv2
from pyzbar.pyzbar import decode  


def  start_b_scanning():
    cap = cv2.VideoCapture(1)  

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        exit()
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break
        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type
            print(f"Data: {barcode_data}, Type: {barcode_type}")

        cv2.imshow("Barcode Scanning (iVCam)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

