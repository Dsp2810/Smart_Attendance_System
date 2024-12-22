import csv
from datetime import datetime

def create_attendance_csv(student_id, session='Morning'):
    # Current time and date
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Check if the CSV file exists, if not, create the file and write headers
    file_path = 'attendancelist.csv'
    try:
        with open(file_path, 'a', newline='') as file:
            writer = csv.writer(file)
            # Writing headers if the file is empty
            if file.tell() == 0:
                writer.writerow(['id', 'time', 'session', 'status'])  # headers

            # Writing the attendance record
            writer.writerow([student_id, current_time, session, 'Present'])
            print(f"Attendance for {student_id} marked as Present.")
    except Exception as e:
        print(f"Error: {e}")
