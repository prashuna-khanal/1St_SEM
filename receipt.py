import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime

def fetch_salary(employee_id):
    """Fetch the salary of an employee based on employee_id."""
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()

    try:
        cursor.execute('''SELECT salary FROM Employees WHERE id = ?''', (employee_id,))
        salary = cursor.fetchone()  # Fetch the result

        if salary:
            return salary[0]  # Return the salary value (first item in tuple)
        else:
            return None  # Return None if no record is found
    except sqlite3.Error as e:
        print(f"Error fetching salary: {e}")
        return None
    finally:
        conn.close()

def count_present_days(employee_id):
    """Count how many times 'Present' is marked for the employee."""
    conn = sqlite3.connect('management.db')  # Connect to the database
    cursor = conn.cursor()

    try:
        cursor.execute('''
            SELECT COUNT(*) FROM Attendance
            WHERE employee_id = ? AND status = 'Present'
        ''', (employee_id,))
        present_count = cursor.fetchone()[0]  # Fetch the result and get the count
        return present_count
    except sqlite3.Error as e:
        print(f"Error counting present days: {e}")
        return 0
    finally:
        conn.close()





def fetch_employee_details(employee_id):
    """Fetch employee details from the database based on employee_id."""
    try:
        conn = sqlite3.connect('management.db')  # Assuming you're using SQLite for the employee database
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, role, gender, salary FROM Employees WHERE id = ?", (employee_id,))
        employee = cursor.fetchone()

        conn.close()

        if employee:
            employee_name, role, gender, salary = employee
            return employee_name, role, gender, salary
        else:
            return None, None, None, None, None

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching employee details: {e}")
        return None, None, None, None, None

def generate_salary_receipt(employee_id, employee_name, role, gender, total_salary, status, allowances, deductions, net_salary, month, year):
    """Generate and display the salary receipt in the Tkinter window."""
    
    # Create a new window for the receipt
    receipt_window = tk.Toplevel(root)
    receipt_window.title("Salary Receipt")
    receipt_window.geometry("400x500")
    
    
    # Add labels to the receipt window
    receipt_label = tk.Label(receipt_window, text=f"Salary Receipt for {employee_name} ({employee_id})", font=("Arial", 14, "bold"))
    receipt_label.pack(pady=10)

    tk.Label(receipt_window, text=f"Role: {role}", font=("Arial", 12)).pack(pady=5)
    tk.Label(receipt_window, text=f"Gender: {gender}", font=("Arial", 12)).pack(pady=5)
    tk.Label(receipt_window, text=f"Status: {status}", font=("Arial", 12)).pack(pady=5)
    tk.Label(receipt_window, text=f"Month: {month}, {year}", font=("Arial", 12)).pack(pady=5)

    tk.Label(receipt_window, text="===================================", font=("Arial", 10, "italic")).pack(pady=5)
    
    tk.Label(receipt_window, text=f"Salary: Rs.{total_salary:.2f}", font=("Arial", 12)).pack(pady=5)
    tk.Label(receipt_window, text=f"Allowances: Rs.{allowances:.2f}", font=("Arial", 12)).pack(pady=5)
    tk.Label(receipt_window, text=f"Deductions: Rs.{deductions:.2f}", font=("Arial", 12)).pack(pady=5)
    
    tk.Label(receipt_window, text="====================================", font=("Arial", 10, "italic")).pack(pady=5)
    
    tk.Label(receipt_window, text=f"Net Salary: Rs.{net_salary:.2f}", font=("Arial", 12, "bold")).pack(pady=10)
    
    tk.Label(receipt_window, text="This is a system-generated salary receipt. No signature required.", font=("Arial", 10, "italic")).pack(pady=10)
     
    # receipt_window.destroy()
def generate_receipt():
    """Function to collect data and generate the receipt in a new window."""
    try:
        # Collect data from the Tkinter fields
        employee_id = entry_employee_id.get()
        
        # Fetch employee details based on the entered Employee ID
        employee_name, role, gender, salary = fetch_employee_details(employee_id)

        if not employee_name:
            messagebox.showerror("Employee Not Found", "No employee found with this ID.")
            return

        # Collect allowances and deductions
        allowances = float(entry_allowances.get())
        deductions = float(entry_deductions.get())
        
        # Calculate net salary
        net_salary = salary + allowances - deductions
        
        month = entry_month.get()
        year = entry_year.get()

        # Check if both month and year are provided
        if not month or not year:
            messagebox.showerror("Input Error", "Please enter both month and year.")
            return

        # Call the function to generate and display the salary receipt
        generate_salary_receipt(employee_id, employee_name, role, gender, salary, "Present", allowances, deductions, net_salary, month, year)

    except ValueError:
        # Handle case where the user enters invalid input
        messagebox.showerror("Input Error", "Please enter valid numbers for salary components.")
        
