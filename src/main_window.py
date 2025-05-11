import requests
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox
import login as lg

def main_window(username, tier):
    root = tk.Tk()
    root.title("Intelectica")
    root.geometry("800x600")

    label1 = tk.Label(text = username, font=("Helvetica", 14))
    label1.place(x = 12, y = 12)

    button1 = tk.Button(text = "View Courses", command = lambda: view_courses(root), width = 16, height = 4)
    button1.place(x = 335, y = 140)

    button2 = tk.Button(text = "Sign Out", command = lambda: Sign_Out(root), width = 16, height = 4)
    button2.place(x = 335, y = 230)

    root.mainloop()

def view_courses():
    pass

def Sign_Out(root):
    root.destroy()
    lg.login()
