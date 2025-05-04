import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

def login():
    root = tk.Tk()
    root.title("Intelectica Login")
    root.geometry("800x600")

    bg_image = Image.open("../assets/login_background.png")
    bg_image = bg_image.resize((800, 600), Image.LANCZOS)
    bg_photo = ImageTk.PhotoImage(bg_image)

    bg_label = tk.Label(root, image=bg_photo)
    bg_label.image = bg_photo
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    font_title = ("Helvetica", 24, "bold")
    font_label = ("Helvetica", 12)
    entry_bg = "#ffffff"
    entry_bd = 2
    btn_bg = "#4a90e2"
    btn_fg = "#ffffff"
    btn_hover_bg = "#357ABD"

    def on_enter(e):
        button.config(bg=btn_hover_bg)

    def on_leave(e):
        button.config(bg=btn_bg)

    frame = tk.Frame(root, bg="#ffffff", bd=0, relief="ridge")
    frame.place(relx=0.5, rely=0.5, anchor="center", width=400, height=350)

    # Title
    label1 = tk.Label(frame, text="Welcome Back!", font=font_title, bg="#ffffff", fg="#333333")
    label1.pack(pady=(30, 20))

    # Username
    label2 = tk.Label(frame, text="Username", font=font_label, bg="#ffffff", anchor="w")
    label2.pack(fill="x", padx=40)
    entry1 = tk.Entry(frame, width=30, bd=entry_bd, bg=entry_bg)
    entry1.pack(pady=(0, 15), padx=40)

    # Password
    label3 = tk.Label(frame, text="Password", font=font_label, bg="#ffffff", anchor="w")
    label3.pack(fill="x", padx=40)
    entry2 = tk.Entry(frame, width=30, bd=entry_bd, bg=entry_bg, show="*")
    entry2.pack(pady=(0, 25), padx=40)

    # Button
    button = tk.Button(frame, text="Login", font=("Helvetica", 12, "bold"), width=20, height=2,
                       bg=btn_bg, fg=btn_fg, bd=0,
                       command=lambda: Login_button(root, entry1, entry2))
    button.pack()
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    label4 = tk.Label(frame, text="Create an account", font=("Helvetica", 10, "underline"), bg="#ffffff", fg="#3366cc", cursor="hand2")
    label4.pack(pady=(30, 20))
    label4.bind("<Button-1>", lambda e: open_registration_form(root))

    root.mainloop()

def Login_button(root, entry1, entry2):
    username = entry1.get()
    password = entry2.get()

    if not username or not password:
        tk.messagebox.showinfo("Info", "You must complete all fields!")
        return

    try:
        response = requests.post("http://127.0.0.1:5000/login", json={"username": username, "password": password})
        data = response.json()

        if response.status_code == 200:
            tk.messagebox.showinfo("Success", data["message"])
            root.destroy()
            # main_window(username)
        else:
            tk.messagebox.showerror("Error", data["message"])
    except Exception as e:
        tk.messagebox.showerror("Error", f"Could not connect to server: {e}")

    # if username in users_data and users_data[username]["password"] == password:
    #     tk.messagebox.showinfo("Info", "Connected!")
    #     root.destroy()
    #     mw.main_window(username, users_data[username]["role"], users_data, patients, treatments_report, treatments, doctors_report)
    # else:
    #     tk.messagebox.showinfo("Info", "Incorrect credentials!")

def open_registration_form(parent_window):
    # parent_window.destroy()
    registration_form()

def registration_form():
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

    tk.Label(window, text="Role").pack()
    role_var = tk.StringVar(window)
    role_var.set("elev")  # default
    role_menu = tk.OptionMenu(window, role_var, "elev", "profesor", "parinte")
    role_menu.pack(pady=5)

    def send_registration():
        data = {
            "username": username_entry.get(),
            "email": email_entry.get(),
            "password": password_entry.get(),
            "confirm": confirm_entry.get(),
            "role": role_var.get()
        }
        response = requests.post("http://localhost:5000/register", json=data)
        # tk.messagebox.showinfo("Server response", response.text)
        data = response.json()
        if response.status_code == 200:
                messagebox.showinfo("Success", data["message"])
                window.destroy()
        else:
            messagebox.showerror("Error", data["message"])

    tk.Button(window, text="Register", bg="#4CAF50", fg="white", command=send_registration).pack(pady=20)

    window.mainloop()
