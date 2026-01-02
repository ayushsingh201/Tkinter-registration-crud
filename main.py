from tkinter import *
from tkinter import messagebox,ttk
import pyodbc
import re

conn = pyodbc.connect(
    'Driver={SQL Server};'
    'Server=LAPTOP-P8F0HK55;'   
    'Database=RegistrationDB;'
    'Trusted_Connection=yes;'
)
cursor = conn.cursor()
screen = Tk()
screen.geometry("600x500")
screen.resizable(False, False)

# ----------- Page 1 -----------
page1 = Frame(screen,width=600,height=500,bg="lightblue")
page1.place(x=0, y=0)
page1.pack_propagate(False)

Label(page1, text="Main Page",font="ariel 20 bold",bg="red",fg="white").pack(fill="both")
Button(page1, text="Crud Operation",font="20", command=lambda: show_page(page3)).place(x=210,y=100)
Button(page1, text="Registration Form",font="20", command=lambda: show_page(page2)).place(x=200,y=200)

# ----------- Page 2 -----------
page2 = Frame(screen,width=600, height=500,bg="lightblue")
page2.place(x=0, y=0)
page2.pack_propagate(False)

name_info=StringVar()
pass_info=StringVar()
gender_info=StringVar()
LabelFrame(page2,text="Registration form")
Label(page2,text="Registration form",font="ariel 20 bold",bg="red",fg="white").pack(fill="both")

Label(page2,text="User Name",font="20",bg="lightblue").place(x=100,y=70)
Label(page2,text="Password",font="20",bg="lightblue").place(x=100,y=115)
Label(page2,text="Gender",font="20",bg="lightblue").place(x=100,y=160)
Label(page2,text="Phone Number",font="20",bg="lightblue").place(x=100,y=205)
Label(page2,text="E-mail",font="20",bg="lightblue").place(x=100,y=250)
Label(page2,text="Qualification",font="20",bg="lightblue").place(x=100,y=295)

name_entry=Entry(page2,font="10",bd=4,textvariable=name_info)
name_entry.place(x=250,y=70)
pass_entry=Entry(page2,font="10",bd=4,textvariable=pass_info,show="*")
pass_entry.place(x=250,y=115)

gender_info.set("Male")
gender_entry=Radiobutton(page2,text="Male",font="20",variable=gender_info,value="Male",bg="lightblue")
gender_entry.place(x=250,y=160)
gender_entry=Radiobutton(page2,text="Female",font="20",variable=gender_info,value="Female",bg="lightblue")
gender_entry.place(x=330,y=160)

phoneNumber_entry=Entry(page2,font="10",bd=4)
phoneNumber_entry.place(x=250,y=205)

Email_entry=Entry(page2,font="10",bd=4)
Email_entry.place(x=250,y=250)

choices=['10th','12th','UG','PG']

quali_dropdown=ttk.Combobox(page2, values=choices,font=("arial",15))
quali_dropdown.set("Select Qualification")
quali_dropdown.place(x=250,y=295)

def register_user():
    name = name_info.get().strip()
    password = pass_info.get().strip()
    gender = gender_info.get().strip()
    phone = phoneNumber_entry.get().strip()
    email = Email_entry.get().strip()
    qualification = quali_dropdown.get().strip()

    if not name.isalpha():
        messagebox.showerror("Error", "Username must contain only letters (A-Z).")
        return
    if not (re.search("[A-Za-z]", password) and re.search("[0-9]", password)):
        messagebox.showerror("Error", "Password must contain letters and numbers.")
        return
    if not phone.isdigit():
        messagebox.showerror("Error", "Phone number must contain digits only.")
        return
    if len(phone) != 10:
        messagebox.showerror("Error", "Phone number must be 10 digits.")
        return
    if "@" not in email or "." not in email:
        messagebox.showerror("Error", "Invalid email format. Must contain '@' and '.'.")
        return
    if qualification == "":
        messagebox.showerror("Error", "Qualification is required.")
        return
    
    cursor.execute("SELECT COUNT(*) FROM Users WHERE UserName = ?", (name,))
    count = cursor.fetchone()[0]

    if count > 0:
        messagebox.showerror("Error", "Username already exists! Choose another name.")
        return
    if name == "" or password == "" or phone == "" or email == "" or qualification == "":
        messagebox.showerror("Error", "All fields are required")
    else:
        cursor.execute(
            "INSERT INTO Users (UserName, Password, Gender, PhoneNumber, Email, Qualification) VALUES (?, ?, ?, ?, ?, ?)",
            (name, password, gender, phone, email, qualification)
        )
        conn.commit()
        messagebox.showinfo("Success", "Registration Successful!")
        clear_fields()
 
def clear_fields():
    name_info.set("")
    pass_info.set("")
    gender_info.set("")
    phoneNumber_entry.delete(0, END)
    Email_entry.delete(0, END)
    quali_dropdown.set("")        
        
Button(page2,text="Register",font="20",command=register_user,bg="lightgreen",bd=4).place(x=100,y=365)
Button(page2,text="Clear",font="20",command=clear_fields,bg="red",bd=4).place(x=270,y=365)
Button(page2, text="Back", font="15" ,bg="lightblue",bd=4,command=lambda: show_page(page1)).place(x=420, y=365)


