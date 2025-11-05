import tkinter as tk
from tkinter import PhotoImage, messagebox

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

        tk.Label(self, text="🛠️ Admin Panel", font=("Arial", 18)).pack(pady=20)
        self.products_frame = tk.Frame(self)
        self.products_frame.pack()

        self.images = []
        self.load_products()

        tk.Button(self, text="Produkt hinzufügen", command=self.add_product_window).pack(pady=10)

    def load_products(self):
        for widget in self.products_frame.winfo_children():
            widget.destroy()

        self.images.clear()

        for i, product in enumerate(PRODUCTS):
            img = PhotoImage(file=f"assets/{product['name']}.png").subsample(4, 4)
            self.images.append(img)
            btn = tk.Button(
                self.products_frame,
                image=img,
                text=f"{product['name']}\n{product['price']}€",
                compound="top",
                command=lambda p=product: self.edit_product(p),
                width=180, height=160
            )
            btn.grid(row=i//3, column=i%3, padx=20, pady=20)

    def edit_product(self, product):
        edit_window = tk.Toplevel(self)
        edit_window.title("Produkt bearbeiten")

        tk.Label(edit_window, text="Name:").pack()
        name_var = tk.StringVar(value=product['name'])
        tk.Entry(edit_window, textvariable=name_var).pack()

        tk.Label(edit_window, text="Preis:").pack()
        price_var = tk.DoubleVar(value=product['price'])
        tk.Entry(edit_window, textvariable=price_var).pack()

        tk.Label(edit_window, text="Beschreibung:").pack()
        desc_var = tk.StringVar(value=product['description'])
        tk.Entry(edit_window, textvariable=desc_var).pack()

        def save_changes():
            product['name'] = name_var.get()
            product['price'] = price_var.get()
            product['description'] = desc_var.get()
            self.load_products()
            messagebox.showinfo("Erfolg", "Produkt aktualisiert!")
            edit_window.destroy()

        def delete():
            PRODUCTS.remove(product)
            self.load_products()
            messagebox.showinfo("Erfolg", "Produkt gelöscht!")
            edit_window.destroy()

        tk.Button(edit_window, text="Speichern", command=save_changes).pack(pady=5)
        tk.Button(edit_window, text="Löschen", command=delete).pack(pady=5)

    def add_product_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Produkt hinzufügen")

        tk.Label(add_window, text="Name:").pack()
        name_var = tk.StringVar()
        tk.Entry(add_window, textvariable=name_var).pack()

        tk.Label(add_window, text="Preis:").pack()
        price_var = tk.DoubleVar()
        tk.Entry(add_window, textvariable=price_var).pack()

        tk.Label(add_window, text="Beschreibung:").pack()
        desc_var = tk.StringVar()
        tk.Entry(add_window, textvariable=desc_var).pack()

        def add():
            new_product = {
                "id": len(PRODUCTS) + 1,
                "name": name_var.get(),
                "price": price_var.get(),
                "description": desc_var.get()
            }
            PRODUCTS.append(new_product)
            self.load_products()
            messagebox.showinfo("Erfolg", "Produkt hinzugefügt!")
            add_window.destroy()

        tk.Button(add_window, text="Hinzufügen", command=add).pack(pady=5)