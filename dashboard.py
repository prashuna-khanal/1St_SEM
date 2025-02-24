from customtkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox
from datetime import datetime

root1 = CTk()
root1.title("Attendance")
root1.geometry("700x450")
root1.resizable(0, 0)

# Connect to SQLite database
conn = sqlite3.connect('employee_management.db')  # Make sure it's the correct database here
c = conn.cursor()

# DATABASE of attendance
def create_database():
    conn = sqlite3.connect('employee_management.db')  # Ensure using the correct database name
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,  # Added missing comma here between time and status
            status TEXT NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES login(id)
        )
    ''')

    conn.commit()
    conn.close()

# Marking attendance
def mark_attendance(employee_id, status):
    date = datetime.now().strftime('%Y-%m-%d')  # Get current date
    time = datetime.now().strftime('%H:%M:%S')  # Get current time in 24-hour format (HH:MM:SS)
    
    conn = sqlite3.connect('employee_management.db')  # Ensure using the correct database here
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO attendance (employee_id, date, time, status)  # Added 'time' in the insert statement
        VALUES (?, ?, ?, ?)
    ''', (employee_id, date, time, status))

    conn.commit()
    conn.close()

    # Show confirmation message
    messagebox.showinfo("Success", f"Attendance marked as {status} for {date} at {time}")

def attendance_window(employee_id):
    # Create the window
    window = CTk()
    window.title("Mark Attendance")

    # Display employee info (just the ID for now)
    label = CTk.Label(window, text=f"Employee ID: {employee_id}")
    label.grid(row=0, column=0, pady=10)  # Use grid instead of pack

    # Present button
    present_button = CTk.Button(window, text="Present", width=20, bg_color="#FAFAFA", fg_color="#000E65", cursor="hand2", command=lambda: mark_attendance(employee_id, "Present"))
    present_button.grid(row=1, column=0, pady=5)  # Use grid instead of pack

    # Absent button
    absent_button = CTk.Button(window, text="Absent", width=20, bg_color="#FAFAFA", fg_color="#000E65", cursor="hand2", command=lambda: mark_attendance(employee_id, "Absent"))
    absent_button.grid(row=2, column=0, pady=5)  # Use grid instead of pack

    # Exit button
    exit_button = CTk.Button(window, text="Exit", width=20, bg_color="#FAFAFA", fg_color="#000E65", cursor="hand2", command=window.destroy)
    exit_button.grid(row=3, column=0, pady=10)  # Use grid instead of pack

    window.mainloop()





attendance_window()
create_database()
root1.mainloop()