def on_employee_id_entry_change(*args):
    """Update employee details and calculate salary automatically when employee_id changes."""
    employee_id = entry_employee_id.get()
    if employee_id.isdigit():  # Check if the entered value is a valid ID
        # Fetch employee details (name, role, salary, etc.)
        employee_name, role, gender, salary = fetch_employee_details(employee_id)
        if employee_name:
            # Update the entry fields
            entry_employee_name.delete(0, tk.END)
            entry_employee_name.insert(0, employee_name)
            entry_role.delete(0, tk.END)
            entry_role.insert(0, str(role))
            entry_gender.delete(0, tk.END)
            entry_gender.insert(0, gender)
            entry_base_salary.delete(0, tk.END)
            entry_base_salary.insert(0, str(salary))
            
            # Count the number of present days
            present_days = count_present_days(employee_id)
            entry_present.delete(0, tk.END)  # Clear previous value
            entry_present.insert(0, str(present_days))  # Insert present days
            
            # Calculate the total salary based on the number of present days
            total_salary = salary * present_days
            entry_salary.delete(0, tk.END)  # Clear previous value
            entry_salary.insert(0, str(total_salary))  # Insert total salary
        else:
            # Clear the fields if no employee is found
            entry_employee_name.delete(0, tk.END)
            entry_role.delete(0, tk.END)
            entry_gender.delete(0, tk.END)
            entry_base_salary.delete(0, tk.END)
            entry_present.delete(0, tk.END)
            entry_salary.delete(0, tk.END)

# Create the main Tkinter window
root = tk.Tk()
root.title("Salary Receipt Generator")
root.geometry("400x500")

# Create the input fields and labels
tk.Label(root, text="Employee ID:", fg="#000E65").grid(row=0, column=0, padx=10, pady=5)
entry_employee_id = tk.Entry(root)
entry_employee_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Employee Name:", fg="#000E65").grid(row=1, column=0, padx=10, pady=5)
entry_employee_name = tk.Entry(root)
entry_employee_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Role:", fg="#000E65").grid(row=2, column=0, padx=10, pady=5)
entry_role = tk.Entry(root)
entry_role.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Gender:", fg="#000E65").grid(row=3, column=0, padx=10, pady=5)
entry_gender = tk.Entry(root)
entry_gender.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Base Salary:", fg="#000E65").grid(row=4, column=0, padx=10, pady=5)  # Fixed row index for Base Salary
entry_base_salary = tk.Entry(root)
entry_base_salary.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="No. of Present days:", fg="#000E65").grid(row=5, column=0, padx=10, pady=5)  # Fixed row index for Present Days
entry_present = tk.Entry(root)
entry_present.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Salary:", fg="#000E65").grid(row=6, column=0, padx=10, pady=5)  # Fixed row index for Salary
entry_salary = tk.Entry(root)
entry_salary.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Allowances:", fg="#000E65").grid(row=7, column=0, padx=10, pady=5)  # Fixed row index for Allowances
entry_allowances = tk.Entry(root)
entry_allowances.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Deductions:", fg="#000E65").grid(row=8, column=0, padx=10, pady=5)  # Fixed row index for Deductions
entry_deductions = tk.Entry(root)
entry_deductions.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="Month:", fg="#000E65").grid(row=9, column=0, padx=10, pady=5)  # Fixed row index for Month
entry_month = tk.Entry(root)
entry_month.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="Year:", fg="#000E65").grid(row=10, column=0, padx=10, pady=5)  # Fixed row index for Year
entry_year = tk.Entry(root)
entry_year.grid(row=10, column=1, padx=10, pady=5)


# Bind the employee ID entry to automatically fetch and populate details
entry_employee_id.bind("<KeyRelease>", on_employee_id_entry_change)

# Generate Receipt Button
btn_generate = tk.Button(root, text="Generate Receipt", command=generate_receipt,fg="#000E65")
btn_generate.grid(row=11, column=0, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()
