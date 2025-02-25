from operator import add
from select import select
import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import database
import subprocess

# creating tkinter window
home=customtkinter.CTk()
home.title("Employee Management System")
home.geometry("700x500")
home.config(bg="#161C25")
# home.resizable(False,False)

# insering data 
def add_in_view():
    # fetching data from fetch_employees function of database.py
    employees=database.fetch_employees()
    # preventing to insert the same row multiple times
    tree.delete(*tree.get_children())
    # 
    for employee in employees:
        # 
        tree.insert('',END,values=employee)

# selecting the certain row and highlighting
def highlight(*clicked):
    if clicked:
        # remove highlight
            tree.selection_remove(tree.focus())
            # preventing data updation without selection
            tree.focus('')
    # 0 and END to indicate beginning and ending of the text in the entry box and delete it
    id_entry.delete(0,END)
    name_entry.delete(0,END)
    role_entry.delete(0,END)
    storing.set('Male')
    salary_entry.delete(0,END)
    status_entry.delete(0,END)

# showing data in entry boxes to update
def display_data(event):
    # event: wait for an event to occur i.e mouse cursor movement
    # if row selected highlight it
    selected=tree.focus()
    if selected:
        row=tree.item(selected)['values']
        # clear the highlighted row
        highlight()
        # insert new data 
        # inserting data from beginning in the expected row
        id_entry.insert(0,row[0])
        name_entry.insert(0,row[1])
        role_entry.insert(0,row[2])
        storing.set(row[3])
        salary_entry.insert(0,row[4])
        status_entry.insert(0,row[5])
    # if data remain same just pass the same data in else
    else:
        pass

# deleting data
def delete_data():
    selected=tree.focus()
    if not selected:
        messagebox.showerror("Error","Please select an employee to erase!!")
    else:
        id=id_entry.get()
        database.delete_employee(id)
        # fetching data 
        add_in_view()
        # check the row to be deleted and delete
        highlight()
        messagebox.showinfo("Success","Data has been deleted.")

# update data
def update_data():
    selected=tree.focus()
    if not selected:
        messagebox.showerror("Error","Select employee to update!!")
    else:
        id=id_entry.get()
        name=name_entry.get()
        role=role_entry.get()
        gender=storing.get()
        salary=salary_entry.get()
        status=status_entry.get()
        # updating to database
        database.update_employee(name,role,gender,salary,status,id)
        add_in_view()
        highlight()
        messagebox.showinfo("Success","Data has been updated.")


# displaying data using add employee button
def insert_data():
    id=id_entry.get()
    name=name_entry.get()
    role=role_entry.get()
    gender=storing.get()
    salary=salary_entry.get()
    status=status_entry.get()
    # conditions
    if not (id and name and role and gender and salary and status):
        messagebox.showerror("Error","All fields are required!!")
        # fetching id from id_exists function from databae.py
    elif database.id_exists(id):
        messagebox.showerror("Error","ID already exists!!")
    else:
        database.insert_employee(id,name,role,gender,salary,status)
        add_in_view()
        highlight()
        messagebox.showinfo("Success","Data has been successfully inserted.")


# Define the function to go to the salary receipt page
def payroll():
    import receipt


# Define the function to go back to the login page
def back_to_login():
    subprocess.Popen(["python", "login.py"])  # Run the login page script (login.py)
    home.destroy()  # Close the current window


# adding fonts used overall
font1=("Arial",16,"bold")
font2=("Arial",12,"bold")

# id
id_label=customtkinter.CTkLabel(home,font=font1,text='ID:',text_color='#fff',bg_color='#161C25')
id_label.place(x=20,y=20)

id_entry = customtkinter.CTkEntry(home,font=font1,text_color='#000',fg_color='#fff',border_color='#0C9295',border_width=2,width=120)
id_entry.place(x=100,y=20)

# name
name_label=customtkinter.CTkLabel(home,font=font1,text='Name:',text_color='#fff',bg_color='#161C25')
name_label.place(x=20,y=80)

name_entry = customtkinter.CTkEntry(home,font=font1,text_color='#000',fg_color='#fff',border_color='#0C9295',border_width=2,width=120)
name_entry.place(x=100,y=80)

# role
role_label=customtkinter.CTkLabel(home,font=font1,text='Role:',text_color='#fff',bg_color='#161C25')
role_label.place(x=20,y=140)

role_entry = customtkinter.CTkEntry(home,font=font1,text_color='#000',fg_color='#fff',border_color='#0C9295',border_width=2,width=120)
role_entry.place(x=100,y=140)

