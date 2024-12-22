import cv2
from pyzbar.pyzbar import decode

def start_b_scanning():
    cap = cv2.VideoCapture(1)  # Adjust index if necessary

    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        exit()

    print("Press 'q' to exit the scanner.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame. Exiting...")
            break

        barcodes = decode(frame)
        for barcode in barcodes:
            barcode_data = barcode.data.decode('utf-8')
            barcode_type = barcode.type

            # Get position of the barcode
            (x, y, w, h) = barcode.rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.putText(frame, f"{barcode_data} ({barcode_type})", (x, y - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            print(f"Data: {barcode_data}, Type: {barcode_type}")

            # Save barcode data to a file
            with open("scanned_barcodes.txt", "a") as file:
                file.write(f"{barcode_data}, {barcode_type}\n")

        # Display the video feed
        cv2.imshow("Barcode Scanning (iVCam)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return barcode_data

