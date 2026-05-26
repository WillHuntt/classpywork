import tkinter as tk
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk
import re

def validate_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email)

def register_student():
    name = entry_name.get()
    age = int(entry_age.get())
    phone = entry_phone.get()
    email1 = entry_email1.get()
    email2 = entry_email2.get()

    if email1 != email2:
        messagebox.showerror("Error", "Emails do not match!")
        return 
    
    if not validate_email(email1):
        messagebox.showerror("Error", "Invalid email address: " + email1)
        return
    
    conn = sqlite3.connect('student_records.db')
    cursor = conn.cursor()

    cursor.execute(''' INSERT INTO students (name, age, phone, email) 
                       VALUES (?, ?, ?, ?)''', (name, age, phone, email1))
    conn.commit()
    conn.close()

    messagebox.showinfo("Success", "Student registered successfully!")

window = tk.Tk()
window.title("Student Registration")

background_image = ImageTk.PhotoImage(Image.open("background.png"))
background_label = tk.Label(window, image=background_image)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

label_name = tk.Label(window, text="Name:", bg="white")
label_name.place(x=50, y=100)
entry_name = tk.Entry(window)
entry_name.place(x=150, y=100)

label_age = tk.Label(window, text="Age:", bg="white")
label_age.place(x=50, y=150)
entry_age = tk.Entry(window)
entry_age.place(x=150, y=150)

label_phone = tk.Label(window, text="Phone:", bg="white")
label_phone.place(x=50, y=200)
entry_phone = tk.Entry(window)
entry_phone.place(x=150, y=200)

label_email1 = tk.Label(window, text="Email:", bg="white")
label_email1.place(x=50, y=250)
entry_email1 = tk.Entry(window)
entry_email1.place(x=150, y=250)

label_email2 = tk.Label(window, text="Confirm Email:", bg="white")
label_email2.place(x=50, y=300)
entry_email2 = tk.Entry(window)
entry_email2.place(x=150, y=300)

button_register = tk.Button(window, text="Register", command=register_student)
button_register.place(x=150, y=350)

window.mainloop()