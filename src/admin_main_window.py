import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import login as lg

def admin_main_window():
    root = tk.Tk()
    root.title("Intelectica")
    root.geometry("800x600")

    button1 = tk.Button(text = "Create teacher account", command = lambda: create_teacher_acc(root), width = 20, height = 4)
    button1.place(x = 335, y = 140)

    button2 = tk.Button(text = "Create courses", command = lambda: create_courses(root), width = 20, height = 4)
    button2.place(x = 335, y = 230)

    button3 = tk.Button(text = "Add students to a course", command = lambda: add_students(root), width = 20, height = 4)
    button3.place(x = 335, y = 320)

    button4 = tk.Button(text = "Sign Out", command = lambda: Sign_Out(root), width = 20, height = 4)
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
    window = tk.Tk()
    window.title("Create Course")
    window.geometry("400x300")

    tk.Label(window, text="Nume Clasa:").pack(pady=5)
    clasa_entry = tk.Entry(window)
    clasa_entry.pack(pady=5)

    tk.Label(window, text="Alege Profesorul:").pack(pady=5)
    profesor_var = tk.StringVar(window)
    dropdown = tk.OptionMenu(window, profesor_var, "")
    dropdown.pack(pady=5)

    # Se încarcă profesorii din backend
    def populate_profesori():
        response = requests.get("http://localhost:5000/get_profesori")
        if response.status_code == 200:
            profesori = response.json()
            options = {p["username"]: p["id"] for p in profesori}
            profesor_var.set(next(iter(options)))  # Setează prima opțiune
            dropdown["menu"].delete(0, "end")
            for username, id_prof in options.items():
                dropdown["menu"].add_command(label=username, command=tk._setit(profesor_var, username))
            dropdown.profesor_options = options
        else:
            messagebox.showerror("Error", "Eroare la obținerea listei de profesori")

    populate_profesori()

    def send_create_course():
        selected_name = profesor_var.get()
        profesor_id = dropdown.profesor_options.get(selected_name)

        data = {
            "nume_clasa": clasa_entry.get(),
            "profesor_id": profesor_id
        }
        response = requests.post("http://localhost:5000/create_clasa", json=data)
        data = response.json()
        if response.status_code == 200:
            messagebox.showinfo("Success", data["message"])
            window.destroy()
        else:
            messagebox.showerror("Error", data["message"])

    tk.Button(window, text="Creeaza Clasa", command=send_create_course, bg="blue", fg="white").pack(pady=20)

    window.mainloop()

def add_students(root):
    window = tk.Tk()
    window.title("Adauga Elev la Clasa")
    window.geometry("400x300")

    tk.Label(window, text="Selecteaza Elevul:").pack(pady=5)
    elev_var = tk.StringVar(window)
    elev_dropdown = tk.OptionMenu(window, elev_var, "")
    elev_dropdown.pack(pady=5)

    tk.Label(window, text="Selecteaza Clasa:").pack(pady=5)
    clasa_var = tk.StringVar(window)
    clasa_dropdown = tk.OptionMenu(window, clasa_var, "")
    clasa_dropdown.pack(pady=5)

    elev_map = {}
    clasa_map = {}

    def populate_data():
        # Elevi
        elev_resp = requests.get("http://localhost:5000/get_elevi")
        if elev_resp.status_code == 200:
            elevi = elev_resp.json()
            elev_dropdown["menu"].delete(0, "end")
            for e in elevi:
                elev_map[e["nume_complet"]] = e["id"]
                elev_dropdown["menu"].add_command(label=e["nume_complet"], command=tk._setit(elev_var, e["nume_complet"]))
            elev_var.set(next(iter(elev_map)))

        # Clase
        clasa_resp = requests.get("http://localhost:5000/get_clase")
        if clasa_resp.status_code == 200:
            clase = clasa_resp.json()
            clasa_dropdown["menu"].delete(0, "end")
            for c in clase:
                clasa_map[c["nume"]] = c["id"]
                clasa_dropdown["menu"].add_command(label=c["nume"], command=tk._setit(clasa_var, c["nume"]))
            clasa_var.set(next(iter(clasa_map)))

    populate_data()

    def send_add():
        elev_id = elev_map.get(elev_var.get())
        clasa_id = clasa_map.get(clasa_var.get())

        response = requests.post("http://localhost:5000/add_student_to_class", json={
            "elev_id": elev_id,
            "clasa_id": clasa_id
        })

        data = response.json()
        if response.status_code == 200:
            messagebox.showinfo("Succes", data["message"])
            window.destroy()
        else:
            messagebox.showerror("Eroare", data["message"])

    tk.Button(window, text="Adauga Elev", command=send_add, bg="green", fg="white").pack(pady=20)

    window.mainloop()


def Sign_Out(root):
    root.destroy()
    lg.login()
