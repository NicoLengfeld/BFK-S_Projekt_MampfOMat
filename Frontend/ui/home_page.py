import tkinter as tk
from PIL import Image, ImageTk  # <--- wichtig!
from tkinter import PhotoImage
import os

PRODUCTS = [
    {"name": "Brezel", "image": "assets/Brezel.png"},
    {"name": "Croissant", "image": "assets/Croissant.png"},
    {"name": "Brötchen", "image": "assets/Broetchen.png"},
    {"name": "Donut", "image": "assets/Kaesebroetchen.png"},
    {"name": "Muffin", "image": "assets/Muffin.png"},
    {"name": "Berliner", "image": "assets/Berliner.png"},
]

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="🍞 Willkommen beim Bäckerautomaten 🍩", font=("Arial", 18)).pack(pady=20)

        self.products_frame = tk.Frame(self)
        self.products_frame.pack()

        self.images = []

        # --- Produkte im Raster anzeigen ---
        for i, product in enumerate(PRODUCTS):
            # Öffne Bild mit Pillow, skaliere es auf 120x120 Pixel
            img = Image.open(product["image"])
            img = img.resize((120, 120), Image.Resampling.LANCZOS)  # gleich große Bilder
            tk_img = ImageTk.PhotoImage(img)
            self.images.append(tk_img)

            # Erstelle Button mit Bild
            btn = tk.Button(
                self.products_frame,
                image=tk_img,
                text=product["name"],
                compound="top",
                command=lambda p=product: controller.show_frame("ProductPage", product=p),
                width=160, height=160,  # sorgt für gleich große Buttons
                relief="raised",
                bg="white"
            )
            btn.grid(row=i // 3, column=i % 3, padx=20, pady=20)

        # --- Anmelde-Button unten links ---
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
        tk.Entry(popup).pack()
        tk.Label(popup, text="Passwort:").pack()
        tk.Entry(popup, show="*").pack()
        tk.Button(popup, text="Anmelden", command=popup.destroy).pack(pady=10)