# gender
gender_label=customtkinter.CTkLabel(home,font=font1,text='Gender:',text_color='#fff',bg_color='#161C25')
gender_label.place(x=20,y=200)
# gender options
options = ["Male","Female"]
storing=StringVar()
gender_option=customtkinter.CTkComboBox(home,font=font1,text_color='#000',button_color='#0C9295',button_hover_color='#0C9295',fg_color='#fff',dropdown_hover_color='#0C9295',border_color='#0C9295',width=120,variable=storing,values=options,state='readonly')
# first appearing gender
gender_option.set('Male')
gender_option.place(x=100,y=200)

# salary
salary_label=customtkinter.CTkLabel(home,font=font1,text='Salary:',text_color='#fff',bg_color='#161C25')
salary_label.place(x=20,y=260)

salary_entry = customtkinter.CTkEntry(home,font=font1,text_color='#000',fg_color='#fff',border_color='#0C9295',border_width=2,width=120)
salary_entry.place(x=100,y=260)

# active status of employee
status_label=customtkinter.CTkLabel(home,font=font1,text='Status:',text_color='#fff',bg_color='#161C25')
status_label.place(x=20,y=320)

status_entry = customtkinter.CTkEntry(home,font=font1,text_color='#000',fg_color='#fff',border_color='#0C9295',border_width=2,width=120)
status_entry.place(x=100,y=320)

# adding buttons
add_button=customtkinter.CTkButton(home,font=font1,text_color='#fff',text='Add Employee',command=insert_data,fg_color='#05A312',hover_color='#00850B',bg_color='#161C25',border_color='',cursor='hand2',corner_radius=10)
add_button.place(x=15,y=390)
 
clear_button=customtkinter.CTkButton(home,font=font1,text_color='#fff',command=lambda:highlight(True),text='New Employee',fg_color='#05A312',hover_color='#00850B',bg_color='#161C25',border_color='',cursor='hand2',border_width=2,corner_radius=10)
clear_button.place(x=180,y=390)

update_button=customtkinter.CTkButton(home,font=font1,command=update_data,text_color='#fff',text='Update Employee',fg_color='#05A312',hover_color='#00850B',bg_color='#161C25',border_color='',border_width=2,corner_radius=10)
update_button.place(x=350,y=390)

delete_button=customtkinter.CTkButton(home,font=font1,command=delete_data,text_color='#fff',text='Delete Employee',fg_color='#05A312',hover_color='#00850B',border_color='',cursor='hand2',border_width=2,corner_radius=10)
delete_button.place(x=540,y=390)

payroll_button = customtkinter.CTkButton(home,font=font1,text_color='#fff',text='Salary receipt',fg_color='#05A312',hover_color='#00850B',border_color='',cursor='hand2',border_width=2,corner_radius=10, command=payroll)                                           
payroll_button.place(x=160, y=455)

back_button = customtkinter.CTkButton(home, font=font1, text_color='#fff', text='Back to Login',fg_color='#05A312', hover_color='#00850B',bg_color='#161C25', border_color='', cursor='hand2',border_width=2, corner_radius=10, command=back_to_login)
back_button.place(x=360, y=455)  


# creating a view page i.e employee data using tree
view=ttk.Style(home)
# setting interface theme
view.theme_use("clam")
view.configure("Treeview",font=font2,foreground='#fff',background='#000',fieldbackground='#313837')
# knowing selected rows state using map 
view.map('Treeview',background=[('selected','#1A8F2D')])

tree=ttk.Treeview(home,height=15)
tree['columns']=('ID','Name','Role','Gender','Salary','Status')

# styling colums 
# HIDINGG THE FIRST DEFAULT COLUMN
tree.column('#0',width=0,stretch=tk.NO)
# centering column using anchor
tree.column('ID',anchor=tk.CENTER,width=70)
tree.column('Name',anchor=tk.CENTER,width=100)
tree.column('Role',anchor=tk.CENTER,width=100)
tree.column('Gender',anchor=tk.CENTER,width=100)
tree.column('Salary',anchor=tk.CENTER,width=100)
tree.column('Status',anchor=tk.CENTER,width=100)

# setting the heading of each column
tree.heading('ID',text='ID')
tree.heading('Name',text='NAME')
tree.heading('Role',text='ROLE')
tree.heading('Gender',text='GENDER')
tree.heading('Salary',text='SALARY')
tree.heading('Status',text='STATUS')

tree.place(x=295,y=50)

# if clicking in table, this function will be executed to trigger selected row
tree.bind('<ButtonRelease-1>',display_data)

add_in_view()
home.mainloop()