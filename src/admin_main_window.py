import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import login as lg

def admin_main_window():
    root = tk.Tk()
    root.title("Intelectica")
    root.geometry("800x600")

    button1 = tk.Button(text = "Create teacher account", command = lambda: create_teacher_acc(root), width = 16, height = 4)
    button1.place(x = 335, y = 140)

    button2 = tk.Button(text = "Create courses", command = lambda: create_courses(root), width = 16, height = 4)
    button2.place(x = 335, y = 230)

    button3 = tk.Button(text = "Add students to a course", command = lambda: add_students(root), width = 16, height = 4)
    button3.place(x = 335, y = 320)

    button4 = tk.Button(text = "Sign Out", command = lambda: Sign_Out(root), width = 16, height = 4)
    button4.place(x = 335, y = 410)

    root.mainloop()

def create_teacher_acc(root):
    window = tk.Tk()
    window.title("Register")
    window.geometry("400x500")

    tk.Label(window, text="Registration Form", font=("Helvetica", 16, "bold")).pack(pady=20)

    tk.Label(window, text="Username").pack()
    username_entry = tk.Entry(window)
    username_entry.pack(pady=5)

    tk.Label(window, text="Email").pack()
    email_entry = tk.Entry(window)
    email_entry.pack(pady=5)

    tk.Label(window, text="Password").pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=5)

    tk.Label(window, text="Confirm Password").pack()
    confirm_entry = tk.Entry(window, show="*")
    confirm_entry.pack(pady=5)

    def send_registration():
        data = {
            "username": username_entry.get(),
            "email": email_entry.get(),
            "password": password_entry.get(),
            "confirm": confirm_entry.get(),
            "role": "profesor"
        }
        response = requests.post("http://localhost:5000/register", json=data)
        data = response.json()
        if response.status_code == 200:
                messagebox.showinfo("Success", data["message"])
                window.destroy()
        else:
            messagebox.showerror("Error", data["message"])

    tk.Button(window, text="Register", bg="#4CAF50", fg="white", command=send_registration).pack(pady=20)

    window.mainloop()

def create_courses(root):
    pass

def add_students(root):
    pass

def Sign_Out(root):
    root.destroy()
    lg.login()
