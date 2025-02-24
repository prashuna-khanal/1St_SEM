import sqlite3
def create_table():
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()
    cursor.execute('''
                        CREATE TABLE IF NOT EXISTS Employees (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT ,
                        role INTEGER ,
                        gender TEXT ,
                        salary REAL NOT NULL,
                        status TEXT
                    )''')
    conn.commit()
    conn.close()

def fetch_employees():
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Employees")
    employees = cursor.fetchall()
    conn.close()
    return employees

def insert_employee(id,name,role,gender,salary,status):
    conn=sqlite3.connect("management.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Employees (id,name,role,gender,salary,status) VALUES (?,?,?,?,?,?)",
    (id,name,role,gender,salary,status))
    conn.commit()
    conn.close()

def delete_employee(id):
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM employees WHERE id=?", (id,))
    conn.commit()
    conn.close()

def update_employee(new_name, new_role, new_gender, new_salary, new_status,id):
    conn = sqlite3.connect("management.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE Employees SET name=?, role=?, gender=?, salary=? ,status = ? WHERE id=?", 
    (new_name, new_role, new_gender, new_salary,new_status, id))
    conn.commit()
    conn.close()


# checking employee existence
def id_exists(id):
    conn=sqlite3.connect("management.db")
    cursor=conn.cursor()
    # 
    cursor.execute("SELECT COUNT(*) FROM Employees WHERE id = ?", (id,))
    result= cursor.fetchone()
    conn.close()
    # if we have an employee with a matching ID, the count will be equal to one which is geater than 0 , which is true
    return result[0]>0


def get_present_days(employee_id):
    conn = sqlite3.connect('management.db')
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM attendance WHERE employee_id=? AND status='Present'", (employee_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else 0




create_table()
print("success")