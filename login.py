from customtkinter import *
import sqlite3
from PIL import Image, ImageTk
from tkinter import messagebox
from datetime import datetime

root = CTk()
root.title("Login")
root.geometry("700x450")
root.resizable(0, 0)


# Connect to SQLite database
conn = sqlite3.connect('management.db')
c = conn.cursor()

# Create the login table again with the correct schema
c.execute("""CREATE TABLE IF NOT EXISTS login(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT,
                password TEXT)""")
#Register function
def register():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username already exists
    c.execute("SELECT * FROM login WHERE username=?", (username,))
    user = c.fetchone()
    if username == "" or password == "":
        messagebox.showerror("Error", "All the fields are required")
    else:
        if user:
            messagebox.showinfo("", "Username already exists. Please Login")
        else:
            c.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User Registered Successfully")
        
# Login function
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username or password is empty
    if username == "" or password == "":
        messagebox.showerror("Error", "Both username and password are required to login.")
        return
    if username=="admin" or password=="admin123":
        root.destroy()
        import admin
        root.destroy()
          
    # Check if the username exists in the database
    c.execute("SELECT * FROM login WHERE username=?", (username,))
    user = c.fetchone()

    if user:
        # If user exists, verify password
        stored_id,stored_username, stored_password= user
        if password == stored_password:
            messagebox.showinfo("Login Success", f"Welcome back, {stored_username}!")
            employee_id = fetch_employee_id(username)
            root.destroy()  # Close the login window
            attendance_window(employee_id)  # Pass the employee_id to the attendance window
        else:
            messagebox.showerror("Error", "Incorrect password.")
    else:
        messagebox.showerror("Error", "Username not registered.Contact Admin to register.")
   
            

# Fetch employee_id based on the username
def fetch_employee_id(username):
    conn = sqlite3.connect('management.db')  # Ensure using the correct database
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM login WHERE username=?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None


def create_attendance_table():
    conn = sqlite3.connect('management.db')
    cursor = conn.cursor()
    cursor.execute(''' 
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER,
            date TEXT,
            time TEXT,
            status TEXT,
            FOREIGN KEY (employee_id) REFERENCES login(id)
        )
    ''')
    conn.commit()
    conn.close()

create_attendance_table()  

def fetch_employee_name(employee_id):
    """Fetch the employee's name from the database."""
    conn = sqlite3.connect('management.db')  # Connect to the database
    cursor = conn.cursor()
    try:
        cursor.execute('''SELECT name FROM Employees WHERE id = ?''', (employee_id,))
        employee_name = cursor.fetchone()
        if employee_name:
            return employee_name[0]  # Return the name if found
        else:
            return None  # Return None if no employee found
    except sqlite3.Error as e:
        print(f"Error fetching employee name: {e}")
        return None
    finally:
        conn.close()

# Attendance window for marking attendance
def attendance_window(employee_id):
    # Fetch employee name based on the employee ID
    employee_name = fetch_employee_name(employee_id)
    
    if employee_name is None:
        # Show an error if the employee name couldn't be fetched
        messagebox.showerror("Error", f"No employee found with ID {employee_id}.")
        return  # Exit the function early if there's no employee name
    
    # Create the attendance window
    window = CTk()
    window.title("Mark Attendance")
    window.geometry("700x450")
    window.resizable(0, 0)
    window.configure(fg_color="#FFFFFF")


    # Title label for the window
    title_label = CTkLabel(window, text="Attendance Marking", font=("Poppins", 20, "bold"), text_color="navy blue")
    title_label.grid(row=0, column=0, columnspan=2, pady=(20, 15))

    # Center the employee ID and Name label
    label = CTkLabel(window, text=f"Employee ID: {employee_id} | Name: {employee_name}", 
                     font=("Helvetica", 14), text_color="#333333")
    label.grid(row=1, column=0, columnspan=2, pady=(5, 15))

    # Center the Present button with styling
    present_button = CTkButton(window, text="Mark as Present",  bg_color="#FAFAFA",fg_color="#000E65", cursor="hand2",font=("Helvetica", 12, "bold"), width=200, height=40,
                               command=lambda: mark_attendance(employee_id, "Present"))
    present_button.grid(row=2, column=0, columnspan=2, pady=(5, 18))

    # Center the Exit button with refined styling
    exit_button = CTkButton(window, text="Exit", bg_color="#FAFAFA",fg_color="#000E65", cursor="hand2", font=("Helvetica", 12, "bold"), width=200, height=40,
                            command=window.destroy)
    exit_button.grid(row=3, column=0, columnspan=2, pady=(8, 18))

    # Footer label at the bottom of the window
    footer_label = CTkLabel(window, text="Powered by HR Management System", font=("Helvetica", 13), text_color="#888888")
    footer_label.grid(row=4, column=0, columnspan=2, pady=8)

    # Adjust row and column weight to ensure centering
    window.grid_rowconfigure(0, weight=1)
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=1)
    window.grid_rowconfigure(4, weight=1)

    window.grid_columnconfigure(0, weight=1)
    window.grid_columnconfigure(1, weight=1)

    window.mainloop()

# Mark attendance in the database



# Open and resize image
cover_image = CTkImage(Image.open(r"C:\Users\LENOVO\Desktop\project\cover.png"), size=(700, 450))
cover_image_lbl = CTkLabel(root, image=cover_image, text=" ")
cover_image_lbl.place(x=0, y=0)

# Heading
heading_label = CTkLabel(root, text="Employee Management System", bg_color="#FAFAFA", font=("Poppins", 17, "bold"), text_color="#000E65")
heading_label.place(x=6, y=70)

# Username and Password Entry
username_entry = CTkEntry(root, placeholder_text="Enter your username", fg_color="#FAFAFA", bg_color="#FAFAFA", width=180, text_color="navy blue", border_color="dark blue")
username_entry.place(x=20, y=130)

password_entry = CTkEntry(root, placeholder_text="Enter your password", fg_color="#FAFAFA", bg_color="#FAFAFA", width=180, show='*', text_color="navy blue", border_color="dark blue")
password_entry.place(x=20, y=180)

# Login Button
login_button = CTkButton(root, text="Login", bg_color="#FAFAFA",fg_color="#000E65", cursor="hand2", command=login_user)
login_button.place(x=30, y=230)

# Register Button
register_button = CTkButton(root, text="Create Account", bg_color="#FAFAFA",fg_color="#000E65",cursor="hand2", command=register)
register_button.place(x=30, y=270)

root.mainloop()
