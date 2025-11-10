import tkinter as tk
from PIL import Image, ImageTk  # <--- wichtig für Größenanpassung der Bilder!
from tkinter import PhotoImage
import os

PRODUCTS = [
    {"name": "Brezel", "image": "assets/Brezel.png"},
    {"name": "Croissant", "image": "assets/Croissant.png"},
    {"name": "Brötchen", "image": "assets/Broetchen.png"},
    {"name": "Käsebrötchen", "image": "assets/Kaesebroetchen.png"},
    {"name": "Muffin", "image": "assets/Muffin.png"},
    {"name": "Berliner", "image": "assets/Berliner.png"},
]

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f7f7f7")

        tk.Label(
            self,
            text="🍞 Willkommen beim Bäckerautomaten 🥐",
            font=("Helvetica", 24, "bold"),
            bg="#f7f7f7",
            fg="#333"
        ).pack(pady=20)

        self.products_frame = tk.Frame(self, bg="#f7f7f7")
        self.products_frame.pack()

        self.images = []
        for i, product in enumerate(PRODUCTS):
            image_path = os.path.join(os.path.dirname(__file__), "..", "assets", os.path.basename(product["image"]))
            img = PhotoImage(file=image_path).subsample(4, 4)
            self.images.append(img)
            btn = tk.Button(
                self.products_frame,
                image=img,
                text=product["name"],
                compound="top",
                font=("Helvetica", 12),
                bg="#ffffff",
                fg="#333",
                relief="groove",
                command=lambda p=product: controller.show_frame("ProductPage", product=p),
                width=180, height=160
            )
            btn.grid(row=i//3, column=i%3, padx=20, pady=20)

        self.bottom_frame = tk.Frame(self, bg="#f7f7f7")
        self.bottom_frame.pack(fill="x", pady=10, padx=20)

        self.login_button = tk.Button(
            self.bottom_frame,
            text="🔐 Admin Login",
            font=("Helvetica", 14),
            bg="#4caf50",
            fg="#ffffff",
            relief="raised",
            command=self.open_login
        )
        self.login_button.pack(side="left", anchor="sw")

    def open_login(self):
        popup = tk.Toplevel(self)
        popup.title("Admin Login")
        popup.geometry("300x250")
        popup.configure(bg="#f7f7f7")

        tk.Label(
            popup,
            text="🔐 Admin Login",
            font=("Helvetica", 18, "bold"),
            bg="#f7f7f7",
            fg="#333"
        ).pack(pady=20)

        tk.Label(popup, text="Benutzername:", bg="#f7f7f7", fg="#333").pack()
        username_entry = tk.Entry(popup)
        username_entry.pack()

        tk.Label(popup, text="Passwort:", bg="#f7f7f7", fg="#333").pack()
        password_entry = tk.Entry(popup, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if username == "admin" and password == "admin":
                popup.destroy()
                self.controller.show_frame("AdminPage")
            else:
                tk.Label(popup, text="❌ Falsche Anmeldedaten!", fg="red", bg="#f7f7f7").pack()

        tk.Button(
            popup,
            text="Login",
            font=("Helvetica", 12),
            bg="#4caf50",
            fg="#ffffff",
            command=login
        ).pack(pady=10)

