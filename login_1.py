from customtkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox

root = CTk()
root.title("Login")
root.geometry("700x450")
root.resizable(0, 0)

# Connect to SQLite database
conn = sqlite3.connect('management.db')
c = conn.cursor()

c.execute("""CREATE TABLE IF NOT EXISTS login(id INTEGER PRIMARY KEY AUTOINCREMENT, username text, password text)""")
conn.commit()

#register
def register():
    username = username_entry.get()
    password = password_entry.get()

    # Check if the username already exists
    c.execute("SELECT * FROM login WHERE username=?", (username,))
    user = c.fetchone()
    if username=="" or password=="":
        messagebox.showerror("Error","All the fields are required")
    else:
        if user:
            messagebox.showinfo("","Username already exists.Please Login")
        else:
            c.execute("INSERT INTO login (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "User Registered Successfully")
        username_entry.delete(0, END)
        password_entry.delete(0, END)

#LOGIN
def login_user():
    username = username_entry.get()
    password = password_entry.get()

    # Check if username or password is empty
    if username == "" or password == "":
        messagebox.showerror("Error", "Both username and password are required to login.")
        return

    # Check if the username exists in the database
    c.execute("SELECT * FROM login WHERE username=?", (username,))
    user = c.fetchone()

    if user:
        # If user exists, verify password
        stored_username, stored_password= user
        if password == stored_password:
            messagebox.showinfo("Login Success", f"Welcome back, {stored_username}!")
        else:
            messagebox.showerror("Error", "Incorrect password.")
    else:
        messagebox.showerror("Error", "Username not found. Please register first.")
    username_entry.delete(0, END)
    password_entry.delete(0, END)


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

register_button = CTkButton(root, text="Create Account", bg_color="#FAFAFA",fg_color="#351676",cursor="hand2", command=register)
register_button.place(x=30, y=270)

root.mainloop()
