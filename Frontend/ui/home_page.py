import tkinter as tk
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
        tk.Label(self, text="🍞 Willkommen beim Bäckerautomaten 🥐", font=("Arial", 18)).pack(pady=20)
        self.products_frame = tk.Frame(self)
        self.products_frame.pack()

        self.images = []
        for i, product in enumerate(PRODUCTS):
            image_path = os.path.join(os.path.dirname(__file__), "..", "assets", os.path.basename(product["image"]))
            img = PhotoImage(file=image_path).subsample(4, 4)
            self.images.append(img)  # sonst wird Bild gelöscht
            btn = tk.Button(
                self.products_frame,
                image=img,
                text=product["name"],
                compound="top",
                command=lambda p=product: controller.show_frame("ProductPage", product=p),
                width=180, height=160
            )
            btn.grid(row=i//3, column=i%3, padx=20, pady=20)

# Anmeldebutton unter den Produkten links
  # ⬇️ Anmelde-Button unter den Produkten links unten
        self.bottom_frame = tk.Frame(self)
        self.bottom_frame.pack(fill="x", pady=10, padx=20)

        self.login_button = tk.Button(
            self.bottom_frame,
            text="🔐 Anmelden",
            font=("Arial", 12),
            bg="#e0e0e0",
            relief="raised",
            command=self.open_login
        )
        self.login_button.pack(side="left", anchor="sw")

    def open_login(self):
        popup = tk.Toplevel(self)
        popup.title("Anmeldung")
        popup.geometry("300x200")

        tk.Label(popup, text="Login-Fenster", font=("Arial", 14)).pack(pady=20)
        tk.Label(popup, text="Benutzername:").pack()
        username_entry = tk.Entry(popup)
        username_entry.pack()
        tk.Label(popup, text="Passwort:").pack()
        password_entry = tk.Entry(popup, show="*")
        password_entry.pack()

        def login():
            username = username_entry.get()
            password = password_entry.get()
            if username == "admin" and password == "admin":
                popup.destroy()
                self.controller.show_frame("AdminPage")
            else:
                tk.Label(popup, text="Falsche Anmeldedaten!", fg="red").pack()

        tk.Button(popup, text="Anmelden", command=login).pack(pady=10)

