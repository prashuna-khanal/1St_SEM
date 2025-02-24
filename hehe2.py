from customtkinter import *
import subprocess
from tkinter import messagebox

# Main Dashboard Window
root = CTk()
root.title("Employee Management Dashboard")
root.geometry("700x450")

# Function to open employee details (calls babita.py)
def open_employee_details():
    try:
        subprocess.run(['python', 'babita.py'], check=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open Employee Details: {e}")

# Function to open payroll details
def open_payroll():
    # This would be another function to open payroll page, similar to above.
    pass

# Buttons for navigation
employee_button = CTkButton(root, text="Employee Detail", command=open_employee_details, fg_color="#005C97", cursor="hand2")
employee_button.place(x=30, y=100)

payroll_button = CTkButton(root, text="Payroll", command=open_payroll, fg_color="#005C97", cursor="hand2")
payroll_button.place(x=30, y=200)

# Main loop
root.mainloop()
