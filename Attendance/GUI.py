import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
from .Barcode_Scanning import start_b_scanning

class AttendanceSystemGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Attendance System")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f4")
        self.other_session_entry =None  
        self.main_menu()

    def main_menu(self):
        self.clear_window()
        self.title_label = tk.Label(
            self.root, text="Smart Attendance System", font=("Helvetica", 24, "bold"), bg="#f4f4f4", fg="#333"
        )
        self.title_label.pack(pady=20)

        self.nav_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.nav_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.nav_frame, text="Start Attendance", font=("Helvetica", 14), bg="#4caf50", fg="white", width=20, command=self.start_attendance
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.logs_button = tk.Button(
            self.nav_frame, text="View Logs", font=("Helvetica", 14), bg="#2196f3", fg="white", width=20, command=self.view_logs
        )
        self.logs_button.grid(row=0, column=1, padx=10)

        self.settings_button = tk.Button(
            self.nav_frame, text="Settings", font=("Helvetica", 14), bg="#ff9800", fg="white", width=20, command=self.settings
        )
        self.settings_button.grid(row=0, column=2, padx=10)

        self.footer_label = tk.Label(
            self.root, text="Developed by Dhaval Patel", font=("Helvetica", 10, "italic"), bg="#f4f4f4", fg="#888"
        )
        self.footer_label.pack(side=tk.BOTTOM, pady=10)

    def start_attendance(self):
        self.clear_window()

        header_label = tk.Label(
            self.root, text="Start Attendance", font=("Helvetica", 20, "bold"), bg="#f4f4f4", fg="#333"
        )
        header_label.pack(pady=20)

        self.form_frame = tk.Frame(self.root, bg="#f4f4f4")
        self.form_frame.pack(pady=20)
        
        tk.Label(self.form_frame, text="Class :", font=("Helvetica", 14), bg="#f4f4f4").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.class_var = tk.StringVar()
        subject_dropdown = ttk.Combobox(self.form_frame, textvariable=self.class_var, font=("Helvetica", 12), width=30)
        subject_dropdown['values'] = ("cse/div1/sem-2", "cse/div2/sem-2", "cse/div1/sem-4", "cse/div2/sem-4", "cse/div1/sem-6","cse/div2/sem-6")
        subject_dropdown.grid(row=0, column=1, pady=5)
        
        
        tk.Label(self.form_frame, text="Subject:", font=("Helvetica", 14), bg="#f4f4f4").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.subject_var = tk.StringVar()
        subject_dropdown = ttk.Combobox(self.form_frame, textvariable=self.subject_var, font=("Helvetica", 12), width=30)
        subject_dropdown['values'] = ("Mathematics", "Physics", "Chemistry", "AI Basics", "Programming")
        subject_dropdown.grid(row=0, column=1, pady=5)

        tk.Label(self.form_frame, text="Session Type:", font=("Helvetica", 14), bg="#f4f4f4").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.session_type_var = tk.StringVar()
        session_type_dropdown = ttk.Combobox(self.form_frame, textvariable=self.session_type_var, font=("Helvetica", 12), width=30)
        session_type_dropdown['values'] = ("Lecture", "Lab", "Others")
        session_type_dropdown.grid(row=1, column=1, pady=5)

        session_type_dropdown.bind("<<ComboboxSelected>>", self.on_session_type_select)

        tk.Label(self.form_frame, text="Start Time (HH:MM):", font=("Helvetica", 14), bg="#f4f4f4").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.start_time_entry = tk.Entry(self.form_frame, font=("Helvetica", 12), width=33)
        self.start_time_entry.grid(row=3, column=1, pady=5)

        tk.Label(self.form_frame, text="End Time (HH:MM):", font=("Helvetica", 14), bg="#f4f4f4").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.end_time_entry = tk.Entry(self.form_frame, font=("Helvetica", 12), width=33)
        self.end_time_entry.grid(row=4, column=1, pady=5)

        start_attendance_button = tk.Button(
            self.root, text="Start Attendance", font=("Helvetica", 14), bg="#4caf50", fg="white", command=self.process_attendance
        )
        start_attendance_button.pack(pady=20)

        back_button = tk.Button(
            self.root, text="Back", font=("Helvetica", 12), bg="#e0e0e0", fg="#333", command=self.main_menu
        )
        back_button.pack(pady=10)

    def on_session_type_select(self, event):
        selected_session = self.session_type_var.get()

    # Remove existing "Specify Session Type" label and entry if they exist
        if hasattr(self, "other_session_label"):
            self.other_session_label.grid_forget()
        if self.other_session_entry:
            self.other_session_entry.grid_forget()
    
    # If "Others" is selected, show the label and entry field
        if selected_session == "Others":
            self.other_session_label = tk.Label(
            self.form_frame, 
            text="Specify Session Type:", 
            font=("Helvetica", 14), 
            bg="#f4f4f4"
        )
        self.other_session_label.grid(row=2, column=0, sticky=tk.W, pady=5)

        if self.other_session_entry is None:
            self.other_session_entry = tk.Entry(
                self.form_frame, 
                font=("Helvetica", 12), 
                width=32
            )
        self.other_session_entry.grid(row=2, column=1, pady=5)
 

    def process_attendance(self):
        class_type  = self.class_var.get()
        subject = self.subject_var.get()
        session_type = self.session_type_var.get()
        start_time = self.start_time_entry.get()
        end_time = self.end_time_entry.get()

        if  not subject or not session_type or not start_time or not end_time:
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            datetime.strptime(start_time, "%H:%M")
            datetime.strptime(end_time, "%H:%M")
        except ValueError:
            messagebox.showerror("Error", "Invalid time format. Use HH:MM")
            return

        messagebox.showinfo("Success", f"Attendance started for {subject} ({session_type})\n{start_time} - {end_time}")
        start_b_scanning()

    def view_logs(self):
        self.clear_window()

        header_label = tk.Label(
            self.root, text="Attendance Logs", font=("Helvetica", 20, "bold"), bg="#f4f4f4", fg="#333"
        )
        header_label.pack(pady=20)

        logs_label = tk.Label(
            self.root, text="[Logs will be displayed here]", font=("Helvetica", 14), bg="#f4f4f4", fg="#555"
        )
        logs_label.pack(pady=50)

        back_button = tk.Button(
            self.root, text="Back", font=("Helvetica", 12), bg="#e0e0e0", fg="#333", command=self.main_menu
        )
        back_button.pack(pady=10)

    def settings(self):
        self.clear_window()

        header_label = tk.Label(
            self.root, text="Settings", font=("Helvetica", 20, "bold"), bg="#f4f4f4", fg="#333"
        )
        header_label.pack(pady=20)

        settings_label = tk.Label(
            self.root, text="[Settings options will be added here]", font=("Helvetica", 14), bg="#f4f4f4", fg="#555"
        )
        settings_label.pack(pady=50)

        back_button = tk.Button(
            self.root, text="Back", font=("Helvetica", 12), bg="#e0e0e0", fg="#333", command=self.main_menu
        )
        back_button.pack(pady=10)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    def start_b_scanning(self):
        start_b_scanning()