# ----------- Page 3 -----------
page3 = Frame(screen, width=600, height=500, bg="lightblue")
page3.place(x=0, y=0)
page3.pack_propagate(False)

Label(page3, text="CRUD Operation", font="ariel 20 bold", bg="red", fg="white").pack(fill="both")

Label(page3, text="Username", font="20", bg="lightblue").place(x=50, y=70)
search_name = StringVar()
search_entry = Entry(page3, font="10", bd=4, textvariable=search_name)
search_entry.place(x=150, y=70)

Label(page3,text="UserName:",font="10",bg="lightblue").place(x=50,y=150)
Label(page3,text="Password:",font="10",bg="lightblue").place(x=50,y=195)
Label(page3,text="Gender:",font="10",bg="lightblue").place(x=50,y=240)
Label(page3,text="Phone:",font="10",bg="lightblue").place(x=50,y=285)
Label(page3,text="E-mail:",font="10",bg="lightblue").place(x=50,y=330)
Label(page3,text="Qualification:",font="10",bg="lightblue").place(x=50,y=375)
# ----------- Update Form Boxes -----------
u_name = Entry(page3, font="10", bd=4)
u_name.place(x=180, y=150)

u_pass = Entry(page3, font="10", bd=4)
u_pass.place(x=180, y=195)

u_gender = ttk.Combobox(page3, values=["Male", "Female"], font=("Arial", 10))
u_gender.place(x=180, y=240)

u_phone = Entry(page3, font="10", bd=4)
u_phone.place(x=180, y=285)

u_email = Entry(page3, font="10", bd=4)
u_email.place(x=180, y=330)

u_quali = ttk.Combobox(page3, values=["10th", "12th", "UG", "PG"], font=("Arial", 10))
u_quali.place(x=180, y=375)


def search_user():
    name = search_name.get().strip()
    if name == "":
        messagebox.showerror("Error", "Please enter a username to search.")
        return

    cursor.execute("SELECT * FROM Users WHERE UserName = ?", (name,))
    row = cursor.fetchone()

    if row:
        u_name.delete(0, END)
        u_name.insert(0, row[0])

        u_pass.delete(0, END)
        u_pass.insert(0, row[1])

        u_gender.set(row[2])

        u_phone.delete(0, END)
        u_phone.insert(0, row[3])

        u_email.delete(0, END)
        u_email.insert(0, row[4])

        u_quali.set(row[5])
    else:
        messagebox.showinfo("Not Found", "No user found with that username.")


def delete_user():
    name = search_name.get()
    if name == "":
        messagebox.showerror("Error", "Please enter a username to delete.")
        return
    cursor.execute("DELETE FROM Users WHERE UserName = ?", (name,))
    conn.commit()
    messagebox.showinfo("Success", "User deleted successfully!")
    reset_form()

def reset_form():
    search_name.set("")

    u_name.delete(0, END)
    u_pass.delete(0, END)
    u_gender.set("")
    u_phone.delete(0, END)
    u_email.delete(0, END)
    u_quali.set("")


def update_user():
    name = search_name.get().strip()

    if name == "":
        messagebox.showerror("Error", "Search username first.")
        return

    new_password = u_pass.get().strip()
    new_gender = u_gender.get().strip()
    new_phone = u_phone.get().strip()
    new_email = u_email.get().strip()
    new_quali = u_quali.get().strip()

    # Validations
    if new_password == "" or new_gender == "" or new_phone == "" or new_email == "" or new_quali == "":
        messagebox.showerror("Error", "All fields must be filled.")
        return

    if not (re.search("[A-Za-z]", new_password) and re.search("[0-9]", new_password)):
        messagebox.showerror("Error", "Password must contain both letters and numbers.")
        return

    if new_gender not in ["Male", "Female"]:
        messagebox.showerror("Error", "Gender must be Male or Female.")
        return

    if not new_phone.isdigit():
        messagebox.showerror("Error", "Phone must contain digits only.")
        return

    if len(new_phone) != 10:
        messagebox.showerror("Error", "Phone number must be exactly 10 digits.")
        return

    if "@" not in new_email or "." not in new_email:
        messagebox.showerror("Error", "Invalid email format. Must contain '@' and '.'.")
        return

    if new_quali not in ["10th", "12th", "UG", "PG"]:
        messagebox.showerror("Error", "Qualification must be 10th, 12th, UG, or PG.")
        return

    # Update in database
    cursor.execute("""
        UPDATE Users 
        SET Password=?, Gender=?, PhoneNumber=?, Email=?, Qualification=?
        WHERE UserName=?
    """, (new_password, new_gender, new_phone, new_email, new_quali, name))

    conn.commit()
    messagebox.showinfo("Success", "User updated successfully!")


Button(page3, text="Search", font="15",bg="blue" ,bd=4,command=search_user).place(x=400, y=67)
Button(page3, text="Update", font="15",bg="lightgreen",bd=4 ,command=update_user).place(x=50, y=420)
Button(page3, text="Delete", font="15",bg="red",bd=4,command=delete_user).place(x=170, y=420)
Button(page3, text="Reset", font="15",bg="orange",bd=4, command=reset_form).place(x=290, y=420)
Button(page3, text="Back", font="15", bg="lightblue",bd=4,command=lambda: show_page(page1)).place(x=410, y=420)

def show_page(page):
    page.tkraise()
    
# Start on page 1
show_page(page1)
mainloop() 