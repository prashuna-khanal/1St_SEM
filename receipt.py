import tkinter as tk
from tkinter import messagebox
import sqlite3

def fetch_employee_details(employee_id):
    """Fetch employee details from the database based on employee_id."""
    try:
        conn = sqlite3.connect('management.db')  # Assuming you're using SQLite for the employee database
        cursor = conn.cursor()
        
        cursor.execute("SELECT name, role, gender, salary, status FROM Employees WHERE id = ?", (employee_id,))
        employee = cursor.fetchone()

        conn.close()

        if employee:
            employee_name, role, gender, salary, status = employee
            return employee_name, role, gender, salary, status
        else:
            return None, None, None, None, None

    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"An error occurred while fetching employee details: {e}")
        return None, None, None, None, None

def generate_salary_receipt(employee_id, employee_name, role, gender, salary, status, allowances, deductions, net_salary, month, year):
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
    
    tk.Label(receipt_window, text=f"Salary: Rs.{salary:.2f}", font=("Arial", 12)).pack(pady=5)
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
        employee_name, role, gender, salary, status = fetch_employee_details(employee_id)

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

        # Call the function to generate and display the salary receipt
        generate_salary_receipt(employee_id, employee_name, role, gender, salary, status, allowances, deductions, net_salary, month, year)

    except ValueError:
        # Handle case where the user enters invalid input
        messagebox.showerror("Input Error", "Please enter valid numbers for salary components.")

def on_employee_id_entry_change(*args):
    """Update employee details automatically when employee_id changes."""
    employee_id = entry_employee_id.get()
    if employee_id.isdigit():  # Check if the entered value is a valid ID
        employee_name, role, gender, salary, status = fetch_employee_details(employee_id)
        if employee_name:
            entry_employee_name.delete(0, tk.END)
            entry_employee_name.insert(0, employee_name)
            entry_role.delete(0, tk.END)
            entry_role.insert(0, str(role))
            entry_gender.delete(0, tk.END)
            entry_gender.insert(0, gender)
            entry_salary.delete(0, tk.END)
            entry_salary.insert(0, str(salary))
        else:
            # Clear the fields if no employee is found
            entry_employee_name.delete(0, tk.END)
            entry_role.delete(0, tk.END)
            entry_gender.delete(0, tk.END)
            entry_salary.delete(0, tk.END)

# Create the main Tkinter window
root = tk.Tk()
root.title("Salary Receipt Generator")
root.geometry("400x500")

# Create the input fields and labels
tk.Label(root, text="Employee ID:",fg="#000E65").grid(row=0, column=0, padx=10, pady=5)
entry_employee_id = tk.Entry(root)
entry_employee_id.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Employee Name:",fg="#000E65").grid(row=1, column=0, padx=10, pady=5)
entry_employee_name = tk.Entry(root)
entry_employee_name.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Role:",fg="#000E65").grid(row=2, column=0, padx=10, pady=5)
entry_role = tk.Entry(root)
entry_role.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Gender:",fg="#000E65").grid(row=3, column=0, padx=10, pady=5)
entry_gender = tk.Entry(root)
entry_gender.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Salary:",fg="#000E65").grid(row=5, column=0, padx=10, pady=5)
entry_salary = tk.Entry(root)
entry_salary.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Allowances:",fg="#000E65").grid(row=6, column=0, padx=10, pady=5)
entry_allowances = tk.Entry(root)
entry_allowances.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Deductions:",fg="#000E65").grid(row=7, column=0, padx=10, pady=5)
entry_deductions = tk.Entry(root)
entry_deductions.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Month:",fg="#000E65").grid(row=8, column=0, padx=10, pady=5)
entry_month = tk.Entry(root)
entry_month.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="Year:",fg="#000E65").grid(row=9, column=0, padx=10, pady=5)
entry_year = tk.Entry(root)
entry_year.grid(row=9, column=1, padx=10, pady=5)

# Bind the employee ID entry to automatically fetch and populate details
entry_employee_id.bind("<KeyRelease>", on_employee_id_entry_change)

# Generate Receipt Button
btn_generate = tk.Button(root, text="Generate Receipt", command=generate_receipt,fg="#000E65")
btn_generate.grid(row=10, column=0, columnspan=2, pady=20)

# Run the Tkinter event loop
root.mainloop()
