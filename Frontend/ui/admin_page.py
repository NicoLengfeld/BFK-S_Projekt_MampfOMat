import tkinter as tk
from tkinter import PhotoImage, messagebox
import os

# In-memory product data
PRODUCTS = [
    {"id": 1, "name": "Croissant", "price": 2.20, "description": "Zartblättriges Buttercroissant."},
    {"id": 2, "name": "Brezel", "price": 1.50, "description": "Frisch gebackene Brezel."},
    {"id": 3, "name": "Muffin", "price": 2.50, "description": "Saftiger Muffin."},
]

class AdminPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#f7f7f7")

        tk.Label(
            self,
            text="🛠️ Admin Panel",
            font=("Helvetica", 24, "bold"),
            bg="#f7f7f7",
            fg="#333"
        ).pack(pady=20)

        self.products_frame = tk.Frame(self, bg="#f7f7f7")
        self.products_frame.pack()

        self.images = []
        self.load_products()

        tk.Button(
            self,
            text="➕ Produkt hinzufügen",
            font=("Helvetica", 14),
            bg="#4caf50",
            fg="#ffffff",
            command=self.add_product_window
        ).pack(pady=10)

    def load_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        self.images.clear()

        for i, product in enumerate(PRODUCTS):
            image_path = os.path.join(os.path.dirname(__file__), "..", "assets", f"{product['name']}.png")
            img = PhotoImage(file=image_path).subsample(4, 4)
            self.images.append(img)
            btn = tk.Button(
                self.products_frame,
                image=img,
                text=f"{product['name']}\n{product['price']}€",
                compound="top",
                font=("Helvetica", 12),
                bg="#ffffff",
                fg="#333",
                relief="groove",
                command=lambda p=product: self.edit_product(p),
                width=180, height=160
            )
            btn.grid(row=i//3, column=i%3, padx=20, pady=20)

    def edit_product(self, product):
        edit_window = tk.Toplevel(self)
        edit_window.title("Produkt bearbeiten")
        edit_window.geometry("400x300")
        edit_window.configure(bg="#f7f7f7")

        tk.Label(edit_window, text="Name:", bg="#f7f7f7", fg="#333").pack()
        name_var = tk.StringVar(value=product['name'])
        tk.Entry(edit_window, textvariable=name_var).pack()

        tk.Label(edit_window, text="Preis:", bg="#f7f7f7", fg="#333").pack()
        price_var = tk.DoubleVar(value=product['price'])
        tk.Entry(edit_window, textvariable=price_var).pack()

        tk.Label(edit_window, text="Beschreibung:", bg="#f7f7f7", fg="#333").pack()
        desc_var = tk.StringVar(value=product['description'])
        tk.Entry(edit_window, textvariable=desc_var).pack()

        def save_changes():
            product['name'] = name_var.get()
            product['price'] = price_var.get()
            product['description'] = desc_var.get()
            self.load_products()
            tk.messagebox.showinfo("Erfolg", "Produkt aktualisiert!")
            edit_window.destroy()

        def delete():
            PRODUCTS.remove(product)
            self.load_products()
            tk.messagebox.showinfo("Erfolg", "Produkt gelöscht!")
            edit_window.destroy()

        tk.Button(edit_window, text="Speichern", bg="#4caf50", fg="#ffffff", command=save_changes).pack(pady=5)
        tk.Button(edit_window, text="Löschen", bg="#f44336", fg="#ffffff", command=delete).pack(pady=5)

    def add_product_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Produkt hinzufügen")
        add_window.geometry("400x300")
        add_window.configure(bg="#f7f7f7")

        tk.Label(add_window, text="Name:", bg="#f7f7f7", fg="#333").pack()
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var).pack()

        tk.Label(add_window, text="Preis:", bg="#f7f7f7", fg="#333").pack()
        price_var = tk.DoubleVar()
        tk.Entry(add_window, textvariable=price_var).pack()

        tk.Label(add_window, text="Beschreibung:", bg="#f7f7f7", fg="#333").pack()
        desc_var = tk.StringVar()
        tk.Entry(add_window, textvariable=desc_var).pack()

        tk.Label(add_window, text="Bildname (z. B. Brezel.png):", bg="#f7f7f7", fg="#333").pack()
        image_var = tk.StringVar()
        tk.Entry(add_window, textvariable=image_var).pack()

        def add():
            image_path = os.path.join(os.path.dirname(__file__), "..", "assets", image_var.get())
            if not os.path.exists(image_path):
                tk.messagebox.showerror("Fehler", "Bilddatei existiert nicht!")
                return

            new_product = {
                "id": len(PRODUCTS) + 1,
                "name": name_var.get(),
                "price": price_var.get(),
                "description": desc_var.get(),
                "image": image_var.get()
            }
            PRODUCTS.append(new_product)
            self.load_products()
            tk.messagebox.showinfo("Erfolg", "Produkt hinzugefügt!")
            add_window.destroy()

        tk.Button(add_window, text="Hinzufügen", bg="#4caf50", fg="#ffffff", command=add).pack(pady=5)